#!/usr/bin/python
# -*- coding: utf-8 -*-

__all__ = ['VersionsTable']

from generictable import GenericTable

class VersionsTable(GenericTable):
    """ Table to hold version information for all tables. """
    def __init__(self):
        GenericTable.__init__(self)
        self.Version = 1
        self.Key = "tablename"
        self.KeyAuto = False
        self.Name = "VersionsTable"
        self.CreateSQL = """
            CREATE TABLE %s (
            tablename   VARCHAR(255) NOT NULL,
            version INT NOT NULL)
        """ % self.Name
        self.Fields = ['tablename', 'version']
