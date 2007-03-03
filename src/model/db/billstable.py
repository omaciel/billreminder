#!/usr/bin/python
# -*- coding: utf-8 -*-

__all__ = ['BillsTable']

from generictable import GenericTable

class BillsTable(GenericTable):
    """ Table to hold information for all bills created. """
    def __init__(self):
        GenericTable.__init__(self)
        self.Version = 1
        self.Key = "Id"
        self.KeyAuto = True
        self.Name = "br_BillsTable"
        self.CreateSQL = """
            CREATE TABLE %s (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                payee TEXT NOT NULL,
                dueDate INTEGER NOT NULL,
                amountDue INTEGER NOT NULL,
                notes TEXT,
                paid INTEGER DEFAULT 0)
        """ % self.Name
        self.Fields = ['Id', 'payee', 'dueDate', 'amountDue', 'notes', 'paid']
