import unittest
import sys
import os

from decimal import Decimal

sys.path += [os.path.abspath('..')]

from lib import dal

class DALTest(unittest.TestCase):
    def setUp(self):
        from datetime import date
        from datetime import datetime

        self.dal = dal.DAL(fake=True)

        self.today = date.today()
        self.today_t = datetime.today()

    def test_add_category(self):
        category_orig = dal.Category('Groceries', 'c0c0c0')

        # Add category using DAL
        category_orig_id = self.dal.add(category_orig)

        session = self.dal.Session()
        category = session.query(dal.Category).filter(dal.Category.name=='Groceries').first()
        
        self.assertEqual(category.name, 'Groceries')
        self.assertEqual(category.color, 'c0c0c0')
        self.assertEqual(category.id, category_orig_id)

        session.close()

    def test_add_category_twice(self):
        category_orig_A = dal.Category('Groceries', 'c0c0c0')
        category_orig_A_id = self.dal.add(category_orig_A)

        category_orig_B = dal.Category('Groceries', 'c0c0c0')
        category_orig_B_id = self.dal.add(category_orig_A)

        self.assertEqual(category_orig_A_id, category_orig_B_id)

        session = self.dal.Session()
        self.assertEqual(session.query(dal.Category).filter(dal.Category.name=='Groceries').count(), 1)
        session.close()
    
    def test_add_simple_bill(self):
        bills_orig = dict()
        bills = dict()

        # Create a simple bill
        bills_orig['Harris Teeter'] = dal.Bill('Harris Teeter', Decimal('123.94'), self.today)
        
        # Add bill using DAL
        self.dal.add(bills_orig['Harris Teeter'])

        session = self.dal.Session()
        bills['Harris Teeter'] = session.query(dal.Bill).filter(dal.Bill.payee=='Harris Teeter').first()

        self.assertEqual(bills['Harris Teeter'].payee, 'Harris Teeter')
        self.assertEqual(bills['Harris Teeter'].amount, Decimal('123.94'))
        self.assertEqual(bills['Harris Teeter'].dueDate, self.today)
        self.assertEqual(bills['Harris Teeter'].alarmDate, None)
        self.assertEqual(bills['Harris Teeter'].notes, None)
        self.assertFalse(bills['Harris Teeter'].paid)
        self.assertEqual(bills['Harris Teeter'].repeats, None)
        self.assertEqual(bills['Harris Teeter'].category, None)

        session.close()    

    def test_add_bill_with_category(self):
        bills_orig = dict()
        bills = dict()

        category_orig = dal.Category('Groceries', 'c0c0c0')

        # Add category using DAL
        category_orig_id = self.dal.add(category_orig)

        session = self.dal.Session()
        category = session.query(dal.Category).filter(dal.Category.name=='Groceries').first()

        # Create a simple bill
        bills_orig['Harris Teeter'] = dal.Bill('Harris Teeter', Decimal('123.94'), self.today, category=dal.Category('Groceries', 'c0c0c0'))

        session.close()
        
        # Add bill using DAL
        self.assertEqual(self.dal.add(bills_orig['Harris Teeter']), 1)
        
        session = self.dal.Session()
        category = session.query(dal.Category).filter(dal.Category.name=='Groceries').first()
        bills['Harris Teeter'] = session.query(dal.Bill).filter(dal.Bill.payee=='Harris Teeter').first()
        
        self.assertEqual(bills['Harris Teeter'].payee, 'Harris Teeter')
        self.assertEqual(bills['Harris Teeter'].amount, Decimal('123.94'))
        self.assertEqual(bills['Harris Teeter'].dueDate, self.today)
        self.assertEqual(bills['Harris Teeter'].alarmDate, None)
        self.assertEqual(bills['Harris Teeter'].notes, None)
        self.assertFalse(bills['Harris Teeter'].paid)
        self.assertEqual(bills['Harris Teeter'].repeats, None)
        self.assertEqual(bills['Harris Teeter'].category.id, category_orig_id)

        session.close()

    def test_add_bill_with_new_category(self):
        bills_orig = dict()
        bills = dict()
        category_orig = dal.Category('Nothing', 'c0c0c0')

        # Create a simple bill
        bills_orig['Harris Teeter'] = dal.Bill('Harris Teeter', Decimal('123.94'), self.today, category=category_orig)
        
        # Add bill using DAL
        self.dal.add(bills_orig['Harris Teeter'])
        session = self.dal.Session()

        bills['Harris Teeter'] = session.query(dal.Bill).filter(dal.Bill.payee=='Harris Teeter').first()
        
        self.assertEqual(bills['Harris Teeter'].payee, 'Harris Teeter')
        self.assertEqual(bills['Harris Teeter'].amount, Decimal('123.94'))
        self.assertEqual(bills['Harris Teeter'].dueDate, self.today)
        self.assertEqual(bills['Harris Teeter'].alarmDate, None)
        self.assertEqual(bills['Harris Teeter'].notes, None)
        self.assertFalse(bills['Harris Teeter'].paid)
        self.assertEqual(bills['Harris Teeter'].repeats, None)
        self.assertEqual(bills['Harris Teeter'].category.id, 1)

        session.close()

