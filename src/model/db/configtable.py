#!/usr/bin/python
# -*- coding: utf-8 -*-

__all__ = ['ConfigTable']

from generictable import GenericTable

class ConfigTable(GenericTable):
    """ Table to hold version information for all tables. """
    def __init__(self):
        GenericTable.__init__(self)
        self.Version = 1
        self.Key = "key"
        self.KeyAuto = False
        self.Name = "br_ConfigTable"
        self.CreateSQL = """
            CREATE TABLE %s (
            key  VARCHAR(255) NOT NULL,
            value VARCHAR(255) NOT NULL)
        """ % self.Name
        self.Fields = ['key', 'value']
