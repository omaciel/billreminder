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
    <one line to give the program's name and a brief idea of what it does.>
        Copyright (C) <year>  <name of author>
This file is part of BillReminder.
Copyright (C) 2006 - 2009 - Og Maciel <ogmaciel@gnome.org>.

BillReminder is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

BillReminder is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with BillReminder.  If not, see <http://www.gnu.org/licenses/>.
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
