# -*- coding: utf-8 -*-

__all__ = ['Actions']

import sys

import dal
import bill
from lib import common
from lib.utils import force_string
from lib.utils import verify_dbus_service
from db.billstable import BillsTable
from db.categoriestable import CategoriesTable

class Actions(object):

    def __init__(self, databaselayer=None):
        if not databaselayer:
            databaselayer = dal.DAL()

        self.dal = databaselayer

    def get_bills(self, kwargs):
        """ Returns one or more records that meet the criteria passed """
        return self.dal.get(BillsTable, kwargs)

    def add_bill(self, kwargs):
        """ Adds a bill to the database """
        return self.dal.add(BillsTable, kwargs)

    def edit_bill(self, kwargs):
        """ Edit a record in the database """
        return self.dal.edit(BillsTable, kwargs)

    def delete_bill(self, key):
        """ Delete a record in the database """
        return self.dal.delete(BillsTable, key)

    def get_categories(self, kwargs):
        """ Returns one or more records that meet the criteria passed """
        return self.dal.get(CategoriesTable, kwargs)

    def add_category(self, kwargs):
        """ Adds a category to the database """
        return self.dal.add(CategoriesTable, kwargs)

    def edit_category(self, kwargs):
        """ Edit a record in the database """
        return self.dal.edit(CategoriesTable, kwargs)

    def delete_category(self, key):
        """ Delete a record in the database """
        return self.dal.delete(CategoriesTable, key)


if not '--standalone' in sys.argv \
   and not sys.argv[0].endswith('billreminderd') \
   and verify_dbus_service(common.DBUS_INTERFACE):
    from lib.dbus_actions import Actions

