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
    import os
    import time
    import gobject
    from bill import Bill
    from dal import DAL
except:
    sys.exit(1)

# Glade file name
GLADEFILE = "billreminder.glade"

class Message:
    
    def question(self, msg, cancel=1, parent=None):
        if not parent: parent = self
        dialog = gtk.MessageDialog(parent, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, \
                                   gtk.MESSAGE_QUESTION, gtk.BUTTONS_NONE, msg)
        dialog.add_buttons(gtk.STOCK_YES, gtk.RESPONSE_YES, gtk.STOCK_NO, gtk.RESPONSE_NO)
    
        if cancel: dialog.add_buttons(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        dialog.set_default_response(gtk.RESPONSE_CANCEL)
        response = dialog.run()
        dialog.destroy()
        return response

def select_combo_Text(cb,text):
    i=0
    
    for n in cb.get_model():
        if n[0] == text:
            break
        i +=1
    cb.set_active(i)
    
def str_to_date(strdate):
    dt = strdate.split()[0]
    sep = [c for c in dt if not c.isdigit()][0]
    dtPieces = [int(p) for p in dt.split(sep)]
    print dtPieces
    return datetime.date(dtPieces[0], dtPieces[1], dtPieces[2])

    
    
    
class BillDialog:
    """ This is the dialog to add/edit bills """

    def __init__(self, bill=None):
        #Set the Glade file
        self.gladefilename = os.path.join(os.path.dirname(__file__), GLADEFILE)
        self.formName = "frmBillDialog"
        self.gladefile = gtk.glade.XML(self.gladefilename, self.formName)

        self.frmBillDialog = self.gladefile.get_widget(self.formName)

        self.txtAmount = self.gladefile.get_widget("txtAmount")
        self.cCalendar = self.gladefile.get_widget("cCalendar")
        self.cboPayee = self.gladefile.get_widget("cboPayee")
        self.txtNotes = self.gladefile.get_widget("txtNotes")
        self.txtBuffer = self.txtNotes.get_buffer()

        # Populate payees
        self._populatePayee()

        self.bill = bill

        # If a bill object was passed, go into edit mode
        if self.bill != None:
            self.txtAmount.set_text(bill.amountDue)
            dt = str_to_date(bill.dueDate)
            self.cCalendar.select_day(dt.day)
            self.cCalendar.select_month(dt.month -1,dt.year)
            select_combo_Text(self.cboPayee,bill.payee)
            self.txtBuffer.set_text(bill.notes)

    def run(self):
        """ This function will show the dialog """        
        #run the dialog and store the response      
        result = self.frmBillDialog.run()

        #we are done with the dialog, destroy it
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

            #buffer = self.txtNotes.get_buffer()
            startiter, enditer = self.txtBuffer.get_bounds()
            buffer = self.txtBuffer.get_text(startiter, enditer)

            # Gets the payee
            payee = self._getPayee()
            if self.bill == None:
                self.bill = Bill(payee, selectedDate, self.txtAmount.get_text(), buffer)
            else:
                self.bill.payee = payee
                self.bill.amoutDue = self.txtAmount.get_text()
                self.bill.dueDate = selectedDate
                self.bill.notes = buffer


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
            iter = self.cboPayee.get_active_iter()
            if iter:
                return model.get_value(iter, 0)
        else:
            return self.cboPayeeEntry.get_text()

class AboutDialog:
    """ This is the About dialog window """
    def __init__(self):

        #Set the Glade file
        self.gladefilename = os.path.join(os.path.dirname(__file__), GLADEFILE)
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
        self.gladefilename = os.path.join(os.path.dirname(__file__), GLADEFILE) 
        self.formName = "frmMain"
        self.gladefile = gtk.glade.XML(self.gladefilename, self.formName)
        

        #get form widgets and map it to objects
        self.frmMain = self.gladefile.get_widget(self.formName)
        self.btnQuit = self.gladefile.get_widget('btnQuit')
        self.btnAdd = self.gladefile.get_widget('btnAdd')
        self.btnRemove = self.gladefile.get_widget('btnRemove')
        self.btnEdit = self.gladefile.get_widget('btnEdit')
        self.btnPaid = self.gladefile.get_widget('btnPaid')
        self.mnuAbout = self.gladefile.get_widget('mnuAbout')
        self.mnuAdd = self.gladefile.get_widget('mnuAdd')
        self.mnuEdit = self.gladefile.get_widget('mnuEdit')
        self.lblStatusPanel1 = self.gladefile.get_widget('lblStatusPanel1')
        self.lblStatusPanel2 = self.gladefile.get_widget('lblStatusPanel2')
        
        #set unused buttons to disable mode
        self.enable_buttons(False)
        # connect all handled signals to our procedures
        self.frmMain.connect('destroy', self.on_frmMain_destroy)
        self.btnQuit.connect('clicked',self.on_btnQuit_clicked)
        self.btnAdd.connect('clicked', self.on_btnAdd_clicked)
        self.btnEdit.connect('clicked', self.on_btnEdit_clicked)
        self.mnuAbout.connect('activate',self.on_mnuAbout_activate)
        self.mnuAdd.connect('activate',self.on_mnuAdd_activate)
        self.mnuEdit.connect('activate',self.on_mnuEdit_activate)

        # Connects to the database
        self.dal = DAL()

        #Formats the tree view
        self.formatTreeView()

        # and populate it
        self.populateTreeView(self.dal.get({'paid': 0}))

        # Current record holder
        self.currentBill = None
        self.id = None

    def update_status_bar(self):
        self.lblStatusPanel1.set_markup('<b>Records:</b> %d' % len(self.billList))
        
    def enable_buttons(self, bValue):
        """
            Enable/disable buttons.
            If bValue = True  buttons will be enabled.
        """
        self.btnRemove.set_sensitive(bValue)
        self.btnEdit.set_sensitive(bValue)
        self.btnPaid.set_sensitive(bValue)
        
    def on_frmMain_destroy(self, widget):
        """Quit yourself"""
        gtk.main_quit()

    def on_btnQuit_clicked(self, widget):
        self.on_frmMain_destroy(widget)

    def on_btnAdd_clicked(self, widget):
        self.addBill()

    def on_btnEdit_clicked(self, widget):
        self.editBill()

    def addBill(self):
        # Displays the Bill dialog
        frmBillDialog = BillDialog()
        response, bill = frmBillDialog.run()

        # Checks if the user did not cancel the action
        if (response == gtk.RESPONSE_OK):
            # Add new bill to database
            ret = self.dal.add(bill)
            if ret:
                # Format the dueDate field
                dueDate = datetime.datetime.fromtimestamp(bill.dueDate)
                dueDate = dueDate.strftime('%Y/%m/%d')
                # Format the amount field
                amountDue = "%0.2f" % float(bill.amountDue)
                self.billList.append(['', bill.payee, dueDate, amountDue, bill.notes, bill.paid])
                self.update_status_bar()

    def editBill(self):
        # Get currently selected bill and its id
        id, bill = self.getBill()
        # Displays the Bill dialog
        frmBillDialog = BillDialog(bill)
        response, bill = frmBillDialog.run()

        # Checks if the user did not cancel the action
        if (response == gtk.RESPONSE_OK):
            try:
                # Edit bill in the database
                self.dal.edit(id, bill)
                # Format the dueDate field
                dueDate = datetime.datetime.fromtimestamp(bill.dueDate)
                dueDate = dueDate.strftime('%Y/%m/%d')
                # Format the amount field
                amountDue = "%0.2f" % float(bill.amountDue)
                idx = widget.get_cursor()[0][0]
                self.billList[idx] = [id, bill.payee, dueDate, amountDue, bill.notes, bill.paid]
            except e:
                print str(e)

    def on_mnuAdd_activate(self, widget):
        self.addBill()

    def on_mnuEdit_activate(self, widget):
        self.editBill()

    def on_mnuAbout_activate(self, widget):
        frmAbout = AboutDialog()
        response = frmAbout.run()

    def on_billView_button_press_event(self, widget, event):
        if event.button == 3 and event.type == gtk.gdk.BUTTON_PRESS:
            c = ContextMenu(self)
            c.addMenuItem('Add New', self.addBill(), gtk.STOCK_ADD)
            c.addMenuItem('-', None)
            c.addMenuItem('Remove',None ,gtk.STOCK_REMOVE)
            c.addMenuItem('Edit', self.editBill(), gtk.STOCK_EDIT)
            c.addMenuItem('Paid', None,gtk.STOCK_APPLY,True)
            c.addMenuItem('-', None)
            c.addMenuItem('Cancel', None,gtk.STOCK_CANCEL)
            c.popup(None, None, None, event.button, event.get_time())

    def on_billView_cursor_changed(self, widget):
        """ Displays the selected record information """
        try:
            sel = widget.get_selection()
            model, iter = sel.get_selected()

            id = model.get_value(iter, 0)
            notes = model.get_value(iter,4)

            # Display the status for the selected row
            self.lblStatusPanel2.set_text('Notes: %s' % (notes))
            self.enable_buttons(True)
        except :
            pass 

    def getBill(self):
        """ Returns a bill object from the current selected record """
        try:
            sel = self.billView.get_selection()
            model, iter = sel.get_selected()

            id = model.get_value(iter, 0)
            payee = model.get_value(iter, 1)
            date = model.get_value(iter, 2)
            amount = model.get_value(iter,3)
            notes = model.get_value(iter,4)
            paid = model.get_value(iter,5)

            # Instantiate new Bill object
            b = Bill(payee, date, amount, notes, paid)
            # Return bill and id
            return id, b
        except e:
            print str(e)
            return None, None

    def populateTreeView(self, records):
        """ Populates the treeview control with the records passed """

        for rec in records:
            id = rec['Id']
            payee = rec['payee']
            # Format the dueDate field
            dueDate = rec['dueDate']
            dueDate = datetime.datetime.fromtimestamp(rec['dueDate'])
            dueDate = dueDate.strftime('%Y/%m/%d')
            # Format the amount field
            amountDue = "%0.2f" % float(rec['amountDue'])
            notes = rec['notes']
            paid = rec['paid']
            self.billList.append([id, payee, dueDate, amountDue, notes, paid])

        # Select the first row
        self.update_status_bar()
        self.billView.set_cursor(0)

    def formatTreeView(self):
        #Here are some variables that can be reused later
        self.colId = 0
        self.colPayee = 1
        self.colDueDate = 2
        self.colAmountDue = 3
        self.colNotes = 4
        self.colPaid = 5

        self.strId = "Id"
        self.strPayee = "Payee"
        self.strDueDate = "Due Date"
        self.strAmountDue = "Amount Due"
        self.strNotes = "Notes"
        self.strPaid = "Paid"

        #Get the treeView from the widget Tree
        self.billView = self.gladefile.get_widget("tvBills")
        #Add all of the List Columns to the treeView
        self.addBillListColumn(self.strId, self.colId, 100, False)
        self.addBillListColumn(self.strPayee, self.colPayee, 160, True)
        self.addBillListColumn(self.strDueDate, self.colDueDate, 100, True)
        self.addBillListColumn(self.strAmountDue, self.colAmountDue, 100, True)
        self.addBillListColumn(self.strNotes, self.colNotes, 100, False)
        self.addBillListColumn(self.strPaid, self.colPaid, 100, False)

        #Create the listStore Model to use with the treeView
        self.billList = gtk.ListStore(str, str, str, str, str, str)
        #self.billList.connect('row-inserted', self.on_billList_row_inserted)
        #Attache the model to the treeView
        self.billView.set_model(self.billList)
        self.billView.connect('cursor_changed', self.on_billView_cursor_changed)
        self.billView.connect("button_press_event", self.on_billView_button_press_event)

    def addBillListColumn(self, title, columnId, size=100, visible=True):
        """ This function adds a column to the list view.
        First it create the gtk.TreeViewColumn and then sets
        some needed properties """

        column = gtk.TreeViewColumn(title, gtk.CellRendererText()
            , text=columnId)
        column.set_resizable(True)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_min_width(size)
        column.set_clickable(True)
        column.set_visible(visible)
        column.set_sort_column_id(columnId)

        self.billView.append_column(column)

# maybe we should create a file for each class or a package for imports
class ContextMenu(gtk.Menu):
    """ Creates context menus accessed by mouse right click. """
    def __init__(self, *args):
        gtk.Menu.__init__(self)
        self.menuItem = None
    
    def addMenuItem(self,menuName,actionFunction= None,menuImage = None, forceName = False):
        """
            Add itens to menu.
            
            @menuName is the text showed in the menu option.
                    If you pass a - (minus) as parameter value,
                    it will create a separation menu item.
            @actionFunction is the procedure called when activate signal is triggered from the menu.
            
        """
        if menuName == "-":
            self.menuItem = gtk.SeparatorMenuItem()
        else:
            if menuImage != None:
                if isinstance(menuImage, gtk.Image):
                    self.menuItem = gtk.ImageMenuItem(menuName)
                    self.menuItem.set_image(menuImage)
                else:
                    if not forceName:
                        self.menuItem = gtk.ImageMenuItem(menuImage)
                    else:
                        self.menuItem = gtk.ImageMenuItem(menuName)
                        img = gtk.Image()
                        img.set_from_stock(menuImage,gtk.ICON_SIZE_MENU)
                        self.menuItem.set_image(img)
            else:    
                self.menuItem = gtk.ImageMenuItem(menuName)
                
            if actionFunction is not None :
                self.menuItem.connect("activate", actionFunction)
        self.menuItem.show()
        self.append(self.menuItem)
        return
            
if __name__ == "__main__":
    br = BillReminder()
    gtk.main()
