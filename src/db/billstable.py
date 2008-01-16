# -*- coding: utf-8 -*-

__all__ = ['BillsTable']

from generictable import GenericTable

class BillsTable(GenericTable):
    """ Table to hold information for all bills created. """
    Version = 3
    Key = "Id"
    KeyAuto = True
    Name = "br_BillsTable"
    CreateSQL = """
        CREATE TABLE %s (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            catId INTEGER,
            payee TEXT NOT NULL,
            dueDate INTEGER NOT NULL,
            amountDue INTEGER NOT NULL,
            notes TEXT,
            paid INTEGER DEFAULT 0,
            alarm INTEGER)
    """ % Name
    Fields = ['Id', 'catId', 'payee', 'dueDate', 'amountDue', 'notes', 'paid', 'alarm']
