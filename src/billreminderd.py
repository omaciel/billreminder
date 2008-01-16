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

from lib import i18n
from lib import common
from daemon import main as BillReminderd
from daemon.dbus_manager import verify_service


def main():
    help = _("""Usage:  billreminderd [OPTIONS...]

Options:
  --help, -h, -?\tShow this message.
  --verbose\t\tPrint output messages.
  --no-daemon\t\tDon't run as a daemon.
  --open-gui\t\tStart daemon and launch GUI.
  --stop\t\t\tStop daemon.
  --version, -v\t\tDisplays the version number for this application.
""")

    # Verify arguments
    args = sys.argv
    if '--help' in args or '-h' in args or '-?' in args:
        print help
        raise SystemExit
    elif '--stop' in args:
        import dbus
        import dbus.service
        if verify_service(common.DBUS_INTERFACE):
            session_bus = dbus.SessionBus()
            obj = session_bus.get_object(common.DBUS_INTERFACE,
                                         common.DBUS_PATH)
            dbus_interface = dbus.Interface(obj, common.DBUS_INTERFACE)
            dbus_interface.quit()
    elif '--version' in args or '-v' in args:
        print _('This is %(appname)s - Version: %(version)s') % \
                         {'appname': _("BillReminder Notifier"),
                          'version': common.APPVERSION}
    else:
        BillReminderd.main()

if __name__ == "__main__":
    main()
