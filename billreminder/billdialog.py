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
# -*- coding: utf-8 -*-

#default python imports
import sys
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
import os
import gobject
import time
import datetime

#custom imports
from bill import Bill
import common
from dal import DAL
import utils

class BillDialog:
    """ This is the dialog to add/edit bills """

    def __init__(self, bill=None, parent=None):
        """
            Bill Dialog Constructor
        """
        
        #Set the Glade file
        self.gladefile = gtk.glade.XML(common.BILLGLADEFILE, common.BILLDIALOG_NAME)

        #get form widgets and map it to objects
        self.frmBillDialog = self.gladefile.get_widget(common.BILLDIALOG_NAME)
        self.frmBillDialog.set_icon_from_file(common.IMAGE_PATH + 'billreminder.ico')
        
        # if the dialog has a parent form
        # disable the parent form
        self.parent = parent
        if parent != None:
            self.frmBillDialog.set_transient_for(parent)
            self.parent.set_sensitive(False)
            
        #Field controls
        self.txtAmount = self.gladefile.get_widget('txtAmount')
        self.cCalendar = self.gladefile.get_widget('cCalendar')
        self.cboPayee = self.gladefile.get_widget('cboPayee')
        self.txtNotes = self.gladefile.get_widget('txtNotes')
        self.chkPaid = self.gladefile.get_widget('chkPaid')
        self.txtBuffer = self.txtNotes.get_buffer()

        #setup the GUI
        
        self.bill = bill
         
       # fill the combo with saved payee's names
        self._populatePayee()

        # If a bill object was passed, go into edit mode
        if self.bill != None:
            self.frmBillDialog.set_title("Editing bill '%s'" % bill.Payee )
            # Format the amount field
            self.txtAmount.set_text("%0.2f" % bill.AmountDue)
            # Format the dueDate field
            dt = datetime.datetime.fromtimestamp(bill.DueDate)
            self.cCalendar.select_day(dt.day)
            self.cCalendar.select_month(dt.month -1,dt.year)
            utils.select_combo_Text(self.cboPayee,bill.Payee)
            self.txtBuffer.set_text(bill.Notes)
            self.chkPaid.set_active(bill.Paid)
                

    def run(self):
        """ This function will show the dialog """        
        #run the dialog and store the response      
        result = self.frmBillDialog.run()

        #we are done with the dialog, destroy it
        self.frmBillDialog.destroy()
        
        if self.parent != None:
            self.parent.set_sensitive(True) 
        if (result == gtk.RESPONSE_OK):
            # Extracts the date off the calendar widget
            day = self.cCalendar.get_date()[2]
            month = self.cCalendar.get_date()[1] + 1
            year = self.cCalendar.get_date()[0]
            # Create datetime object
            selectedDate = datetime.datetime(year, month, day)
            # Turn it into a time object
            selectedDate = time.mktime(selectedDate.timetuple())

            #buffer = self.txtNotes.get_buffer()
            startiter, enditer = self.txtBuffer.get_bounds()
            sbuffer = self.txtBuffer.get_text(startiter, enditer)

            # Gets the payee
            payee = self._getPayee()

            if self.bill == None:
                # Create a new object
                self.bill = Bill(payee, selectedDate, self.txtAmount.get_text(), sbuffer,self.chkPaid.get_active())
            else:
                # Edit existing bill
                self.bill.Payee = payee
                self.bill.DueDate = selectedDate
                self.bill.AmountDue = self.txtAmount.get_text()
                self.bill.Notes = sbuffer

            #return the result and bill
            return result, self.bill
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
            iteration = self.cboPayee.get_active_iter()
            if iteration:
                return model.get_value(iteration, 0)
        else:
            return self.cboPayeeEntry.get_text()
