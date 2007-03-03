#!/usr/bin/python
# -*- coding: utf-8 -*-

__all__ = ['FieldsTable']

from generictable import GenericTable

class FieldsTable(GenericTable):
    """ Table to hold version information for all tables. """
    def __init__(self):
        GenericTable.__init__(self)
        self.Version = 1
        self.Key = "tablename"
        self.KeyAuto = False
        self.Name = "FieldsTable"
        self.CreateSQL = """
            CREATE TABLE %s (
            tablename   VARCHAR(255) NOT NULL,
            fields INT NOT NULL)
        """ % self.Name
        self.Fields = ['tablename', 'fields']
