#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

current_path = os.path.realpath(__file__)
basedir = os.path.dirname(os.path.realpath(__file__))
if not os.path.exists(os.path.join(basedir, "notifier.py")):
    if os.path.exists(os.path.join(os.getcwd(), "notifier.py")):
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
    from controller.daemon import Daemon
except ImportError:
    sys.exit(1)
import os
import gobject
import dbus

args = sys.argv

if "--help" in args  or "-?" in args:
    print("""Usage:
  billreminder-notifier [OPTIONS...]

Options:
  --help, -?\t\tShow this message
  --stop\t\tStop the daemon that is running
    """)
elif "--stop" in args:
    try:
        session_bus = dbus.SessionBus()
        obj = session_bus.get_object("org.gnome.Billreminder.Daemon", "/org/gnome/Billreminder/Daemon")
        interface = dbus.Interface(obj, "org.gnome.Billreminder.Daemon")
        print "Stopping BillReminder Daemon..."
        interface.quit()
    except:
        print "No BillReminder Daemon is running."
else:
    Daemon()
