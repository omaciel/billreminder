#!/usr/bin/python
# -*- coding: utf-8 -*-

__all__ = ['Daemon']

import datetime
import time
import os
import gobject
import dbus
import gtk
import locale
locale.setlocale(locale.LC_ALL, '')

import common
import model.i18n
import model.daemon
import controller.trayicon
import model.dbus_manager
from model.dbus_manager import DaemonDBus

class Daemon(model.daemon.Daemon):

    def __init__(self):
        model.daemon.Daemon.__init__(self)
        self.__loop()

        # Verify if daemon is already running.
        try:
            session_bus = dbus.SessionBus()
            obj = session_bus.get_object("org.freedesktop.DBus", "/org/freedesktop/DBus")
            iface = dbus.Interface(obj, 'org.freedesktop.DBus')
            if "org.gnome.Billreminder.Daemon" in iface.ListNames():
                print 'Already running'
                return
        except:
            pass

        self.dbus_service = DaemonDBus(self)   

        self.__set_alarm()

        # Keep daemon running
        self.mainloop = gobject.MainLoop()
        self.mainloop.run()

    def __getBills(self, cat):
        date = None
        msg = ''
        for i in cat:
            if date != i['dueDate']:
                msg = '%(msg)s\n<i>%(date)s</i>\n' % \
                    dict(msg=msg, date=datetime.datetime.fromtimestamp(i['dueDate']).strftime(_('%Y/%m/%d').encode('ASCII')))
            item = '%(payee)s - %(currency)s %(amountDue)0.2f' % \
                dict(payee=i['payee'], currency=locale.localeconv()['currency_symbol'], amountDue=i['amountDue'])
            msg = '%(msg)s%(item)s\n' % dict(msg=msg, item=item)
            date = i['dueDate']
        return msg

    def create_message(self, msg='', show=False):
        if not msg:
            today = time.mktime(datetime.date.today().timetuple())
            limit = today + (float(self.config.get('Notification.Days')) 
                             * 86400.0)
            due = self.dal.get('tblbills', 'dueDate <= %s AND paid == 0' 
                               % today)

            if len(due) == 1:
                msg += '\n' + _('You have 1 outstanding bill to pay!')
            elif len(due) > 1:
                msg += '\n' + (_('You have %s outstanding bills to pay!') 
                               % len(due))

        if msg and show:
            self.show_message(_('BillReminder'), msg)
        return msg

    def __loop(self):
        self.create_message(show=True)
        gobject.timeout_add(int(self.config.get('Notification.Interval')) * 1000, self.__loop)

    def __alarm(self):
        self.create_message(show=True)
        self.__set_alarm()

    def __set_alarm(self):
        a_hour, a_min  = self.config.get('Notification.Alarm').split(':')
        a_time = int((float(a_hour) + (float(a_min) / 60.0)) * 3600.0)
        today = int(time.mktime(datetime.date.today().timetuple()))
        now = int(time.time())
        n_time = now - today
        _time = a_time - n_time
        if _time <= 0: _time += 86400
        print _time
        gobject.timeout_add(_time * 1000, self.__alarm)
    
    def __launchBR(self, *arg):
        gobject.timeout_add(10, os.system, 'python -OO startup.py --from_daemon')
        
    def __notify_action(self, *arg):
        print arg
        if model.dbus_manager.verify_service('org.gnome.Billreminder'):
            print 'Show UI'
            session_bus = dbusus.SessionBus()
            obj = session_bus.get_object('org.gnome.Billreminder', '/org/gnome/Billreminder')
            interface = DBus.Interface(obj, 'org.gnome.Billreminder')
            interface.show_window()
            
        else:
            print 'Launch UI'
            self.__launchBR(arg)

    def show_message(self, title, msg):
        try:
            if model.dbus_manager.verify_service('org.gnome.Billreminder'):
                session_bus = dbus.SessionBus()  
                obj = session_bus.get_object('org.gnome.Billreminder', '/org/gnome/Billreminder')
                interface = dbus.Interface(obj, 'org.gnome.Billreminder')
                interface.show_message(title, msg)
            else: 
                raise Exception()
        except:
    	    notif = controller.trayicon.NotifyMessage()
            notif.AppName('BillReminder')
            notif.Title(title)
            notif.Body(msg)
            notif.Icon(os.path.abspath(common.APP_HEADER))
            notif.Timeout(20)
            notif.Action(self.__notify_action)
            notif.Notify() 
            
