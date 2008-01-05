#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['Daemon', 'Program', 'lock', 'unlock']

import os
import sys
from subprocess import Popen

try:
    import gobject
except ImportError:
    print 'Required package: pygobject'
    raise SystemExit
try:
    import dbus
except ImportError:
    print 'Required package: dbus-python'
    raise SystemExit
try:
    import pysqlite2
except ImportError:
    print 'Required package: pysqlite2'
    raise SystemExit

from lib import common
from lib import i18n
from lib.utils import verify_pid
from lib.actions import Actions
from lib.config import Config
from alarm import Alarm
from dbus_manager import Server
from dbus_manager import verify_service
from device import *

stdout_orig = sys.stdout
stderr_orig = sys.stderr

LOCKFD = None

def lock():
    """ Verify/Create Lock File """
    global LOCKFD

    try:
        LOCKFD = os.open(common.DAEMON_LOCK_FILE,
                         os.O_CREAT | os.O_EXCL | os.O_RDWR)
        os.write(LOCKFD, '%d' % os.getpid())
        return True
    except OSError:
        # Already locked
        return False

def unlock():
    """ Remove Lock File """
    global LOCKFD

    if not LOCKFD:
        return False
    try:
        os.close(LOCKFD)
        os.remove(common.DAEMON_LOCK_FILE)
        return True
    except OSError:
        return False


class Daemon(object):
    """ Make the program run like a daemon """
    def __init__(self):
        """ Detach process and run it as a daemon """
        if not '--no-daemon' in sys.argv:
            # Fork first child
            try:
                pid = os.fork()
            except OSError, err:
                print >> sys.stderr, \
                         ('Unexpected error:', sys.exc_info()[0], err)

            if pid == 0:
                os.setsid()

                # Fork second child
                try:
                    pid = os.fork()
                except OSError, err:
                    print >> sys.stderr, \
                             ('Unexpected error:', sys.exc_info()[0], err)

                if pid == 0:
                    os.umask(0)
                else:
                    raise SystemExit
            else:
                raise SystemExit
            # Redirect STDIN, STDOUT and STDERR
            sys.stdin.close()
        if '--verbose' in sys.argv:
            sys.stdout.write('\n')
            sys.stdout = VerboseDevice(type_='stdout')
            sys.stderr = VerboseDevice(type_='stderr')
        else:
            sys.stdout = LogDevice(type_='stdout')
            sys.stderr = LogDevice(type_='stderr')


class Program(Daemon):
    """ BillReminder Daemon Main class """

    def __init__(self):

        # Verify if Lock File exist and if there is another instance running
        if not lock():
            lockfd = open(common.DAEMON_LOCK_FILE, 'r')
            lockpid = int(lockfd.readline())
            lockfd.close()
            if verify_pid(lockpid):
                print _('Lock File found:' \
                        ' You have another instance running. (pid=%d)') % \
                        lockpid
                raise SystemExit
            else:
                print _('Lock File found: ' \
                        'Possibly the program was exited unexpectedly.')
                try:
                    print _('Removing Lock File...')
                    os.remove(common.DAEMON_LOCK_FILE)
                    print _('Successfully.')
                except OSError:
                    print _('Failed.')

        # Verify if there is another Billreminder-Daemon DBus Service
        if verify_service(common.DBUS_INTERFACE):
            print _('BillReminder Notifier is already running.')
            raise SystemExit

        Daemon.__init__(self)

        self.client_pid = None

        self.config = Config()
        self.actions = Actions()
        self.dbus_server = Server(self)
        if '--open-gui' in sys.argv:
            gui = Popen('billreminder', shell=True)
            self.client_pid = gui.pid
        self.alarm = Alarm(self)


        # Create the mainloop
        self.mainloop = gobject.MainLoop()
        self.mainloop.run()

    def __del__(self):
        try:
            unlock()
        except:
            pass

    def quit(self):
        """ Close program """
        self.mainloop.quit()
        unlock()

def main():
    gobject.threads_init()

    try:
        Program()
    except KeyboardInterrupt:
        unlock()
        print >> stdout_orig, 'Keyboard Interrupt (Ctrl+C)'
    except:
        unlock()
        raise SystemExit
