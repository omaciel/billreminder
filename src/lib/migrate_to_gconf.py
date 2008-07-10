
# Tool to migrate to gconf

import gconf
import os
from ConfigParser import ConfigParser
from lib.common import GCONF_PATH, GCONF_GUI_PATH, GCONF_ALARM_PATH

def migrate(filename):
    gconf_client = gconf.client_get_default()
    old_config = ConfigParser()
    old_config.read(filename)

    alarm_values_bool = ('show_startup_notification',
         'use_alert_dialog',
         'show_before_alarm',
         'show_pay_notification',
         'show_alarm',
         'show_due_alarm')

    for name in alarm_values_bool:
        if old_config.has_option("Alarm", name):
            value = old_config.getboolean("Alarm", name)
            gconf_path = GCONF_ALARM_PATH + name
            gconf_client.set_bool(gconf_path, value)

    alarm_values_int = ('interval',
        'notification_days_limit',
        'show_alarm_before_days')

    for name in alarm_values_int:
        if old_config.has_option("Alarm", name):
            value = old_config.getint("Alarm", name)
            gconf_path = GCONF_ALARM_PATH + name
            gconf_client.set_int(gconf_path, value)


    gui_values_int = ('due_date',
        'show_paid_bills',
        'width', 'height',
        'x', 'y')

    for name in gui_values_int:
        if old_config.has_option("GUI", name):
            value = old_config.getint("GUI", name)
            gconf_path = GCONF_GUI_PATH + name
            gconf_client.set_int(gconf_path, value)

    gui_values_bool = ('show_menubar',
                       'show_toolbar')

    for name in gui_values_bool:
        if old_config.has_option("GUI", name):
            value = old_config.getboolean("GUI", name)
            gconf_path = GCONF_GUI_PATH + name
            gconf_client.set_bool(gconf_path, value)

    if old_config.has_option("General", "delay"):
        value = old_config.getint("General", "delay")
        gconf_path = GCONF_PATH + "delay"
        gconf_client.set_int(gconf_path, value)

    if old_config.has_option("General", "start_in_tray"):
        value = old_config.getboolean("General", "start_in_tray")
        gconf_path = GCONF_PATH + "start_in_tray"
        gconf_client.set_bool(gconf_path, value)

    if old_config.has_option("Alarm", "show_alarm_at_time"):
        value = old_config.get("Alarm", "show_alarm_at_time")
        gconf_path = GCONF_ALARM_PATH + "show_alarm_at_time"
        gconf_client.set_string(gconf_path, value)

    os.remove(filename)
