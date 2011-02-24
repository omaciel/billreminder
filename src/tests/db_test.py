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
        bills_orig['Food Market'] = entities.Bill('Food Market', 123.94, self.today)

        session = self.Session()
        session.add(bills_orig['Food Market'])
        session.commit()

        bills['Food Market'] = session.query(entities.Bill).filter(entities.Bill.payee=='Food Market').first()

        self.assertEqual(bills['Food Market'].payee, 'Food Market')
        self.assertEqual(bills['Food Market'].amount, Decimal('123.94'))
        self.assertEqual(bills['Food Market'].dueDate, self.today)
        self.assertEqual(bills['Food Market'].alarmDate, None)
        self.assertEqual(bills['Food Market'].notes, None)
        self.assertFalse(bills['Food Market'].paid)
        self.assertEqual(bills['Food Market'].repeats, None)
        self.assertEqual(bills['Food Market'].category, None)

        # Create a complete bill
        bills_orig['Car'] = entities.Bill('Car', 3900.00, self.today, self.today_t, 'My new car', True, True)

        session = self.Session()
        session.add(bills_orig['Car'])
        session.commit()

        bills['Car'] = session.query(entities.Bill).filter(entities.Bill.payee=='Car').first()

        self.assertEqual(bills['Car'].payee, 'Car')
        self.assertEqual(bills['Car'].amount, Decimal('3900.00'))
        self.assertEqual(bills['Car'].dueDate, self.today)
        self.assertEqual(bills['Car'].alarmDate, self.today_t)
        self.assertEqual(bills['Car'].notes, 'My new car')
        self.assertTrue(bills['Car'].paid)
        self.assertTrue(bills['Car'].repeats)
        self.assertEqual(bills['Car'].category, None)

        session.close()

    def test_add_category_to_bill(self):
        categories = dict()
        bills = dict()

        # Create bills and category to be tested
        bills['Food Market'] = entities.Bill('Food Market', 123.94, self.today)
        bills['Car'] = entities.Bill('Car', 3900.00, self.today, self.today, 'My new car', True, True)
        categories['Miscellaneous'] = entities.Category('Miscellaneous', 'c0c0c0')        

        # Verify that there is no relations between bills and category yet
        self.assertEqual(categories['Miscellaneous'].bills, [])
        self.assertEqual(bills['Food Market'].category, None)
        self.assertEqual(bills['Car'].category, None)

        # Set cotegory for one bill
        bills['Food Market'].category = categories['Miscellaneous']        
        self.assertEqual(categories['Miscellaneous'].bills, [bills['Food Market']])
        self.assertEqual(bills['Food Market'].category, categories['Miscellaneous'])

        # Verify that the other bill remains with no category
        self.assertEqual(bills['Car'].category, None)

        # Append the other bill to the category using another method
        categories['Miscellaneous'].bills.append(bills['Car'])
        self.assertEqual(categories['Miscellaneous'].bills, [bills['Food Market'], bills['Car']])
        self.assertEqual(bills['Car'].category, categories['Miscellaneous'])

