# -*- coding: utf-8 -*-

__all__ = ['Actions']

import sys

import dal
import bill
import time
import datetime
from lib import common, scheduler
from lib.utils import force_string
from lib.utils import verify_dbus_service
from db.billstable import BillsTable
from db.categoriestable import CategoriesTable

class Actions(object):

    def __init__(self, databaselayer=None):
        if not databaselayer:
            databaselayer = dal.DAL()

        self.dal = databaselayer

    def get_monthly_totals(self, status, month, year):
        # Return a list of categories and totals for the given month
        # Delimeters for our search
        firstOfMonth = scheduler.first_of_month(month, year)
        lastOfMonth = scheduler.last_of_month(month, year)

        # Determine status criteria
        status = status < 2 and ' = %s' % status or ' in (0,1)'

        stmt = 'select categoryName, sum(amountDue) as amount, color' \
            ' from br_billstable, br_categoriestable where' \
            ' paid %s' \
            ' and dueDate >= ? and dueDate <= ?' \
            ' and br_categoriestable.Id = br_billstable.catId' \
            ' GROUP BY catId, color' \
            ' ORDER BY dueDate ASC' % status
        params = [firstOfMonth, lastOfMonth]
        records = self.dal.executeSql(stmt, params)

        return records

    def get_monthly_bills(self, status, month, year):
        # Delimeters for our search
        firstOfMonth = scheduler.first_of_month(month, year)
        lastOfMonth = scheduler.last_of_month(month, year)

        # Determine status criteria
        status = status < 2 and ' = %s' % status or ' in (0,1)'

        stmt = 'paid %s' \
            ' and dueDate >= %s and dueDate <= %s' \
            ' ORDER BY dueDate DESC' % (status, firstOfMonth, lastOfMonth)
        records = self.get_bills(stmt)

        return records

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
        bills = self.get_bills({'catId': key})
        for bill in bills:
            bill['catId'] = None
            self.edit_bill(bill)
        return self.dal.delete(CategoriesTable, key)

"""
if not '--standalone' in sys.argv \
   and not sys.argv[0].endswith('billreminderd') \
   and verify_dbus_service(common.DBUS_INTERFACE):
    from lib.dbus_actions import Actions
"""
