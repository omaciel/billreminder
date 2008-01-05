#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['VersionsTable']

from generictable import GenericTable

class VersionsTable(GenericTable):
    """ Table to hold version information for all tables. """
    Version = 1
    Key = "tablename"
    KeyAuto = False
    Name = "br_VersionsTable"
    CreateSQL = """
        CREATE TABLE %s (
        tablename   VARCHAR(255) NOT NULL,
        version INT NOT NULL)
    """ % Name
    Fields = ['tablename', 'version']
