# -*- coding: utf-8 -*-

import sys
import os
from optparse import OptionParser

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
    parser = OptionParser()
    parser.set_usage(_("Usage:  billreminder [OPTIONS...]"))
    parser.add_option('--version', action='store_true', dest='app_version', default=False, help=_('Displays the version number for this application.'))
    parser.add_option('--verbose', action='store_true', dest='app_verbose', default=False, help=_('Print output messages.'))
    parser.add_option('--no-daemon', action='store_true', dest='app_nodaemon', default=False, help=_("Don't run as a daemon."))
    parser.add_option('--open-gui', action='store_true', dest='app_opengui', default=False, help=_('Start daemon and launch GUI.'))
    parser.add_option('--stop', action='store_true', dest='app_stop', default=False, help=_('Stop daemon.'))

    # Verify arguments
    options, args = parser.parse_args()
    if options.app_stop:
        import dbus
        import dbus.service
        if verify_service(common.DBUS_INTERFACE):
            session_bus = dbus.SessionBus()
            obj = session_bus.get_object(common.DBUS_INTERFACE,
                                         common.DBUS_PATH)
            dbus_interface = dbus.Interface(obj, common.DBUS_INTERFACE)
            dbus_interface.quit()
    elif options.app_version:
        print _('This is %(appname)s - Version: %(version)s') % \
                         {'appname': _("BillReminder Notifier"),
                          'version': common.APPVERSION}
    else:
        BillReminderd.main()

if __name__ == "__main__":
    main()
