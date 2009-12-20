# -*- coding: utf-8 -*-

__all__ = ['Alarm']
# TODO: Clear Code

import locale
import datetime
import time
import gconf
from sys import stderr
from gobject import timeout_add
from subprocess import Popen
from gtk import RESPONSE_YES
from gtk import RESPONSE_NO


from lib import common
from lib import i18n
from lib import dialogs
from lib.bubble import NotifyMessage
from lib.utils import verify_pid
from lib.utils import Message
from lib.bill import Bill
from lib.config import Configuration

class Alarm(object):

    def __init__(self, parent):
        self.parent = parent
        self.tray_hints = {}
        self.parent = parent
        self.tray_hints = {}
        self.gconf_client = Configuration()
        self.start()

    def start(self):

        start_delay = self.gconf_client.start_delay()

        showStartup = self.gconf_client.show_startup_notifications()

        if showStartup:
            timeout_add(start_delay, self.show_pay_notification)
            timeout_add(start_delay + 12000, self.verify_due)

        interval = self.gconf_client.get_interval()

        if interval:
            timeout_add(interval, self.timer)

    def notification(self, title, body):
        notify = NotifyMessage(self.parent)
        notify.title = title
        notify.body = body
        notify.set_timeout(20)
        notify.set_default_action(self.__cb_launch_gui)
        notify.hints = self.tray_hints
        return notify

    def show_pay_notification(self):
        print "Got here 3"
        today = datetime.date.today()
        limit = self.gconf_client.notification_days_limit()
        limit = datetime.timedelta(days=limit)
        if limit:
            records = self.parent.actions.get_interval_bills(end=today+limit, paid=False)
            #'dueDate <= %s AND paid = 0' % (today + limit))
        else:
            records = self.parent.actions.get_bills(paid=False)

        msg = ngettext('You have %s outstanding bill to pay!',
            'You have %s outstanding bills to pay!',
            len(records)) % len(records)
        if msg and records:
            bubble = self.notification(common.APPNAME, msg)
            bubble.add_action("view", _("Show BillReminder"),
                self.__cb_launch_gui, None)
            bubble.add_action("close", _("Cancel"), None)
            bubble.show()

        return False

    def verify_due(self, sum=0):
        print "Got here 2"
        showDueAlarm = self.gconf_client.show_due_alarm
        if not showDueAlarm:
            return
        today = datetime.date.today()
        if sum > 0:
            records = self.parent.actions.get_interval_bills(today, today, False)
        else:
            records = self.parent.actions.get_interval_bills(end=today, paid=False)

        i = 1

        use_dialog = self.gconf_client.use_alert_dialog()

        # TODO: use only one dialog for all bills, if use_dialog == True
        for bill in records:
            if sum > 0:
                # date format string
                dtformat = locale.nl_langinfo(locale.D_FMT)
                # date from record in timestamp format
                dtstamp = bill.dueDate
                # record dictionary
                recDict = {
                    'bill': "<b>\"%s\"</b>" % bill.payee,
                    'day': "<b>\"%s\"</b>" % dtstamp.strftime(dtformat).encode('ASCII')
                }

                # TODO: calculate days
                timeout_add(i * 12000, 
                    self.show_bill_notification,
                    bill,
                    _("The bill %(bill)s will be due at %(day)s.") % recDict,
                    use_dialog)
            else:
                timeout_add(i * 12000,
                    self.show_bill_notification,
                    bill,
                    None,
                    use_dialog)
            i += 1

    def show_bill_notification(self, bill=None, msg=None, alert=False, timeout=None):
        if msg is None:
            msg = _('The bill %s is due.') % "<b>\"%s\"</b>" % bill.payee
        if not self.parent.actions.get_bills(id=bill.id)[0].paid:
            if alert:
                alert = Message().ShowBillInfo(text=msg,
                    title=_("BillReminder Notifier"))
                if alert == RESPONSE_YES:
                    self.__cb_mark_as_paid(None, (bill,))
                elif alert == RESPONSE_NO:
                    self.__cb_edit_bill(None, (bill,))
            else:
                bubble = self.notification(common.APPNAME, msg)
                bubble.add_action("paid", _("Mark as paid"),
                    self.__cb_mark_as_paid, bill)
                bubble.add_action("edit", _("Edit"), self.__cb_edit_bill, bill)
                bubble.add_action("close", _("Cancel"), None)
                if timeout:
                    bubble.set_timeout(timeout)
                bubble.show()
        return False

    def __cb_launch_gui(self, *arg):
    # If client is not running, launch it
        # Send DBus 'show_main_window' signal
        self.parent.dbus_server.show_main_window()
        if not self.parent.client_pid or \
           not verify_pid(self.parent.client_pid):
            gui = Popen('billreminder', shell=True)
            self.parent.client_pid = gui.pid

    def __cb_mark_as_paid(self, *arg):
        record = arg[1][0]
        if record:
            record.paid = True
            try:
                # Edit bill to database
                self.parent.dbus_server.edit_bill(record)
            except Exception, e:
                print str(e)

    def __cb_edit_bill(self, *arg):
        record = dialogs.edit_dialog(Bill(arg[1][0]))
        if record:
            try:
                # Edit bill to database
                self.parent.dbus_server.edit_bill(record)
            except Exception, e:
                print str(e)

    def timer(self):
        interval = self.gconf_client.get_interval()
        now = datetime.datetime.now()

        alert_hour, alert_minute = self.gconf_client.show_alarm_at_time()

        alert_hour = int(alert_hour)
        alert_minute = int(alert_minute)
        alert = datetime.datetime(now.year, now.month, now.day, alert_hour, alert_minute)
        now = int(time.mktime(now.timetuple()))
        alert = int(time.mktime(alert.timetuple()))
        # Alarm for bills which will be due before n days
        beforeAlarm = self.gconf_client.show_before_alarm()
        if beforeAlarm and alert >= (now - interval/2) and alert < (now + interval/2):
            days = self.gconf_client.show_alarm_before_days()
            self.verify_due(days)

        startAlarm = now - interval/2
        endAlarm = now + interval/2
        records = self.parent.actions.get_alarm_bills(startAlarm, endAlarm, 0)

        i = 0
        use_dialog = self.gconf_client.use_alert_dialog()
        for bill in records:
            # date format string
            dtformat = locale.nl_langinfo(locale.D_FMT)
            # date from record in timestamp format
            dtstamp = bill.dueDate
            # record dictionary
            recDict = {
                'bill': "<b>\"%s\"</b>" % bill.payee,
                'day': "<b>\"%s\"</b>" % dtstamp.strftime(dtformat).encode('ASCII')
            }

            timeout_add(i * 12000,
                self.show_bill_notification,
                bill,
                _("The bill %(bill)s will be due at %(day)s.") % recDict,
                use_dialog,
                -1)

            i += 1
        print (now - interval, now), records

        return True
