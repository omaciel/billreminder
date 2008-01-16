# -*- coding: utf-8 -*-

__all__ = ['Alarm']
# TODO: Clear Code

import datetime
import time
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

class Alarm(object):

    def __init__(self, parent):
        self.parent = parent
        self.tray_hints = {}
        self.parent = parent
        self.tray_hints = {}
        self.start()

    def start(self):
        start_delay = self.parent.config.getint('General', 'delay') * 60000
        print start_delay
        if self.parent.config.getboolean('Alarm', 'show_startup_notification'):
            timeout_add(start_delay, self.show_pay_notification)
            timeout_add(start_delay + 12000, self.verify_due)
        interval = self.parent.config.getint('Alarm', 'interval') * 1000
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
        today = time.mktime(datetime.date.today().timetuple())
        limit = self.parent.config.getint('Alarm',
                                          'notification_days_limit') * 86400.0
        if limit:
            records = self.parent.actions.get_bills('dueDate <= %s AND ' \
                                               'paid = 0' % (today + limit))
        else:
            records = self.parent.actions.get_bills('paid = 0')

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
        if not self.parent.config.getboolean('Alarm', 'show_due_alarm'):
            return
        today = time.mktime(datetime.date.today().timetuple())
        if sum > 0:
            records = self.parent.actions.get_bills('dueDate <= %s ' \
                                                    'AND dueDate > %s ' \
                                                    'AND paid = 0' % \
                                                    (today + (sum * 86400),
                                                    today))
            print records
        else:
            records = self.parent.actions.get_bills('dueDate < %s ' \
                                                    'AND paid = 0' % \
                                                    today)

        i = 1
        use_dialog = self.parent.config.getboolean('Alarm', 'use_alert_dialog')
        # TODO: use only one dialog for all bills, if use_dialog == True
        for bill in records:
            if sum > 0:
                # TODO: calculate days
                timeout_add(i * 12000, self.show_bill_notification, bill,
                    _("The bill %(bill)s will be due at %(day)s.") %\
                      {'bill': "<b>\"%s\"</b>" % bill['payee'],
                      'day': "<b>\"%s\"</b>" % datetime.datetime.fromtimestamp( \
                                int(bill['dueDate'])).strftime(_('%Y/%m/%d' \
                                ).encode('ASCII'))},
                    use_dialog)
            else:
                timeout_add(i * 12000,
                            self.show_bill_notification, bill, None, use_dialog)
            i += 1

    def show_bill_notification(self, bill=None, msg=None, alert=False, timeout=None):
        if msg is None:
            msg = _('The bill %s is due.') % "<b>\"%s\"</b>" % bill['payee']
        if self.parent.actions.get_bills({'Id': bill['Id']})[0]['paid'] == 0:
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
            record['paid'] = 1
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
                self.parent.dbus_server.edit_bill(record.Dictionary)
            except Exception, e:
                print str(e)

    def timer(self):

        interval = self.parent.config.getint('Alarm', 'interval')
        now = datetime.datetime.now()
        alert_hour, alert_minute = self.parent.config.get('Alarm',
                                     'show_alarm_at_time').split(':')
        alert_hour = int(alert_hour)
        alert_minute = int(alert_minute)
        alert = datetime.datetime(now.year, now.month, now.day,
                                  alert_hour, alert_minute)
        now = int(time.mktime(now.timetuple()))
        alert = int(time.mktime(alert.timetuple()))
        # Alarm for bills wich will be due before n days
        if self.parent.config.getboolean('Alarm', 'show_before_alarm') \
           and alert >= (now - interval/2) and alert < (now + interval/2):
            days = self.parent.config.getint('Alarm', 'show_alarm_before_days')
            self.verify_due(days)

        records = self.parent.actions.get_bills('alarm >= %d AND ' \
                        'alarm < %d AND paid = 0' \
                        % (now - interval/2, now + interval/2))

        i = 0
        use_dialog = self.parent.config.getboolean('Alarm', 'use_alert_dialog')
        for bill in records:
            timeout_add(i * 12000, self.show_bill_notification, bill,
                    _("The bill %(bill)s will be due at %(day)s.") %\
                      {'bill': "<b>\"%s\"</b>" % bill['payee'],
                       'day': "<b>\"%s\"</b>" % datetime.datetime.fromtimestamp( \
                                int(bill['dueDate'])).strftime(_('%Y/%m/%d' \
                                ).encode('ASCII'))}, use_dialog, -1)

            i += 1
        print (now - interval, now), records

        return True
