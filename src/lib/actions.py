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

    def default_categories(self):
        categories = [
                ("Utilities", '#f8bcffff0db4'),
                ("Food & Dining", '#cccc00000000'),
                ("Mortgage", '#4e4e9a9a0606'),
                ("Rent", '#c4c4a0a00000'),
                ("Medical", '#34346565a4a4'),
                ("Educational", '#757550507b7b'),
                ("Donation", '#060698209a9a'),
                ("Credit Card", '#d3d3d7d7cfcf'),
                ("Gifts", '#555557575353'),
                ("Books", '#efef29292929'),
                ("Online Services", '#8a8ae2e23434'),
                ("Insurance", '#fcfce9e94f4f'),
                ("Auto & Transport", '#72729f9fcfcf'),
                ("Home", '#adad7f7fa8a8'),
                ("Gas & Fuel", '#3434e2e2e2e2'),
                ("Electronics", '#eeeeeeeeecec'),
            ]

        for category in categories:
            self.add(Category(category[0], category[1]))

    def get_interval_bills(self, start=None, end=None, paid=None):
        """
        """

        records = []

        paid = bool(paid) if paid in (0,1) else None

        try:
            session = self.dal.Session()
            q = session.query(Bill).options(eagerload('category'))
            if start:
                q = q.filter(Bill.dueDate >= start)
            if end:
                q = q.filter(Bill.dueDate <= end)
            if paid is not None:
                q = q.filter(Bill.paid == paid)
            records = q.order_by(Bill.dueDate.desc()).all()
        except Exception, e:
            print str(e)
            pass
        finally:
            session.close()

        return records

    def get_alarm_bills(self, start=None, end=None, paid=None):
        """
        """

        records = []

        paid = bool(paid) if paid in (0,1) else None

        try:
            session = self.dal.Session()
            q = session.query(Bill).options(eagerload('category'))
            if start:
                q = q.filter(Bill.alarmDate >= start)
            if end:
                q = q.filter(Bill.alarmDate <= end)
            if paid is not None:
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

        paid = bool(paid) if paid in (0,1) else None

        try:
            session = self.dal.Session()
            # records is a tuple of Category.name and total as type Decimal
            q = session.query(Category.name, func.sum(Bill.amount)).select_from(outerjoin(Bill, Category)).filter(Bill.dueDate >= start).filter(Bill.dueDate <= end).group_by(Category.name)
            if paid is not None:
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

    def delete(self, dbobject):
        return self.dal.delete(dbobject)
