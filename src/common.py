#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

DEFAULT_PATH = '/usr/share/billreminder/'
#DEFAULT_PATH ='../gui/'
#Main window constants
MAINGLADEFILE = os.path.join(DEFAULT_PATH, 'maindialog.glade')
MAINFORM_NAME = 'frmMain'

# Bills Dialog constants
BILLGLADEFILE = os.path.join(DEFAULT_PATH, 'billdialog.glade')
BILLDIALOG_NAME = 'frmBillDialog'

# About Dialog constants
ABOUTGLADEFILE = os.path.join(DEFAULT_PATH, 'aboutdialog.glade')
ABOUTDIALOG_NAME = 'frmAboutDialog'

#systray status menu
TRAYGLADEFILE = os.path.join(DEFAULT_PATH, 'systraymenu.glade')
TRAY_NAME = 'TrayMenu'

#media path
IMAGE_PATH = os.path.join(DEFAULT_PATH, 'pixmaps/')
APP_ICON = os.path.join(IMAGE_PATH, 'billreminder.png')
APP_HEADER = os.path.join(IMAGE_PATH, 'header.png')
