# -*- coding: utf-8 -*-

__all__ = ['Actions']

import sys

import dal
import time
import datetime
from db.entities import Bill, Category
from sqlalchemy.orm import eagerload
from lib import common, scheduler
from lib.utils import force_string
from lib.utils import verify_dbus_service

class Actions(object):

    def __init__(self, databaselayer=None):
        if not databaselayer:
            databaselayer = dal.DAL()

        self.dal = databaselayer

    def get_interval_bills(self, status, start, end):
        """
        """

        records = []

        try:
            session = self.dal.Session()
            records = session.query(Bill).options(eagerload('category')).filter(Bill.dueDate >= start).filter(Bill.dueDate <= end).all()
        except Exception, e:
            print str(e)
            pass
        finally:
            session.close()

        return records

    def get_monthly_totals(self, status, month, year):
        """
        Return a list of categories and totals for the given month
        """

        records = 0.00

        firstOfMonth = scheduler.first_of_month(month, year)
        lastOfMonth = scheduler.last_of_month(month, year)

        try:
            session = self.dal.Session()
            # records is a tuple of type Decimal
            records = session.query(func.sum(Bill.amount)).filter(Bill.dueDate >= dt).filter(Bill.dueDate <= to).one()[0]
            records = float(records)
        except Exception, e:
            print str(e)
            pass
        finally:
            session.close()

        return records

    def get_monthly_bills(self, status, month, year):
        """
        Return a list of all bills for the given month with STATUS
        """

        records = []

        firstOfMonth = scheduler.first_of_month(month, year)
        lastOfMonth = scheduler.last_of_month(month, year)

        try:
            session = self.dal.Session()
            records = session.query(Bill).filter(Bill.dueDate >= firstOfMonth).filter(Bill.dueDate <= lastOfMonth).all()
        except Exception, e:
            print str(e)
        finally:
            session.close()

        return records

    def get_bills(self, kwargs):
        """
        Returns a list of all bills filtered by values.
        """
        records = []

        try:
            session = self.dal.Session()
            records = session.query(Bill).filter_by(**kwargs).all()
        except Exception, e:
            print str(e)
        finally:
            session.close()

        return records

