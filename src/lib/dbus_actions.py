# -*- coding: utf-8 -*-

__all__ = ['Actions']

import dbus
import dbus.service
import os
from subprocess import Popen

from lib import common, scheduler
from lib.utils import force_string
from lib.utils import Message
from db.entities import Bill, Category

class Actions(object):

    def __init__(self, databaselayer=None):
        try:
            session_bus = dbus.SessionBus()
            obj = session_bus.get_object(common.DBUS_INTERFACE,
                                         common.DBUS_PATH)
            self.dbus_interface = dbus.Interface(obj, common.DBUS_INTERFACE)
            pid = os.getpid()
            self.dbus_interface.register(pid)
        except dbus.DBusException:
            '''if Message().ShowErrorQuestion( \
              _("An error occurred while connecting to BillReminder Notifier!\n"\
                "Do you want to launch it and restart BillReminder?")):
                Popen('python billreminderd --open-gui', shell=True)
                raise SystemExit
            return False'''
            print 'error'

    def _correct_type(self, record):
        if not isinstance(record, dict):
            return record

        

        return record

    def get_interval_bills(self, start, end, paid):
        #try:
        ret = []
        records = self.dbus_interface.get_interval_bills(start.toordinal(), end.toordinal(), paid)
        print records
        for record in records:
            record = self._correct_type(record)
            ret.append(record)
        return ret
        #except dbus.DBusException:
        #    if self.__init__():
        #        return self.get_monthly_bills(status, start, end)

    def get_alarm_bills(self, start, end, paid):
        #try:
        ret = []
        records = self.dbus_interface.get_alarm_bills(start.toordinal(), end.toordinal(), paid)
        for record in records:
            record = self._correct_type(record)
            ret.append(record)
        return ret
        #except dbus.DBusException:
        #    if self.__init__():
        #        return self.get_monthly_bills(status, start, end)

    def get_monthly_totals(self, month, year, paid):
        # Return a list of categories and totals for the given month
        #try:
        ret = []
        records = self.dbus_interface.get_monthly_totals(month.toordinal(), year.toordinal(), paid)
        for record in records:
            record = self._correct_type(record)
            ret.append(record)
        return ret
        #except dbus.DBusException:
        #    if self.__init__():
        #        return self.get_monthly_totals(status, month, year)


    def get_monthly_bills(self, month, year, paid):
        #try:
        ret = []
        records = self.dbus_interface.get_monthly_bills(month, year, paid)
        for record in records:
            record = self._correct_type(record)
            ret.append(record)
        return ret
        #except dbus.DBusException:
        #    if self.__init__():
        #        return self.get_monthly_bills(status, month, year)

    def get_bills(self, **kwargs):
        """ Returns one or more records that meet the criteria passed """
        try:
            ret = []
            if isinstance(kwargs, basestring):
                records = self.dbus_interface.get_bills_(**kwargs)
            else:
                records = self.dbus_interface.get_bills(force_string(kwargs))
            for record in records:
                record = self._correct_type(record)
                ret.append(record)
            return ret
        except dbus.DBusException:
            if self.__init__():
                return self.get_bills(**kwargs)

    def get_categories(self, **kwargs):
        """ Returns one or more records that meet the criteria passed """
        try:
            ret = []
            print kwargs
            if isinstance(kwargs, basestring):
                records = self.dbus_interface.get_categories_(kwargs)
            else:
                records = self.dbus_interface.get_categories(force_string(kwargs))
            for record in records:
                record = self._correct_type(record)
                ret.append(record)
            return ret
        except dbus.DBusException:
            if self.__init__():
                return self.get_categories(**kwargs)

    def add(self, kwargs):
        """ Adds a bill to the database """
        try:
            record = self.dbus_interface.add(force_string(kwargs.__dict__))
            return self._correct_type(record)
        except dbus.DBusException:
            if self.__init__():
                return self.add(kwargs)

    def edit(self, kwargs):
        """ Edit a record in the database """
        try:
            record = self.dbus_interface.edit(force_string(kwargs.__dict__))
            return self._correct_type(record)
        except dbus.DBusException:
            if self.__init__():
                return self.edit(kwargs)

    def delete(self, kwargs):
        """ Delete a record in the database """
        try:
            return self.dbus_interface.delete(force_string(props(kwargs)))
        except dbus.DBusException:
            if self.__init__():
                return self.delete(kwargs)
