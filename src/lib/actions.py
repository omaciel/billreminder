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

    def get_interval_bills(self, start, end, paid=None):
        """
        """

        records = []

        paid = bool(paid) if (paid and paid < 2) else None

        try:
            session = self.dal.Session()
            q = session.query(Bill).options(eagerload('category')).filter(Bill.dueDate >= start).filter(Bill.dueDate <= end)
            if paid:
                q = q.filter(Bill.paid == paid)
            records = q.all()
        except Exception, e:
            print str(e)
            pass
        finally:
            session.close()

        return records

    def get_monthly_totals(self, month, year, paid=None):
        """
        Return a list of categories and totals for the given month
        """

        total = 0.00

        firstDay = scheduler.first_of_month(month, year)
        lastDay = scheduler.last_of_month(month, year)

        try:
            session = self.dal.Session()
            # records is a tuple of type Decimal
            q = session.query(func.sum(Bill.amount)).filter(Bill.dueDate >= dt).filter(Bill.dueDate <= to)
            if paid:
                q = q.filter(Bill.paid == paid)
            # Got anything back?
            if q.count():
                # Result is of type Decimal and needs to be converted.
                total = float(q.one()[0])
        except Exception, e:
            print str(e)
            pass
        finally:
            session.close()

        return total

    def get_monthly_bills(self, month, year, paid=None):
        """
        Return a list of all bills for the given month with paid
        """

        records = []

        firstDay = scheduler.first_of_month(month, year)
        lastDay = scheduler.last_of_month(month, year)

        try:
            session = self.dal.Session()
            q = session.query(Bill).filter(Bill.dueDate >= firstDay).filter(Bill.dueDate <= lastDay)
            if paid:
                q = q.filter(Bill.paid == paid)
            records = q.all()
        except Exception, e:
            print str(e)
        finally:
            session.close()

        return records

    def get_bills(self, **kwargs):
        """
        Returns a list of all bills filtered by values.
        """
        records = []

        try:
            session = self.dal.Session()
            records = session.query(Bill).options(eagerload('category')).filter_by(**kwargs).all()
        except Exception, e:
            print str(e)
        finally:
            session.close()

        return records

    def get_categories(self, **kwargs):
        """
        Returns a list of all categories filtered by values.
        """
        records = []

        try:
            session = self.dal.Session()
            records = session.query(Category).filter_by(**kwargs).all()
        except Exception, e:
            print str(e)
        finally:
            session.close()

        return records

    def add(self, dbobject):
        return self.dal.add(dbobject)

    def edit(self, dbobject):
        return self.dal.edit(dbobject)

    def delete(self, dbobject):
        return self.dal.delete(dbobject)
