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

import sys
try:
    import pygtk
    pygtk.require("2.0")
except:
      pass
try:
    import gtk
    import gtk.glade
    import datetime
    import time
    import gobject
    from bill import Bill
    from dal import DAL
except:
    sys.exit(1)

class BillDialog:
    """This is the dialog to add/edit bills"""

    def __init__(self):
        #Set the Glade file
        self.gladefilename = "billreminder.glade"
        self.formName = "frmBillDialog"
        self.gladefile = gtk.glade.XML(self.gladefilename, self.formName)

        self.frmBillDialog = self.gladefile.get_widget(self.formName)

        self.txtAmount = self.gladefile.get_widget("txtAmount")
        self.cCalendar = self.gladefile.get_widget("cCalendar")
        self.cboPayee = self.gladefile.get_widget("cboPayee")

        # Populate payees
        self._populatePayee()

        #dic = {"on_cboPayee_changed" : self.on_cboPayee_changed}

    def run(self):
        """This function will show the dialog"""        
        #run the dialog and store the response      
        result = self.frmBillDialog.run()

        #we are done with the dialog, destory it
        self.frmBillDialog.destroy()

        if (result == gtk.RESPONSE_OK):
            # Extracts the date off the calendar widget
            day = self.cCalendar.get_date()[2]
            month = self.cCalendar.get_date()[1] + 1
            year = self.cCalendar.get_date()[0]
            # Create datetime object
            selectedDate = datetime.datetime(year, month, day)
            # Turn it into a time object
            selectedDate = time.mktime(selectedDate.timetuple())

            # Gets the payee
            payee = self._getPayee()
            myBill = Bill(payee, selectedDate, self.txtAmount.get_text(), "hi")

            #return the result and bill
            return result, myBill
        else:
            #return the result and bill
            return None, None

    def _populatePayee(self):
        """ Populates combobox with existing payees """
        # Connects to the database
        dal = DAL()

        # List of payees from database
        payees = dal.Payees()

        store = gtk.ListStore(gobject.TYPE_STRING)
        for payee in payees:
            store.append([payee])

        self.cboPayee.set_model(store)
        self.cboPayee.set_text_column(0)
        self.cboPayeeEntry = self.cboPayee.child
        self.selectedText = ''

    def _getPayee(self):
        """ Extracts information typed into comboboxentry """
        if self.cboPayee.get_active_iter() != None:
            model = self.cboPayee.get_model()
            iter = self.cboPayee.get_active_iter()
            if iter:
                return model.get_value(iter, 0)
        else:
            return self.cboPayeeEntry.get_text()

class AboutDialog:
    """This is the About dialog window"""
    def __init__(self):

        #Set the Glade file
        self.gladefilename = "billreminder.glade"
        self.formName = "frmAbout"
        self.gladefile = gtk.glade.XML(self.gladefilename, self.formName)

    def run(self):
        """This function will show the aboutDialog"""

        #Get the actual dialog widget
        frmAbout = self.gladefile.get_widget(self.formName)
        frmAbout.set_position(gtk.WIN_POS_CENTER)
        frmAbout.set_modal(True)
        #run the dialog and store the response      
        result = frmAbout.run()

        #we are done with the dialog, destroy it
        frmAbout.destroy()

        #return the result and the wine
        return  result  

class BillReminder:
    """ This is the main window of the application """

    def __init__(self):
        #Set the Glade file
        self.gladefilename = "billreminder.glade"
        self.formName = "frmMain"
        self.gladefile = gtk.glade.XML(self.gladefilename, self.formName)

        #Create our dictionay and connect it
        dic = {"on_frmMain_destroy" : self.on_frmMain_destroy,
                "on_btnQuit_clicked" : self.on_btnQuit_clicked,
                "on_btnAdd_clicked" : self.on_btnAdd_clicked,
                "on_mnuAbout_activate" : self.on_mnuAbout_activate}
        self.gladefile.signal_autoconnect(dic)

        # Connects to the database
        self.dal = DAL()

        #Formats the tree view
        self.formatTreeView()

        # and populate it
        self.populateTreeView(self.dal.get({'paid': 0}))

    def on_frmMain_destroy(self, widget):
        """Quit yourself"""
        gtk.main_quit()

    def on_btnQuit_clicked(self, widget):
        self.on_frmMain_destroy(widget)

    def on_btnAdd_clicked(self, widget):
        # Displays the Bill dialog
        frmBillDialog = BillDialog()
        response, bill = frmBillDialog.run()

        # Checks if the user did not cancel the action
        if (response == gtk.RESPONSE_OK):
            # Add new bill to database
            if self.dal.add(bill):
                # Format the dueDate field
                dueDate = datetime.datetime.fromtimestamp(bill.dueDate)
                dueDate = dueDate.strftime('%Y/%m/%d')
                # Format the amount field
                amountDue = "%0.2f" % float(bill.amountDue)
                self.billList.append([bill.payee, dueDate, amountDue])

    def on_mnuAbout_activate(self, widget):
        frmAbout = AboutDialog()
        response = frmAbout.run()
    
    def on_billView_double_Click(self, widget, path, view_column):
        """
            This event will be fired when a user double click
            a row in the bill treeview.
            For now we will just rise up a dialog box showing
            the first cell value.
        """
        sel = widget.get_selection()
        model, iter = sel.get_selected()
        
        text = model.get_value(iter, 0)
        date = model.get_value(iter, 1)
        amount = model.get_value(iter,2)
        
        print 'row activated: %s, %s , %s' % (text,date,amount)
        pass
    
    def populateTreeView(self, records):
        """ Populates the treeview control with the records passed """

        for rec in records:
            payee = rec['payee']
            # Format the dueDate field
            dueDate = rec['dueDate']
            dueDate = datetime.datetime.fromtimestamp(rec['dueDate'])
            dueDate = dueDate.strftime('%Y/%m/%d')
            # Format the amount field
            amountDue = "%0.2f" % float(rec['amountDue'])
            #notes = rec['notes']
            #paid = rec['paid']
            self.billList.append([payee, dueDate, amountDue])

    def formatTreeView(self):
        #Here are some variables that can be reused later
        self.colPayee = 0
        self.colDueDate = 1
        self.colAmountDue = 2

        self.strPayee = "Payee"
        self.strDueDate = "Due Date"
        self.strAmountDue = "Amount Due"

        #Get the treeView from the widget Tree
        self.billView = self.gladefile.get_widget("tvBills")
        #Add all of the List Columns to the wineView
        self.addBillListColumn(self.strPayee, self.colPayee)
        self.addBillListColumn(self.strDueDate, self.colDueDate)
        self.addBillListColumn(self.strAmountDue, self.colAmountDue)

        #Create the listStore Model to use with the wineView
        self.billList = gtk.ListStore(str, str, str)
        #Attache the model to the treeView
        self.billView.set_model(self.billList)
        self.billView.connect('row-activated',self.on_billView_double_Click)

    def addBillListColumn(self, title, columnId):
        """This function adds a column to the list view.
        First it create the gtk.TreeViewColumn and then sets
        some needed properties"""

        column = gtk.TreeViewColumn(title, gtk.CellRendererText()
            , text=columnId)
        column.set_resizable(True)      
        column.set_sort_column_id(columnId)
        self.billView.append_column(column)


if __name__ == "__main__":
    br = BillReminder()
    gtk.main()
