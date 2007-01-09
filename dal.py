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

import os
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
        billDict['payee'] = bill.payee
        billDict['dueDate'] = bill.dueDate
        billDict['amountDue'] = bill.amountDue
        billDict['notes'] = bill.notes

        return billDict

    def add(self, bill):
        """ Adds a bill to the database """
        # Separate columns and values
        billDict = self._makeBillDict(bill)
        values = billDict.values()
        cols = billDict.keys()

        # Insert statement
        stmt = "INSERT INTO %s (%s) VALUES (%s)" %\
            (self.name, ",".join(cols), ",".join('?' * len(values)))

        return self._executeSQL(stmt, values)

    def delete(self, bill):
        billDict = self._makeBillDict(bill)
        # Generate WHERE clause and separate arguments
        (stmt, args) = self._createQueryParams(billDict)

        # Delete statement
        stmt = "DELETE FROM %(name)s" % dict(name=self.name) + stmt

        return self._executeSQL(stmt, args)

    def edit(self, id, bill):
        billDict = self._makeBillDict(bill)
        pairs = billDict.items()

        params = "=?, ".join([ x[0] for x in pairs ]) + "=?"
        stmt = "UPDATE %s SET %s WHERE %s=?" % (self.name, params, self.key)

        args = [ x[1] for x in pairs ] + [id]

        
        return self._executeSQL(stmt, args)

    def get(self, kwargs):
        """ Returns one or more records that meet the criteria passed """
        (stmt, args) = self._createQueryParams(kwargs)

        stmt = "SELECT %(fields)s FROM %(name)s" \
            % dict(fields=", ".join(self.fields), name=self.name) + stmt
            
        self.cur.execute(stmt, args)

        rows = [dict([ (f, row[i]) for i, f in enumerate(self.fields) ]) \
            for row in self.cur.fetchall()]

        return rows

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
            self.cur.execute(stmt, args)
        except Exception, e:
            return None

    def _createQueryParams(self, kwargs):
        """
        Helper method to create a statement and arguments to a query.
        """

        if None == kwargs or 0 == len(kwargs):
            return ("", [])

        pairs = kwargs.items()

        stmt = " WHERE " + \
            " AND ".join([ x[0] + (None == x[1] and " IS NULL" or " = ?")
                for x in pairs ])
        args = [ x[1] for x in filter(lambda x: None != x[1], pairs) ]

        return (stmt, args)

if __name__ == 'main':
    import time

    d = DAL()
    values = {"Id":1, "payee":'Verizon', "dueDate":time.time(), "amountDue":round(56.25, 2), "notes":'', "paid":0}
    # parameters using ** must be a dictionary :)
    d.add(values)
    print 'getting bills'
    print d.get({'Id':10})
    print "Done"
