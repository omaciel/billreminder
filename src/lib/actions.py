# -*- coding: utf-8 -*-

__all__ = ['Actions']

import sys

import dal
import time
import datetime
from db.entities import Bill, Category
from sqlalchemy.sql import func
from sqlalchemy.orm import eagerload, outerjoin
from lib import common, scheduler
from lib.utils import force_string
from lib.utils import verify_dbus_service

class Actions(object):

    def __init__(self, databaselayer=None):
        if not databaselayer:
            databaselayer = dal.DAL()

        self.dal = databaselayer

    def get_interval_bills(self, start, end, paid = None):
        """
        """

        records = []

        paid = bool(paid) if paid in (0,1) else None

        try:
            session = self.dal.Session()
            q = session.query(Bill).options(eagerload('category')).filter(Bill.dueDate >= start).filter(Bill.dueDate <= end)
            if paid != None:
                q = q.filter(Bill.paid == paid)
            records = q.order_by(Bill.dueDate.desc()).all()
        except Exception, e:
            print str(e)
            pass
        finally:
            session.close()

        return records

    def get_monthly_totals(self, start, end, paid=None):
        """
        Return a list of categories and totals for the given month
        """

        records = []

        try:
            session = self.dal.Session()
            # records is a tuple of Category.name and total as type Decimal
            q = session.query(Category.name, func.sum(Bill.amount)).select_from(outerjoin(Bill, Category)).filter(Bill.dueDate >= start).filter(Bill.dueDate <= end).group_by(Category.name)

            if paid:
                q = q.filter(Bill.paid == paid)

            records = q.all()
        except Exception, e:
            print str(e)
            pass
        finally:
            session.close()

        return records

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
            records = q.order_by(Bill.dueDate.desc()).all()
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
        return self.dal.add(dbobject)
        #return self.dal.edit(dbobject)

    def delete(self, dbobject):
        return self.dal.delete(dbobject)
