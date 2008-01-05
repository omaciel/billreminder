#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['FieldsTable']

from generictable import GenericTable

class FieldsTable(GenericTable):
    """ Table to hold version information for all tables. """
    Version = 1
    Key = "tablename"
    KeyAuto = False
    Name = "br_FieldsTable"
    CreateSQL = """
        CREATE TABLE %s (
        tablename   VARCHAR(255) NOT NULL,
        fields INT NOT NULL)
    """ % Name
    Fields = ['tablename', 'fields']
