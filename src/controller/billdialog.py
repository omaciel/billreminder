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
import locale
import re

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

        self.digits = re.compile(r'[0-9]')
        
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
        self.btnSave = self.gladefile.get_widget('btnSave')
        self.txtBuffer = self.txtNotes.get_buffer()

        # Event handlers
        self.txtAmount.connect('insert-text', self.on_insert_text)
        self.txtAmount.connect('focus-out-event', self.on_lost_focus)

        #setup the GUI
        # Mark the current day in the calendar
        self.cCalendar.mark_day(datetime.datetime.today().day) 

        self.bill = bill
         
       # fill the combo with saved payee's names
        self._populatePayee()
        
        self.decimal_sep = locale.localeconv()['mon_decimal_point']
        self.thousands_sep = locale.localeconv()['mon_thousands_sep']
        
        self.allowed_digts = [self.decimal_sep , self.thousands_sep]
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

            # Validate form
            if len(payee.strip()) == 0 or len(self.txtAmount.get_text().strip()) == 0:
                return None, None

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

    def on_lost_focus(self, entry, event):
        try:
            a = float(entry.get_text())
        except:
            if len(entry.get_text()) > 0:
                entry.grab_focus()
                self.btnSave.set_sensitive(False)
                #show a message here
                return True
            

        
    def on_insert_text (self, entry, text, length, position):
        """Stop garbage input.
           What It must do
           1. Allows Numeric (0-9) Digits
           2. Only Allows 1 Decimal "." or any locale
           3. Only Allows 2 digits after decimal "
           4. Does Not Allow decimal as first digit (If you need it comment out that line)
       """
        self.btnSave.set_sensitive(True)
        for c in text[:length]:
            if self.digits.match(c) ==None:
                if not c.lower() in self.allowed_digts:
                    entry.emit_stop_by_name ('insert-text')
                    return
        
        # as event out is checking correct values for this 
        # check if this procedure is really necessary
        """
        #Get atual widget text
        strText = entry.get_text()
        len_txt = len(strText)
        sep_index = strText.find(self.decimal_sep)
        thousand_index = strText.find(self.thousands_sep)
        
        # if digit sent is a number
        if self.digits.match(text):
            #Making sure there is only 2 digits entered after the 
            #decimal separator
        
            if sep_index >0 and len(strText) >=4:
                if strText[-3] == self.decimal_sep:
                    entry.emit_stop_by_name ('insert-text')
                    return
                
        elif text == self.decimal_sep:
           #Not Allowing decimal separator as first character
            #and not Allowing more than one decimal separator
            if len(strText) == 0 or sep_index >0:
                entry.emit_stop_by_name ('insert-text')
                return
            
            if strText[-1] == self.thousands_sep or strText[-2] == self.thousands_sep:
                # not allowing a decial sep aftter a thousand sep
                entry.emit_stop_by_name ('insert-text')
                return
            if len_txt>2 and strText[-3] == self.thousands_sep:
                entry.emit_stop_by_name ('insert-text')
                retur

        #Get atual widget text
        strText = entry.get_text()
        len_txt = len(strText)
        sep_index = strText.find(self.decimal_sep)
        thousand_index = strText.find(self.thousands_sep)
        
        # if digit sent is a number
        if self.digits.match(text):
            #Making sure there is only 2 digits entered after the 
            #decimal separator
        
            if sep_index >0 and len(strText) >=4:n
        elif text ==  self.thousands_sep:
            #Not Allowing thousand separator as first character
            if len(strText) == 0 :
                entry.emit_stop_by_name ('insert-text')
            #will not allow two thousand separator next
            elif strText[-1] == self.thousands_sep:
                entry.emit_stop_by_name ('insert-text')
            
            elif thousand_index  > 0 :
                # just allow a thousand separator after 3 digits if a first separator  was set before
                if (len(strText) -4) <1:
                    entry.emit_stop_by_name ('insert-text')
                elif strText[-4] != self.thousands_sep:
                    entry.emit_stop_by_name ('insert-text')
                 
        else:
            print 'passou'
        """