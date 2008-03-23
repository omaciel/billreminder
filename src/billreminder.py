# -*- coding: utf-8 -*-

import sys
import os

current_path = os.path.realpath(__file__)
basedir = os.path.dirname(os.path.realpath(__file__))
if not os.path.exists(os.path.join(basedir, "billreminder.py")):
    if os.path.exists(os.path.join(os.getcwd(), "billreminder.py")):
        basedir = os.getcwd()
sys.path.insert(0, basedir)
os.chdir(basedir)



try:
    import pygtk
    pygtk.require("2.0")
except ImportError:
    print "Please install pygtk"
    raise SystemExit

try:
    import gtk
except ImportError:
    print "Please install gtk"
    raise SystemExit

from lib import dialogs
from lib import common
from lib import i18n
from gui.maindialog import MainDialog as BillReminder

def main():
    help = _("""Usage:  billreminder [OPTIONS...]

Options:
  --help, -h, -?\tShow this message.
  --about\t\tAbout this application.
  --add\t\t\tAdds a new record to the database.
  --standalone\t\tAccess database directly, without daemon.
  --version, -v\t\tDisplays the version number for this application.
""")

    # Verify arguments
    args = sys.argv
    if "--help" in args or "-h" in args  or "-?" in args:
        print help
    elif "--about" in args:
        dialogs.about_dialog()
    elif "--add" in args:
        print dialogs.add_dialog()
    elif "--version" in args or "-v" in args:
        print _("This is %(appname)s - Version: %(version)s") % \
                         {'appname': common.APPNAME,
                          'version': common.APPVERSION}
    else:
        gtk.gdk.threads_init()
        app = BillReminder()
        gtk.main()

if __name__ == "__main__":
    main()
