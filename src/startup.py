#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
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

view = BillReminderView()
controller = BillReminder(view)
gtk.main()
