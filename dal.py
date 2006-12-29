#!/usr/bin/env python

import os
from pysqlite2 import dbapi2 as sqlite
#from bill import Bill

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

    def add(self, kwargs):
        """ Adds a bill to the database """
        # Separate columns and values
        values = kwargs.values()
        cols = kwargs.keys()

        # Insert statement
        stmt = "INSERT INTO %s (%s) VALUES (%s)" %\
            (self.name, ",".join(cols), ",".join('?' * len(values)))

        return self._executeSQL(stmt, values)

    def delete(self, kwargs):
        # Generate WHERE clause and separate arguments
        (stmt, args) = self._createQueryParams(kwargs)

        # Delete statement
        stmt = "DELETE FROM %(name)s" % dict(name=self.name) + stmt

        return self._executeSQL(stmt, args)

    def edit(self, id, kwargs):
        pairs = kwargs.items()

        params = "=?, ".join([ x[0] for x in pairs ]) + "=?"
        stmt = "UPDATE %s SET %s WHERE %s=?" % (self.name, params, self.key)

        args = [ x[1] for x in pairs ] + [id]

        
        return self._executeSQL(stmt, args)

    def get(self, kwargs):
        (stmt, args) = self._createQueryParams(kwargs)

        stmt = "SELECT %(fields)s FROM %(name)s" \
            % dict(fields=", ".join(self.fields), name=self.name) + stmt
            
        self.cur.execute(stmt, args)

        rows = [dict([ (f, row[i]) for i, f in enumerate(self.fields) ]) \
            for row in self.cur.fetchall()]

        return rows

    def _executeSQL(self, stmt, args):
        """ Excutes passed SQL and returns the result """
        # Flag
        success = True

        try:
            self.cur.execute(stmt, args)
        except Exception, e:
            success = False

        return success

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
