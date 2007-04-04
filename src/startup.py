#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

current_path = os.path.realpath(__file__)
basedir = os.path.dirname(os.path.realpath(__file__))
if not os.path.exists(os.path.join(basedir, "startup.py")):
    if os.path.exists(os.path.join(os.getcwd(), "startup.py")):
        basedir = os.getcwd()
sys.path.insert(0, basedir)
os.chdir(basedir)

try:
    import pygtk
    pygtk.require("2.0")
except ImportError:
    pass
try:
    import gtk
    from controller.maindialog import BillReminder
    from view.maindialog import BillReminderView
except ImportError:
    sys.exit(1)

if "--from_daemon" in sys.argv:
    from model.daemon import Daemon
    Daemon()

view = BillReminderView()
controller = BillReminder(view)
gtk.main()
