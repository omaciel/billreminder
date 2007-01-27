#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
try:
    import pygtk
    pygtk.require("2.0")
except:
      pass
try:
    import gtk
    from maindialog import BillReminder
except:
    sys.exit(1)

br = BillReminder()
gtk.main()
