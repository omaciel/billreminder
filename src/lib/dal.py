# -*- coding: utf-8 -*-

__all__ = ['DAL']

import os
import sys

try:
    from pysqlite2 import dbapi2 as sqlite
except ImportError:
    print "Please install pysqlite2"
    sys.exit(1)

from lib.bill import Bill
from lib.common import DB_NAME, DB_PATH
from db.versionstable import VersionsTable
from db.fieldstable import FieldsTable
from db.billstable import BillsTable
from db.categoriestable import CategoriesTable

class DAL(object):

    # Maybe move dbName and dbPath to lib.common?
    # Database name and path
    dbName = DB_NAME
    dbPath = DB_PATH

    # Tables used by applications and corresponding versions
    tables = {'tblversions': VersionsTable(),
        'tblcategories': CategoriesTable(),
        'tblfields': FieldsTable(),
        'tblbills': BillsTable()}
    # Same dict, but with real table name
    _tables = dict([(tables[table].Name, tables[table]) for table in tables])

    def __init__(self):
        if not os.path.isdir(self.dbPath):
            os.makedirs(self.dbPath)

        self.conn = sqlite.connect(os.path.join(self.dbPath, self.dbName),
                                   isolation_level=None)
        self.cur = self.conn.cursor()
        self.cur.execute("PRAGMA count_changes=0")

        if os.path.isfile(os.path.join(self.dbPath, self.dbName)):
            self._validate_tables()
        else:
            self._createDb()

    def _createDb(self):
        """ All tables get created here."""
        # First, we create them
        for table in self.tables.values():
            self._create_table(table)

        # Now save their field info
        for table in self.tables.values():
            self._update_fields_information(table)

        # Now save their version info
        for table in self.tables.values():
            self._update_table_version(table)


    def _create_table(self, table):
        # Create the table
        self.cur.execute(table.CreateSQL)
        self.conn.commit()
        print table.Name

    def _update_fields_information(self, table):
        """ Adds field information for every table."""
        # Saves fields information for every table except tblfields
        self.add(self.tables['tblfields'],
                 {'tablename': table.Name,
                  'fields': ", ".join(table.Fields)})

    def _update_table_version(self, table):
        """ Adds table verison information."""
        # Save version information for every table
        self.add(self.tables['tblversions'],
                 {'tablename': table.Name,
                  'version': table.Version})
        print 'version saved (%s - %i)' % (table.Name, table.Version)

    def _validate_tables(self):
        """ Validates that all tables are up to date. """
        stmt = "select tbl_name from sqlite_master where " \
               "type = 'table' and tbl_name like 'br_%'"
        self.cur.execute(stmt)
        # List of all tables with names that start with "br_"
        tbllist = self.cur.fetchall()
        print tbllist

        # Create all tables if database is empty
        if len(tbllist) == 0:
            self._createDb()
            return True

        unvalidated = self._tables.copy()
        #unvalidated.pop(self.tables['tblversions'].Name)
        #unvalidated.pop(self.tables['tblfields'].Name)
        for tblname in tbllist:
            tblname = str(tblname[0])
            try:
                ver = self.get(VersionsTable,
                               {'tablename': tblname})[0]['version']
            except:
                ver = -1
            print ver
            # Table is obsolete and will be deleted
            if tblname not in self._tables:
                # We should revisit this logic
                print '%s is an obsolete table and it will be deleted' % \
                       tblname
                self._delete_table(tblname)
                continue
            if self._tables[tblname].Version == int(ver) :
                print '%s is a valid table' % tblname
            else:
                print '%s is NOT a valid table' % tblname
                self._update_table(self._tables[tblname])
                # Save tables version info
                self._update_table_version(self._tables[tblname])
                # Save tables fields info
                self._update_fields_information(self._tables[tblname])
            # Remove valid tables from dict
            unvalidated.pop(tblname)

        # Create tables new in actual version
        for table in unvalidated.values():
            self._create_table(table)
            # Save tables version info
            self._update_table_version(table)
            # Save tables fields info
            self._update_fields_information(table)

    def _delete_table(self, table):
        if isinstance(table, basestring):
            table_name = table
        else:
            table_name = table.Name
        stmt = "DROP TABLE %s" % table_name
        self.cur.execute(stmt)
        self.delete(self.tables['tblversions'],  table_name)
        print "Removed table %s" % table_name

    def _update_table(self, table):
        oldfields = self.get(self.tables['tblfields'],
                            {'tablename': table.Name})[0]['fields'].split(', ')

        stmt = "SELECT %(fields)s FROM %(name)s" \
            % dict(fields=", ".join(oldfields), name=table.Name)
        print stmt
        self.cur.execute(stmt)
        oldrecords = [dict([ (f, row[i]) for i, f in enumerate(oldfields) ]) \
                      for row in self.cur.fetchall()]

        stmt = "ALTER TABLE %s RENAME TO %s_old" % (table.Name, table.Name)
        self.cur.execute(stmt)
        self.delete(self.tables['tblversions'],  table.Name)
        self.delete(self.tables['tblfields'], table.Name)
        self._create_table(table)

        for rec in oldrecords:
            print self.add(table, dict([(col,rec.get(col,'')) \
                                  for col in table.Fields]))

        self._delete_table('%s_old' % table.Name)

    def _create_query_params(self, kwargs):
        """ Helper method to create a statement and arguments to a query. """
        if None == kwargs or 0 == len(kwargs):
            return ("", [])

        if not isinstance(kwargs, basestring):
            pairs = kwargs.items()
            stmt = " WHERE " + \
                " AND ".join([ x[0] + (None is x[1] and " IS NULL" or " = ?")
                    for x in pairs ])

            args = [x[1] for x in filter(lambda x: None is not x[1], pairs)]
        else:
            stmt = " WHERE " + kwargs
            args = []
        return (stmt, args)

    def edit(self, table, kwargs):
        """ Edit a record in the database """
        # Removes the key field
        key = kwargs[table.Key]
        if table.KeyAuto:
            del kwargs[table.Key]

        # Split up into pairs
        pairs = kwargs.items()

        params = "=?, ".join([ x[0] for x in pairs ]) + "=?"
        stmt = "UPDATE %s SET %s WHERE %s=?" \
            % (table.Name, params, table.Key)

        params = [x[1] for x in pairs] + [key]

        return self._executeSQL(stmt, params)

    def delete(self, table, key):
        """ Delete a record in the database """
        # Delete statement
        stmt = "DELETE FROM %s WHERE %s=?" % (table.Name, table.Key)

        try:
            self._executeSQL(stmt, [key])
            return True
        except Exception, e:
            # Dump error to the screen; may be helpfull when debugging
            print str(e)
            return False

    def add(self, table, kwargs):
        """ Adds a record to the database """

        if table.KeyAuto:
            kwargs.pop(table.Key)
        # Separate columns and values
        values = kwargs.values()
        cols = kwargs.keys()
        # Insert statement
        stmt = "INSERT INTO %s (%s) VALUES (%s)" %\
            (table.Name, ",".join(cols), ",".join('?' * len(values)))
        print stmt
        self.cur.execute(stmt, values)
        b_key = self.cur.lastrowid
        if b_key:
            rows = self.get(table, {table.Key: b_key})
            try: return rows[0]
            except: None

    def get(self, table, kwargs):
        """ Returns one or more records that meet the criteria passed """
        (stmt, args) = self._create_query_params(kwargs)

        stmt = "SELECT %(fields)s FROM %(name)s" \
            % dict(fields=", ".join(table.Fields), name=table.Name) + stmt
        try:
            self.cur.execute(stmt, args)
        except sqlite.OperationalError:
            return None


        rows = [dict([(f, row[i]) for i, f in enumerate(table.Fields)]) \
                for row in self.cur.fetchall()]

        return rows

    def _executeSQL(self, stmt, args):
        """ Excutes passed SQL and returns the result """
        try:
            return self.cur.execute(stmt, args)
        except Exception, e:
            print "Unexpected error:", sys.exc_info()[0], e
            return None
