#!/usr/bin/python
# -*- coding: utf-8 -*-

__all__ = ['BillDialog']

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
import common
import model.i18n
from model.bill import Bill
from model.dal import DAL
import controller.utils

class BillDialog:
    """ This is the dialog to add/edit bills """

    def __init__(self, bill=None, parent=None):
        """
            Bill Dialog Constructor
        """
        
        #Set the Glade file
        self.gladefile = gtk.glade.XML(common.BILLGLADEFILE, common.BILLDIALOG_NAME, domain='billreminder')

        #get form widgets and map it to objects
        self.frmBillDialog = self.gladefile.get_widget(common.BILLDIALOG_NAME)
        self.frmBillDialog.set_icon_from_file(common.APP_ICON)
        #self.frmBillDialog.set_icon_from_file(common.IMAGE_PATH + 'billreminder.ico')
        
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
        if self.bill is not None:
            self.frmBillDialog.set_title(_("Editing bill '%s'") % bill.Payee)
            # Format the amount field
            self.txtAmount.set_text("%0.2f" % bill.AmountDue)
            # Format the dueDate field
            dt = datetime.datetime.fromtimestamp(bill.DueDate)
            self.cCalendar.select_day(dt.day)
            self.cCalendar.select_month(dt.month - 1, dt.year)
            controller.utils.select_combo_Text(self.cboPayee, bill.Payee)
            self.txtBuffer.set_text(bill.Notes)
            self.chkPaid.set_active(bill.Paid)
                

    def run(self):
        """ This function will show the dialog """        
        #run the dialog and store the response      
        result = self.frmBillDialog.run()

        #we are done with the dialog, destroy it
        self.frmBillDialog.destroy()
        
        if self.parent is not None:
            self.parent.set_sensitive(True) 
        if result == gtk.RESPONSE_OK:
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

            if self.bill is None:
                # Create a new object
                self.bill = Bill(payee, selectedDate, self.txtAmount.get_text(), sbuffer, int(self.chkPaid.get_active()))
            else:
                # Edit existing bill
                self.bill.Payee = payee
                self.bill.DueDate = int(selectedDate)
                self.bill.AmountDue = float(self.txtAmount.get_text())
                self.bill.Notes = sbuffer
                self.bill.Paid = int(self.chkPaid.get_active())

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
        payees = []
        records = dal.get('tblbills', "paid IN (0,1) ORDER BY payee ASC")
        for rec in records:
            if rec['payee'] not in payees:
                payees .append(rec['payee'])

        store = gtk.ListStore(gobject.TYPE_STRING)
        for payee in payees:
            store.append([payee])

        self.cboPayee.set_model(store)
        self.cboPayee.set_text_column(0)
        self.cboPayeeEntry = self.cboPayee.child
        self.selectedText = ''

    def _getPayee(self):
        """ Extracts information typed into comboboxentry """
        if self.cboPayee.get_active_iter() is not None:
            model = self.cboPayee.get_model()
            iteration = self.cboPayee.get_active_iter()
            if iteration:
                return model.get_value(iteration, 0)
        else:
            return self.cboPayeeEntry.get_text()
