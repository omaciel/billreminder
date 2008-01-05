#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['Config']

import os
from ConfigParser import ConfigParser

from lib.common import CFG_NAME
from lib.common import USER_CFG_PATH
from lib.common import DEFAULT_CFG_PATH

class Config(ConfigParser):

    def __init__(self):
        defaults = {}
        ConfigParser.__init__(self, defaults)
        self.filename = os.path.join(USER_CFG_PATH, CFG_NAME)
        self.read([os.path.join(DEFAULT_CFG_PATH, CFG_NAME), self.filename])

    def reload(self):
        self.read([os.path.join(DEFAULT_CFG_PATH, CFG_NAME), self.filename])

    def save(self):
        file = open(self.filename, 'w')
        self.write(file)
        file.close()
