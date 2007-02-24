#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
from pysqlite2 import dbapi2 as sqlite
from bill import Bill

class DAL(object):

    # Database name and path
    dbName = 'billreminder.db'
    dbPath = '%s/.config/billreminder/data/' % os.environ['HOME']

    # Tables used by applications and corrsponding versions
    tables = {'tblversions': VersionsTable(),
              'tblbills': BillsTable()}

    def __init__(self):

        if not os.path.isdir(self.dbPath):
            os.makedirs(self.dbPath)

        if os.path.isfile (os.path.join(self.dbPath, self.dbName)) :
            self.conn = sqlite.connect(os.path.join(self.dbPath, self.dbName), isolation_level=None)
            self.cur = self.conn.cursor ()
        else :
            self.conn = sqlite.connect (os.path.join(self.dbPath, self.dbName), isolation_level=None)
            self.cur = self.conn.cursor ()

            self.cur.execute (self.createSQL)
            self.conn.commit()

    def validateTables(self):
        """ Validates that all tables are up to date. """
        stmt = "select tbl_name from sqlite_master where type = 'table' and tbl_name like 'br_%'"
        self.cur.execute(stmt)
        
    def _makeBillDict(self, bill):
        billDict = {}
        billDict['payee'] = bill.Payee
        billDict['dueDate'] = bill.DueDate
        billDict['amountDue'] = bill.AmountDue
        billDict['notes'] = bill.Notes

        return billDict

    def add(self, record, kwargs):
        """ Adds a record to the database """
        # Separate columns and values
        values = kwargs.values()
        cols = kwargs.keys()

        # Insert statement
        stmt = "INSERT INTO %s (%s) VALUES (%s)" %\
            (self.name, ",".join(cols), ",".join('?' * len(values)))

        self.cur.execute(stmt, values)
        b_id = self.cur.lastrowid

        if b_id:
            rows = self.get({'Id': b_id})
            return rows[0]

    def delete(self,b_id):
        # Delete statement

        stmt = "DELETE FROM %s WHERE Id=?" % (self.name)

        rowsAffected = self._executeSQL(stmt, [b_id])
        
        return rowsAffected

    def edit(self, id, bill):
        # Removes the Id field
        dic = bill.Dictionary
        del dic['Id']
        # Split up into pais
        pairs = dic.items()

        params = "=?, ".join([ x[0] for x in pairs ]) + "=?"
        stmt = "UPDATE %s SET %s WHERE %s=?" % (self.name, params, self.key)

        args = [ x[1] for x in pairs ] + [id]

        rowsAffected = self._executeSQL(stmt, args)
        return rowsAffected.rowcount

    def get(self, kwargs):
        """ Returns one or more records that meet the criteria passed """
        bills = []

        (stmt, args) = self._createQueryParams(kwargs)

        stmt = "SELECT %(fields)s FROM %(name)s" \
            % dict(fields=", ".join(self.fields), name=self.name) + stmt
        self.cur.execute(stmt, args)

        rows = [dict([ (f, row[i]) for i, f in enumerate(self.fields) ]) \
            for row in self.cur.fetchall()]
        #rows = self.cur.fetchall()
        for row in rows:
            b = Bill(row['payee'].encode("utf-8"), row['dueDate'], row['amountDue'], row['notes'], row['paid'], row['Id'])
            bills.append(b)


        return bills

    def Payees(self):
        """ Returns a list of distinct payees """
        stmt = "SELECT DISTINCT payee from %(name)s" \
            " ORDER BY payee ASC" % dict(name=self.name)

        self.cur.execute(stmt)
        rows = [payee[0].encode("utf-8") for payee in self.cur.fetchall()]

        return rows

    def _executeSQL(self, stmt, args):
        """ Excutes passed SQL and returns the result """

        try:
            return self.cur.execute(stmt, args)
        except Exception, e:
            print "Unexpected error:", sys.exc_info()[0], e
            return None

    def _createQueryParams(self, kwargs):
        """
        Helper method to create a statement and arguments to a query.
        """

        if None == kwargs or 0 == len(kwargs):
            return ("", [])

        

        if not isinstance(kwargs,str):
            pairs = kwargs.items()
            stmt = " WHERE " + \
                " AND ".join([ x[0] + (None == x[1] and " IS NULL" or " = ?")
                    for x in pairs ])
            
            args = [ x[1] for x in filter(lambda x: None != x[1], pairs) ]
        else:
            stmt = " WHERE " + kwargs
            args = []
        return (stmt, args)
