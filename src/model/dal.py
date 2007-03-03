#!/usr/bin/python
# -*- coding: utf-8 -*-

__all__ = ['DAL']

import os, sys
from pysqlite2 import dbapi2 as sqlite

from model.bill import Bill
from model.db.versionstable import VersionsTable
from model.db.billstable import BillsTable

class DAL(object):

    # Database name and path
    dbName = 'billreminder.db'
    dbPath = '%s/.config/billreminder/data/' % os.environ['HOME']

    # Tables used by applications and corresponding versions
    _tables = {VersionsTable().Name: VersionsTable(),
        BillsTable().Name: BillsTable()}
    tables = {'tblversions': VersionsTable(),
        'tblbills': BillsTable()}

    def __init__(self):
        if not os.path.isdir(self.dbPath):
            os.makedirs(self.dbPath)
            
        self.conn = sqlite.connect(os.path.join(self.dbPath, self.dbName), isolation_level=None)
        self.cur = self.conn.cursor()
        
        if os.path.isfile(os.path.join(self.dbPath, self.dbName)):
            self.validateTables()
        else :
            self._createDb()

    def validateTables(self):
        """ Validates that all tables are up to date. """
        stmt = "select tbl_name from sqlite_master where type = 'table' and tbl_name like 'br_%'"
        self.cur.execute(stmt)
        tbllist = self.cur.fetchall()
        
        # Create all tables if database is empty
        if len(tbllist) is 0: 
            self._createDb()
            return
        
        for table in tbllist:
            ver = self.get('tblversions', {'tablename': table[0]})
            if not self._tables[table[0]].Version is ver:
                pass
    
    def _createDb(self):
        for table in self._tables.values():
            self._createTable(table)
    
    def _createTable(self, table, temp=False):
    	# TODO: Verificar se eh uma tabela temporaria
        try:
            self.cur.execute(table.CreateSQL)
            self.conn.commit()
            self.add()
        except:
            pass
    
    def _removeTable(self, table):
    	pass
    
    def _createQueryParams(self, kwargs):
        """ Helper method to create a statement and arguments to a query. """
        if None == kwargs or 0 == len(kwargs):
            return ("", [])
        
        if not isinstance(kwargs,str):
            pairs = kwargs.items()
            stmt = " WHERE " + \
                " AND ".join([ x[0] + (None is x[1] and " IS NULL" or " = ?")
                    for x in pairs ])
            
            args = [ x[1] for x in filter(lambda x: None is not x[1], pairs) ]
        else:
            stmt = " WHERE " + kwargs
            args = []
        return (stmt, args)
    
    def get(self, tblnick, kwargs):
        """ Returns one or more records that meet the criteria passed """
        (stmt, args) = self._createQueryParams(kwargs)
        
        stmt = "SELECT %(fields)s FROM %(name)s" \
            % dict(fields=", ".join(self.tables[tblnick].Fields), name=self.tables[tblnick].Name) + stmt
        self.cur.execute(stmt, args)
        
        rows = [dict([ (f, row[i]) for i, f in enumerate(self.tables[tblnick].Fields) ]) \
            for row in self.cur.fetchall()]
        
        return rows

    def add(self, tblnick, kwargs):
        """ Adds a record to the database """
        # Separate columns and values
        kwargs.pop(self.tables[tblnick].Key)
        values = kwargs.values()
        cols = kwargs.keys()
        # Insert statement
        stmt = "INSERT INTO %s (%s) VALUES (%s)" %\
            (self.tables[tblnick].Name, ",".join(cols), ",".join('?' * len(values)))

        self.cur.execute(stmt, values)
        b_key = self.cur.lastrowid
        if b_key:
            rows = self.get(self.tables[tblnick].Name, {self.tables[tblnick].Key: b_key})
            return rows[0]
    
    def edit(self, tblnick, key, dic):
    	""" Edit a record in the database """
        # Removes the key field
        del dic[self.tables[tblnick].Key]
        
        # Split up into pais
        pairs = dic.items()
        
        params = "=?, ".join([ x[0] for x in pairs ]) + "=?"
        stmt = "UPDATE %s SET %s WHERE %s=?" \
            % (self.tables[tblnick].Name, params, self.tables[tblnick].Key)
        
        args = [x[1] for x in pairs] + [key]
        
        rowsAffected = self._executeSQL(stmt, args)
        return rowsAffected.rowcount
    
    def delete(self, tblnick, key):
    	""" Delete a record in the database """
        # Delete statement
        stmt = "DELETE FROM %s WHERE Id=?" % self.tables[tblnick].Name
        rowsAffected = self._executeSQL(stmt, [key])
        return rowsAffected

    def _executeSQL(self, stmt, args):
        """ Excutes passed SQL and returns the result """
        try:
            return self.cur.execute(stmt, args)
        except Exception, e:
            print "Unexpected error:", sys.exc_info()[0], e
            return None


