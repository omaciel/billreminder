#!/usr/bin/python
# -*- coding: utf-8 -*-

__all__ = ['Daemon']

import sys
import os

from model.dal import DAL
from model.config import Config

class NullDevice:
    def write(self, s):
        pass

class Daemon:
    
    config = None
    dbus_service = None
    
    def __init__(self):
        """ Detach a process and run it as a daemon """
        # Fork first child
        try: pid = os.fork()
        except Exception, e:
            print "Unexpected error:", sys.exc_info()[0], e
        
        if pid == 0: 
            os.setsid()
            
            # Fork second child
            try: 
                pid = os.fork()
            except Exception, e:
                print "Unexpected error:", sys.exc_info()[0], e
            
            if pid == 0: 
                os.chdir('.')
                os.umask(0)
            else:
                os._exit(0)
        else:
            os._exit(0)
        # Redirect STDIN, STDOUT and STDERR  
        # TODO: Create a log system
        sys.stdin.close()
        sys.stdout = NullDevice()
        sys.stderr = NullDevice()
        self.dal = DAL()
        self.config = Config()
        
