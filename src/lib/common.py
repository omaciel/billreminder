# -*- coding: utf-8 -*-

import os
import i18n

try:
    from defs import *
except:
    APPVERSION = "0.3.2"

datadir = "/usr/share"

# Application info
APPNAME = "BillReminder"
COPYRIGHTS = "%s - Copyright (c) 2006-2008\n" \
             "Og Maciel <ogmaciel@gnome.org>" % APPNAME
WEBSITE = "http://billreminder.gnulinuxbrasil.org/"
AUTHORS = [
    _('Developers:'),
    'Og Maciel <ogmaciel@gnome.com>',
    'Luiz Armesto <luiz.armesto@gmail.com>',
    '',
    _('Contributors:'),
    'Laudeci Oliveira <laudeci@gmail.com>',
    'Giovanni Deganni <tiefox@gmail.com>',
    'Ruivaldo <ruivaldo@gmail.com>',
    'Mario Danic <mario.danic@gmail.com>'
]

ARTISTS = [
    'Led Style <ledstyle@gmail.com>',
    'Vinicius Depizzol <vdepizzol@gmail.com>'
]


LICENSE = """
This application is distributed under the BSD
Licensing scheme.  An online version of the
license can be obtained from
http://www.opensource.org/licenses/bsd-license.html.

Copyright (c) 2006-2008 Og Maciel
All rights reserved.
"""

# Media path
if os.path.exists(os.path.abspath('../data/images/')):
    IMAGE_PATH = os.path.abspath('../data/images/')
else:
    IMAGE_PATH = '%s/billreminder/images' % datadir

# Images
APP_ICON = os.path.join(IMAGE_PATH, 'billreminder16.png')
TRAY_ICON = os.path.join(IMAGE_PATH, 'billreminder16.png')
APP_HEADER = os.path.join(IMAGE_PATH, 'header.png')

# Config info
CFG_NAME = 'billreminder.cfg'
USER_CFG_PATH =  os.path.expanduser('~/.config/billreminder/')
if os.path.exists(os.path.abspath('../data/')):
    DEFAULT_CFG_PATH = os.path.abspath('../data/')
else:
    DEFAULT_CFG_PATH = '%s/billreminder/' % datadir

# Database info
DB_NAME = 'billreminder.db'
DB_PATH =  os.path.expanduser('~/.config/billreminder/data/')

# DBus info
DBUS_INTERFACE = 'org.gnome.Billreminder.Daemon'
DBUS_PATH = '/org/gnome/Billreminder/Daemon'

# Notification info
NOTIFICATION_INTERFACE = 'org.freedesktop.Notifications'
NOTIFICATION_PATH = '/org/freedesktop/Notifications'

# Daemon files
DAEMON_LOCK_FILE = '/tmp/billreminderd.pid'
DAEMON_LOG_FILE = '/tmp/billreminderd.log'

#GConf info
GCONF_PATH = '/apps/billreminder/'
GCONF_ALARM_PATH = GCONF_PATH + 'alarm/'
GCONF_GUI_PATH = GCONF_PATH + 'gui/'
