#!/usr/bin/python
#
# The MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of 
# this software and associated documentation files (the "Software"), to deal in the 
# Software without restriction, including without limitation the rights to use, copy, 
# modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
# and to permit persons to whom the Software is furnished to do so, subject to the 
# following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# BillReminder - Copyright (c) 2006, 2007 Og Maciel
#
# -*- coding: utf-8 -*-

DEFAULT_PATH = '/usr/share/billreminder/'
#Main window constants
MAINGLADEFILE = DEFAULT_PATH + 'maindialog.glade'
MAINFORM_NAME = 'frmMain'

# Bills Dialog constants
BILLGLADEFILE = DEFAULT_PATH + 'billdialog.glade'
BILLDIALOG_NAME = 'frmBillDialog'

# About Dialog constants
ABOUTGLADEFILE = DEFAULT_PATH + 'aboutdialog.glade'
ABOUTDIALOG_NAME = 'frmAboutDialog'

#systray status menu
TRAYGLADEFILE = DEFAULT_PATH + 'systraymenu.glade'
TRAY_NAME = 'TrayMenu'

#media path
IMAGE_PATH = DEFAULT_PATH + 'pixmaps/'
APP_ICON = IMAGE_PATH + 'billreminder.ico'
APP_HEADER = IMAGE_PATH + 'header.jpg'
