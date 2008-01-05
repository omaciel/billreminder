#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['NotifyMessage']

from sys import stderr

from lib import common
from lib import i18n
from lib.utils import verify_pid
from lib.utils import get_dbus_interface

class NotifyMessage(object):

    def __init__(self, parent):
        """ Constructor """
        self.title = common.APPNAME
        self.__replaces_id = 0
        self.icon = common.APP_HEADER
        self.summary = ''
        self.body = ''
        self.actions = []
        self.hints = {}
        self.expire_timeout = 1000
        self.__default_action_func = None
        self.__action_func = {}
        self.parent = parent

        # Connect DBus notification interface
        self.__interface = get_dbus_interface(common.NOTIFICATION_INTERFACE,
                                              common.NOTIFICATION_PATH)
        self.__interface.connect_to_signal('ActionInvoked',
                                           self.__on_action_invoked)


    def add_action(self, action, label, callback, *arg):
        self.actions.append(action)
        self.actions.append(label)
        self.__action_func[action] = (callback, arg)

    def set_timeout(self, expire_timeout):
        self.expire_timeout = expire_timeout * 1000

    def set_default_action(self, callback):
        self.__default_action_func = callback

    def __on_action_invoked(self, *arg):
        # Ignore notifications from another programs
        if not arg[0] == self.id:
            return
        print arg

        if arg[1] == "default" and self.__default_action_func:
            self.__default_action_func(arg)
        elif self.__action_func[arg[1]][0]:
            self.__action_func[arg[1]][0](arg, self.__action_func[arg[1]][1])

    def _set_id(self, id):
        self.id = id

    def _notify_error(self, e):
        print >> stderr, str(e)

    def show(self):
        if self.__interface:
            self.__interface.Notify(self.title,
                self.__replaces_id,
                self.icon,
                self.summary,
                self.body,
                self.actions,
                self.hints,
                self.expire_timeout,
                reply_handler=self._set_id,
                error_handler=self._notify_error)
