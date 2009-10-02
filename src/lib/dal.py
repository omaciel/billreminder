# -*- coding: utf-8 -*-

import os
import sys

try:
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
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

    def add(self, dbobjects):
        if not isinstance(dbobjects, list):
            dbobjects = [dbobjects]

        session = self.Session()

        try:
            session.add_all(dbobjects)
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
