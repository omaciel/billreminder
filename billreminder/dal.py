#!/usr/bin/python
#
# The MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of 
# this software and associated documentation files (the "Software"), to deal in the 
# Software without restriction, including without limitation the rights to use, copy, 
# modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
# and to permit persons to whom the Software is furnished to do so, subject to the 
# following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# BillReminder - Copyright (c) 2006, 2007 Og Maciel
#
# -*- coding: utf-8 -*-

import os, sys
from pysqlite2 import dbapi2 as sqlite
from bill import Bill

class DAL(object):

    # Database name and path
    dbName = 'billreminder.db'
    dbPath = '%s/.config/billreminder/data/' % os.environ['HOME']

    name = "bills"
    createSQL = """
        CREATE TABLE %s (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            payee TEXT NOT NULL,
            dueDate INTEGER NOT NULL,
            amountDue INTEGER NOT NULL,
            notes TEXT,
            paid INTEGER DEFAULT 0)
    """ % name

    fields = ["Id", "payee", "dueDate", "amountDue", "notes", "paid"]
    key = 'Id'

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

    def _makeBillDict(self, bill):
        billDict = {}
        billDict['payee'] = bill.Payee
        billDict['dueDate'] = bill.DueDate
        billDict['amountDue'] = bill.AmountDue
        billDict['notes'] = bill.Notes

        return billDict

    def add(self, bill):
        """ Adds a bill to the database """
        # Removes the Id field
        dic = bill.Dictionary
        del dic['Id']
        # Separate columns and values
        values = dic.values()
        cols = dic.keys()

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
        #
        # Split up into pais
        pairs = bill.Dictionary.items()

        params = "=?, ".join([ x[0] for x in pairs ]) + "=?"
        stmt = "UPDATE %s SET %s WHERE %s=?" % (self.name, params, self.key)

        args = [ x[1] for x in pairs ] + [id]

        rowsAffected = self._executeSQL(stmt, args)
        return rowsAffected

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
