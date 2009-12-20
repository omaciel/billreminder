# -*- coding: utf-8 -*-

import gconf

#GConf info
GCONF_PATH = '/apps/billreminder/'
GCONF_ALARM_PATH = GCONF_PATH + 'alarm/'
GCONF_GUI_PATH = GCONF_PATH + 'gui/'

START_DELAY = 1
STARTUP_NOTIFY = True
INTERVAL = 60
DAYS_LIMIT = 15
SHOW_ALARM = True
SHOW_DUE_ALARM = True
ALERT_TIME = "13:00"
SHOW_BEFORE_ALARM = True
ALARM_BEFORE_DAYS = 3
USE_DIALOG = False

class Configuration(object):

    def __init__(self):
        self.client = gconf.client_get_default()

    def start_delay(self):
        start_delay = self.client.get_int(GCONF_PATH + 'delay') or START_DELAY
        start_delay= start_delay * 60000

        return start_delay

    def show_startup_notifications(self):
        showStartup = self.client.get_bool(GCONF_ALARM_PATH + 'show_startup_notification') or STARTUP_NOTIFY

        return showStartup

    def get_interval(self):
        interval = self.client.get_int(GCONF_ALARM_PATH + 'interval') or INTERVAL

        return interval * 1000

    def notification_days_limit(self):
        limit = self.client.get_int(GCONF_ALARM_PATH + 'notification_days_limit') or DAYS_LIMIT

        return limit

    def show_due_alarm(self):
        showDueAlarm = self.client.get_bool(GCONF_ALARM_PATH + 'show_due_alarm') or SHOW_DUE_ALARM

        return showDueAlarm

    def use_alert_dialog(self):
        use_dialog = self.client.get_bool(GCONF_ALARM_PATH + 'use_alert_dialog') or USE_DIALOG

        return use_dialog

    def show_alarm(self):
        showalarm = self.client.'show_alarm') or SHOW_ALARM

        return showalarm

    def show_before_alarm(self):
        beforeAlarm = self.client.get_bool(GCONF_ALARM_PATH + 'show_before_alarm') or SHOW_BEFORE_ALARM

        return beforeAlarm

    def show_alarm_at_time(self):
        alertTime = self.client.get_string(GCONF_ALARM_PATH +'show_alarm_at_time') or ALERT_TIME

        return alertTime.split(':')

    def show_alarm_before_days(self):
        days = self.client.get_int(GCONF_ALARM_PATH + 'show_alarm_before_days') or ALARM_BEFORE_DAYS

        return days

    def get_window_width(self):
        width = self.client.get_int(GCONF_GUI_PATH + 'width') or 500

        return width

    def get_window_height(self):
        height = self.client.get_int(GCONF_GUI_PATH + 'height') or 300

        return height

    def get_window_x(self):
        x = self.client.get_int(GCONF_GUI_PATH + 'x') or 0

        return x

    def get_window_y(self):
        y = self.client.get_int(GCONF_GUI_PATH + 'y') or 0

        return y

    def start_in_tray(self):
        return self.client.get_bool(GCONF_PATH + 'start_in_tray') or False

    def show_paid_bills(self):
        return self.client.get_int(GCONF_GUI_PATH + 'show_paid_bills') or 2

    def show_toolbar(self):
        return self.client.get_bool(GCONF_GUI_PATH + 'show_toolbar') or False
