#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['CategoriesTable']

from generictable import GenericTable

class CategoriesTable(GenericTable):
    """ Table to hold bill category information. """
    Version = 2
    Key = "id"
    KeyAuto = False
    Name = "br_CategoriesTable"
    CreateSQL = """
        CREATE TABLE %s (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        categoryname VARCHAR(50) NOT NULL,
        color VARCHAR(14) NOT NULL)
    """ % Name
    Fields = ['id', 'categoryname', 'color']

