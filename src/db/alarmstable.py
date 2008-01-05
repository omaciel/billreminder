#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['AlarmsTable']

from generictable import GenericTable

class AlarmsTable(GenericTable):
    """ Table to hold information for all bills alarms. """
    Version = 2
    Key = "Id"
    KeyAuto = True
    Name = "br_AlarmsTable"
    CreateSQL = """
        CREATE TABLE %s (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            billId INTEGER,
            date INTEGER NOT NULL,
            type INTEGER DEFAULT 0,
            sound TEXT,
            text TEXT,
            enabled INTEGER DEFAULT 1)
    """ % Name
    Fields = ['Id', 'billId', 'date', 'type', 'sound', 'text', 'enabled']
