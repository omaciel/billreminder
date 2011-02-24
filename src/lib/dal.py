# -*- coding: utf-8 -*-

import os
import sys
import warnings

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, eagerload
    from sqlalchemy.orm.exc import NoResultFound
except ImportError:
    print "Please install SQLAlchemy!"
    raise SystemExit


from db.entities import Bill, Category

from lib.common import DB_NAME, APPNAME

from xdg.BaseDirectory import *

class DAL(object):

    def __init__(self, fake=False):

        new_setup = False

        # This is where the database file should live
        data_dir = os.path.join(xdg_data_home, APPNAME.lower())
        # Check that this is a new setup and there's no database yet.
        if not os.path.isdir(data_dir):
            # Create the directory where the database file will live
            os.mkdir(data_dir)
            # Safe to assume that this is a new setup.
            new_setup = True

        # The fake mode is used to run tests using a clean db created on memory
	if not fake:
            self.engine = create_engine('sqlite:///%s' % os.path.join(data_dir, DB_NAME))
        else:
            self.engine = create_engine('sqlite:///:memory:', echo=False)

        self.Session = sessionmaker(bind=self.engine)

        # Creates all database tables
        Bill.metadata.create_all(self.engine)

        # Let us make sure to create some default values.
        if new_setup:
            self.default_categories()

    def add(self, dbobject):

        session = self.Session()

        if isinstance(dbobject, Bill):
            try:
                bill = session.query(Bill).options(eagerload('category')).filter_by(id=dbobject.id).one()
                if bill:
                    bill.payee = dbobject.payee
                    bill.amount = dbobject.amount
                    bill.dueDate = dbobject.dueDate
                    bill.alarmDate = dbobject.alarmDate
                    bill.notes = dbobject.notes
                    bill.paid = dbobject.paid
                    
                    if dbobject.category:
                        try:
                            category = session.query(Category).filter(Category.name==dbobject.category.name).one()
                            bill.category = category
                        except NoResultFound, e:
                            warnings.warn("Failed to retrieve category \"%s\" for bill \"%s\". Creating category." \
	                        % (dbobject.category.name, dbobject.payee), RuntimeWarning)
                
                if session.dirty:
                    session.commit()

                dbobject_id = bill.id

            except NoResultFound, e:
                if dbobject.category:
                    try:
                        category = session.query(Category).filter(Category.name==dbobject.category.name).one()
                        del(dbobject.category)
                        dbobject.category = category
                    except NoResultFound, e:
                        warnings.warn("Failed to retrieve category \"%s\" for bill \"%s\". Creating category." \
	                    % (dbobject.category.name, dbobject.payee), RuntimeWarning)
                
                session.add(dbobject)
                session.commit()
                dbobject_id = dbobject.id

            except Exception, e:
                session.rollback()
                print str(e)
            finally:
                session.close()

        elif isinstance(dbobject, Category):
            try:
                category = session.query(Category).filter_by(name=dbobject.name).one()
                if category:
                    category.name = dbobject.name
                    category.color = dbobject.color

                if session.dirty:
                    session.commit()

                dbobject_id = category.id

            except NoResultFound, e:
                session.add(dbobject)
                session.commit()              
                dbobject_id = dbobject.id
            except Exception, e:
                session.rollback()
                print str(e)
            finally:
                session.close()

        return dbobject_id

    def edit(self, dbobject):

        session = self.Session()

        if session.dirty:
            try:
                session.commit()
            except Exception, e:
                session.rollback()
                print str(e)
            finally:
                session.close()

    def delete(self, dbobjects):
        if not isinstance(dbobjects, list):
            dbobjects = [dbobjects]

        session = self.Session()

        try:
            for dbo in dbobjects:
                session.delete(dbo)
            session.commit()
        except Exception, e:
            session.rollback()
            print str(e)
        finally:
            session.close()

    def default_categories(self):
        categories = [
                (_("Utilities"), '#f8bcffff0db4'),
                (_("Food & Dining"), '#cccc00000000'),
                (_("Mortgage"), '#4e4e9a9a0606'),
                (_("Rent"), '#c4c4a0a00000'),
                (_("Medical"), '#34346565a4a4'),
                (_("Educational"), '#757550507b7b'),
                (_("Donations"), '#060698209a9a'),
                (_("Credit Card"), '#d3d3d7d7cfcf'),
                (_("Gifts"), '#555557575353'),
                (_("Books"), '#efef29292929'),
                (_("Online Services"), '#8a8ae2e23434'),
                (_("Insurance"), '#fcfce9e94f4f'),
                (_("Auto & Transport"), '#72729f9fcfcf'),
                (_("Home"), '#adad7f7fa8a8'),
                (_("Gas & Fuel"), '#3434e2e2e2e2'),
                (_("Electronics"), '#eeeeeeeeecec'),
            ]

        for category in categories:
            self.add(Category(category[0], category[1]))
