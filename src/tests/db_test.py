import unittest
import sys
import os

from decimal import Decimal

sys.path += [os.path.abspath('..')]

from db import entities

class EntitiesTest(unittest.TestCase):
    def setUp(self):
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from datetime import date
        from datetime import datetime

        # Create a temporary database
        self.engine = create_engine('sqlite:///:memory:', echo=False)
        self.Session = sessionmaker(bind=self.engine)

        # Creates all database tables
        entities.Bill.metadata.create_all(self.engine)
        entities.Category.metadata.create_all(self.engine)
        
        self.today = date.today()
        self.today_t = datetime.today()

    def test_create_a_new_category(self):
        category_orig = entities.Category('Groceries', 'c0c0c0')

        session = self.Session()
        session.add(category_orig)
        session.commit()

        category = session.query(entities.Category).filter(entities.Category.name=='Groceries').first()

        self.assertEqual(category.name, 'Groceries')
        self.assertEqual(category.color, 'c0c0c0')

        session.close()

    def test_create_a_new_bill(self):
        bills_orig = dict()
        bills = dict()

        # Create a simple bill
        bills_orig['Harris Teeter'] = entities.Bill('Harris Teeter', 123.94, self.today)

        session = self.Session()
        session.add(bills_orig['Harris Teeter'])
        session.commit()

        bills['Harris Teeter'] = session.query(entities.Bill).filter(entities.Bill.payee=='Harris Teeter').first()

        self.assertEqual(bills['Harris Teeter'].payee, 'Harris Teeter')
        self.assertEqual(bills['Harris Teeter'].amount, Decimal('123.94'))
        self.assertEqual(bills['Harris Teeter'].dueDate, self.today)
        self.assertEqual(bills['Harris Teeter'].alarmDate, None)
        self.assertEqual(bills['Harris Teeter'].notes, None)
        self.assertFalse(bills['Harris Teeter'].paid)
        self.assertEqual(bills['Harris Teeter'].repeats, None)
        self.assertEqual(bills['Harris Teeter'].category, None)

        # Create a complete bill
        bills_orig['Toyota'] = entities.Bill('Toyota', 3900.00, self.today, self.today_t, 'My new car', True, True)

        session = self.Session()
        session.add(bills_orig['Toyota'])
        session.commit()

        bills['Toyota'] = session.query(entities.Bill).filter(entities.Bill.payee=='Toyota').first()

        self.assertEqual(bills['Toyota'].payee, 'Toyota')
        self.assertEqual(bills['Toyota'].amount, Decimal('3900.00'))
        self.assertEqual(bills['Toyota'].dueDate, self.today)
        self.assertEqual(bills['Toyota'].alarmDate, self.today_t)
        self.assertEqual(bills['Toyota'].notes, 'My new car')
        self.assertTrue(bills['Toyota'].paid)
        self.assertTrue(bills['Toyota'].repeats)
        self.assertEqual(bills['Toyota'].category, None)

        session.close()

    def test_add_category_to_bill(self):
        categories = dict()
        bills = dict()

        # Create bills and category to be tested
        bills['Harris Teeter'] = entities.Bill('Harris Teeter', 123.94, self.today)
        bills['Toyota'] = entities.Bill('Toyota', 3900.00, self.today, self.today, 'My new car', True, True)
        categories['Miscellaneous'] = entities.Category('Miscellaneous', 'c0c0c0')        

        # Verify that there is no relations between bills and category yet
        self.assertEqual(categories['Miscellaneous'].bills, [])
        self.assertEqual(bills['Harris Teeter'].category, None)
        self.assertEqual(bills['Toyota'].category, None)

        # Set cotegory for one bill
        bills['Harris Teeter'].category = categories['Miscellaneous']        
        self.assertEqual(categories['Miscellaneous'].bills, [bills['Harris Teeter']])
        self.assertEqual(bills['Harris Teeter'].category, categories['Miscellaneous'])

        # Verify that the other bill remains with no category
        self.assertEqual(bills['Toyota'].category, None)

        # Append the other bill to the category using another method
        categories['Miscellaneous'].bills.append(bills['Toyota'])
        self.assertEqual(categories['Miscellaneous'].bills, [bills['Harris Teeter'], bills['Toyota']])
        self.assertEqual(bills['Toyota'].category, categories['Miscellaneous'])

