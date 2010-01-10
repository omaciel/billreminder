# -*- coding: utf-8 -*-

import os
import sys

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

    def __init__(self):
        data_dir = os.path.join(xdg_data_home, APPNAME)
        if not os.path.isdir(data_dir):
            os.mkdir(data_dir)

        self.engine = create_engine('sqlite:///%s' % os.path.join(data_dir, DB_NAME))
        self.Session = sessionmaker(bind=self.engine)

        # Creates all database tables
        Bill.metadata.create_all(self.engine)

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
                            category = session.query(Category).filter_by(name=dbobject.category.name).one()
                            bill.category = category
                        except Exception, e:
                            print "Failed to retrieve category \"%s\" for bill \"%s\": %s" \
                                % (dbobject.payee, dbobject.category.name, str(e))

                if session.dirty:
                    session.commit()

            except NoResultFound, e:
                session.add(dbobject)
                session.commit()

            except Exception, e:
                session.rollback()
                print str(e)
            finally:
                session.close()

        elif isinstance(dbobject, Category):
            try:
                category = session.query(Category).filter_by(id=dbobject.id).one()
                if category:
                    category.name = dbobject.name
                    category.color = dbobject.color

                if session.dirty:
                    session.commit()

            except NoResultFound, e:
                session.add(dbobject)
                session.commit()
            except Exception, e:
                session.rollback()
                print str(e)
            finally:
                session.close()

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
