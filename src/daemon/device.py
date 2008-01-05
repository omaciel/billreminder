#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['LogDevice', 'NullDevice', 'VerboseDevice']

import sys
import logging

from lib import common

class NullDevice (object):
    """ Disable sys.stdout and sys.stderr """
    def __init__(self):
        pass

    def write(self, string):
        """ Fake write """
        pass


class LogDevice (object):
    """ Redir sys.stdout and sys.stderr to log file """
    def __init__(self, type_='stdout'):
        self.type_ = type_
        if type_ == 'stdout':
            level_ = logging.INFO
        elif type_ == 'stderr':
            level_ = logging.ERROR
        logging.basicConfig(level=level_,
                format='%(asctime)s %(name)-12s %(levelname)-9s %(message)s',
                datefmt='%m-%d-%Y %H:%M',
                filename=common.DAEMON_LOG_FILE,
                filemode='a')
        self.log = logging.getLogger('billreminderd')
        pass

    def write(self, string):
        """ Write log message """
        if string == '\n':
            return
        if string.endswith('\n'):
            string = string[:(len(string) - 1)]
        if self.type_ == 'stdout':
            self.log.info(string)
        elif self.type_ == 'stderr':
            self.log.error(string)

class VerboseDevice (LogDevice):
    def __init__(self, type_='stdout'):
        LogDevice.__init__(self, type_)
        console = logging.StreamHandler()
        console.setFormatter(
                logging.Formatter('%(name)-12s %(levelname)-9s %(message)s'))
        if type_ == 'stdout':
            self.log.addHandler(console)
