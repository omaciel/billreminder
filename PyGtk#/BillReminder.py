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
# BillReminder - Copyright (c) 2006 Og Maciel
#
# -*- coding: utf-8 -*-
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, gobject
import os, sys
import threading
from pysqlite2 import dbapi2 as sqlite

# Caminho para a pasta do programa
path= os.path.abspath (os.path.dirname (sys.argv[0]))

class Dialog:
    def __init__(self, name):
        self.glade = gtk.glade.XML('billreminder.glade', name)

        self.glade.signal_autoconnect({
        })
        
        self.glade.Modal = true;
        self.glade.Show();

class Display:
    def __init__(self, whereClause):
        
        self.glade = gtk.glade.XML('billreminder.glade', 'frmDisplay')
 
        self.frmDisplay = self.glade.get_widget('frmDisplay')
        
        self.glade.signal_autoconnect({
            'on_btnClose_clicked' : self.on_btnClose_clicked
        })
        
        self.format_listview()
        self.populate_bills()
        
    def format_listview(self):
    
        # Treeview
        treeview = self.glade.get_widget('tvBills')
        
        self.list = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING)
        self.list.clear()

        treeview.set_model(self.list)
        treeview.append_column(gtk.TreeViewColumn('Payee', gtk.CellRendererText(), text=0))
        treeview.append_column(gtk.TreeViewColumn('Amount', gtk.CellRendererText(), text=1))
        treeview.append_column(gtk.TreeViewColumn('Due Date', gtk.CellRendererText(), text=2))
        
    def populate_bills(self, whereClause):

        # TODO: Append the where clause if its not null
        sqlStatement = "SELECT id, payee, amountDue, dueDate FROM bills ORDER BY dueDate, payee"
        
	# Fetch all results to be displayed
	#rs.execute ("SELECT id, payee, amountDue, dueDate FROM bills ORDER BY dueDate, payee")
	rs.execute(sqlStatement + whereClause)
	result = rs.fetchall ()

        for id, payee, amountDue, dueDate in result :
            self.list.append([payee, amountDue, dueDate])
         
    # Callbacks
    def on_btnClose_clicked(self, widget, data = None):		
	self.frmDisplay.hide()
	
class GtkClient:

    def __init__(self):
                
        self.glade = gtk.glade.XML('billreminder.glade', 'frmMenu')
	self.btnClose = self.glade.get_widget("btnClose")
	self.btnDisplay = self.glade.get_widget("btnDisplay")
	
        self.glade.signal_autoconnect({
            'on_btnClose_clicked' : self.on_btnClose_clicked,
            'on_btnDisplay_clicked' : self.on_btnDisplay_clicked
        })

    # Callbacks
    def on_btnClose_clicked(self, widget, data = None):
	gtk.main_quit()

    def on_btnDisplay_clicked(self, widget, data = None):
	Display("")

if __name__ == '__main__':
   
    # Arquivo da base de dados
    #db= '%s/data/BillReminder.db' % path
    db = 'data/BillReminder.db'

    # Faz conexão com a base de dados ou cria caso não exista
    if os.path.isfile (db) :
        cn = sqlite.connect (db, isolation_level=None)
        rs = cn.cursor ()
    else :
	cn = sqlite.connect (db, isolation_level=None)
	rs = cn.cursor ()
	rs.execute ("CREATE TABLE bills (id INTEGER PRIMARY KEY, payee VARCHAR(50) NOT NULL, amountDue VARCHAR(10) NOT NULL, dueDate INTEGER NOT NULL, paid CHAR(1) DEFAULT '0' )")

    #gtk.threads_init()
    client = GtkClient()
    gtk.main()
