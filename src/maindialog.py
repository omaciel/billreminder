#!/usr/bin/python
# -*- coding: utf-8 -*-

#default python imports
import sys
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
import datetime
import os
import time
import gobject
#custom imports
from aboutdialog import AboutDialog
from bill import Bill
from billdialog import BillDialog
import common
from trayicon import NotifyIcon

from dal import DAL
import utils
from utils import ContextMenu, Message

class BillReminder:
    """ This is the main window of the application """

    # set global columns ids for bills tree constants 
    (COL_ID, COL_PAYEE, COL_DUEDATE, COL_AMOUNTDUE, COL_NOTES, COL_PAID) = range(6)

    def __init__(self):
        """ BillReminder constructor. """

        # Set the Glade file
        self.gladefilename = common.MAINGLADEFILE
        self.formName = common.MAINFORM_NAME
        self.gladefile = gtk.glade.XML(self.gladefilename, self.formName)

        #get form widgets and map it to objects
        self.frmMain = self.gladefile.get_widget(self.formName)
        self.frmMain.set_icon_from_file(common.APP_ICON)

        #Toolbar button widgets
        self.btnQuit = self.gladefile.get_widget('btnQuit')
        self.btnAdd = self.gladefile.get_widget('btnAdd')
        self.btnRemove = self.gladefile.get_widget('btnRemove')
        self.btnEdit = self.gladefile.get_widget('btnEdit')
        self.btnPaid = self.gladefile.get_widget('btnPaid')
        self.btnUnpaid = self.gladefile.get_widget('btnUnpaid')

        #menu widgets
        self.mnuAbout = self.gladefile.get_widget('mnuAbout')
        self.mnuQuit = self.gladefile.get_widget('mnuQuit')
        self.mnuAdd = self.gladefile.get_widget('mnuAdd')
        self.mnuEdit = self.gladefile.get_widget('mnuEdit')
        self.mnuPaid = self.gladefile.get_widget('mnuPaid')
        self.mnuUnpaid = self.gladefile.get_widget('mnuUnpaid')
        self.mnuRemove = self.gladefile.get_widget('mnuRemove')

        #status panel widgets
        self.lblCountPanel = self.gladefile.get_widget('lblCountPanel')
        self.lblInfoPanel = self.gladefile.get_widget('lblInfoPanel')

        #Get the treeView from the widget Tree
        self.billView = self.gladefile.get_widget("tvBills")

        # connect all handled signals to our procedures

        #form events
        self.frmMain.connect('delete_event', self.on_frmMain_destroy)
        self.frmMain.connect('destroy',gtk.main_quit)
        #buttons events
        self.btnQuit.connect('clicked',self.on_btnQuit_clicked)
        self.btnAdd.connect('clicked', self.on_btnAdd_clicked)
        self.btnEdit.connect('clicked', self.on_btnEdit_clicked)
        self.btnRemove.connect('clicked', self.on_btnRemove_clicked)
        self.btnPaid.connect('clicked', self.on_btnPaid_clicked)
        self.btnUnpaid.connect('clicked', self.on_btnPaid_clicked)
        #menus events
        self.mnuQuit.connect('activate',self.on_btnQuit_clicked)
        self.mnuAbout.connect('activate',self.on_mnuAbout_activate)
        self.mnuAdd.connect('activate',self.on_btnAdd_clicked)
        self.mnuEdit.connect('activate',self.on_btnEdit_clicked)
        self.mnuRemove.connect('activate',self.on_btnRemove_clicked)
        self.mnuPaid.connect('activate', self.on_btnPaid_clicked)
        self.mnuUnpaid.connect('activate', self.on_btnPaid_clicked)

        #set default variables values

        # Current record holder
        self.currentBill = None 
        #Bill ID holder
        self.bill_id = None 
        #Create the listStore Model to use with the treeView
        self.billList = gtk.ListStore(str, str, str, str, str, str) 

        #Here are some variables that can be reused later
        self.strId = 'Id'
        self.strPayee = 'Payee'
        self.strDueDate = 'Due Date'
        self.strAmountDue = 'Amount Due'
        self.strNotes = 'Notes'
        self.strPaid = 'Paid'

        #create objects variables

        # Connects to the database
        self.dal = DAL()

        # prepare the environment

        #set unused buttons to disable mode
        self.toggleButtons()

        #Formats the tree view
        self.formatTreeView()

        # and populate it
        self.populateTreeView(self.dal.get('paid IN (0,1)'))
        
        if len(self.billList) >0:
            self.billView.set_cursor(0)
        self.notify = NotifyIcon(self)
    
    def ShowHideWindow(self):
        if self.frmMain.get_property("visible"):
            self.frmMain.hide()
        else:
            self.frmMain.show()

    def toggleButtons(self, paid=None):
        """ Toggles all buttons conform number of records present and their state """
        if len(self.billList) > 0:
            self.btnEdit.set_sensitive(True)
            self.btnRemove.set_sensitive(True)
            """
            Enable/disable paid and unpiad buttons.
            If paid = True, paid button and menu will be enabled.
            """
            if paid:
                self.btnPaid.set_sensitive(False)
                self.btnUnpaid.set_sensitive(True)
                self.mnuPaid.set_sensitive(False)
                self.mnuUnpaid.set_sensitive(True)
            else:
                self.btnPaid.set_sensitive(True)
                self.btnUnpaid.set_sensitive(False)
                self.mnuPaid.set_sensitive(True)
                self.mnuUnpaid.set_sensitive(False)
        else:
            self.btnEdit.set_sensitive(False)
            self.btnRemove.set_sensitive(False)
            self.btnPaid.set_sensitive(False)
            self.btnUnpaid.set_sensitive(False)

    def formatTreeView(self):
        """ This functions prepares all the visual treeview issues used by the application. """
        #Add all of the List Columns to the treeView
        self.addBillListColumn(self.strId, self.COL_ID , 100, False)
        self.addBillListColumn(self.strPayee, self.COL_PAYEE, 160, True)
        self.addBillListColumn(self.strDueDate, self.COL_DUEDATE, 100, True)
        self.addBillListColumn(self.strAmountDue, self.COL_AMOUNTDUE, 100, True,1.0)
        self.addBillListColumn(self.strNotes, self.COL_NOTES, 100, False)
        self.addBillListColumn(self.strPaid, self.COL_PAID, 100, False)

        #Attache the model to the treeView
        self.billView.set_model(self.billList)
        self.billView.set_rules_hint(True)
        
        self.billView.connect('cursor_changed', self.on_billView_cursor_changed)
        self.billView.connect('button_press_event', self.on_billView_button_press_event)
        self.billList.connect('row-deleted', self.on_billview_row_deleted)
        self.billList.connect('row-inserted', self.on_billview_row_inserted)
        # add double click and on insert event handles
        #self.billView.connect()

        
    def addBillListColumn(self, title, columnId, size=100, visible=True, xalign = 0.0):
        """ This function adds a column to the list view.
        First it creates the gtk.TreeViewColumn and then sets
        some needed properties """

        renderer = gtk.CellRendererText()
        renderer.set_property('xalign', xalign)
        column = gtk.TreeViewColumn(title, renderer , text=columnId)
        column.set_resizable(True)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_min_width(size)
        column.set_clickable(True)
        column.set_visible(visible)
        column.set_sort_column_id(columnId)

        self.billView.append_column(column)
    
    def formatedRow(self, row):
        """ Formats a bill to be displayed as a row. """
    
        # Format the dueDate field
        dueDate = datetime.datetime.fromtimestamp(row['DueDate'])
        row['DueDate'] = dueDate.strftime('%Y/%m/%d')
        # Format the amount field
        amountDue = "%0.2f" % float(row['AmountDue'])
        row['AmountDue'] = amountDue

        formated = [row['Id'], row['Payee'], row['DueDate'], row['AmountDue'], row['Notes'], row['Paid']]
        return formated
    
    def updateStatusBar(self, index=0):
        """ This function is used to update status bar informations about the list"""
        self.lblInfoPanel.set_text('')
        self.lblCountPanel.set_text('%d' % len(self.billList))
        #if len(self.billList) > 0:
        #    self.billView.set_cursor(index)

    def populateTreeView(self, records):
        """ Populates the treeview control with the records passed """
        # Loops through bills collection
        for rec in records:
            try:
                self.billList.append(self.formatedRow(rec.Dictionary))
            except:
                #better show a DialogBox here if  the error is something crucial
                print "Unexpected error:", sys.exc_info()[0]
        # update statusbar information
        self.updateStatusBar()
        return

    # Event handlers
    
    def on_billview_row_deleted(self, model, path):
        """ 
            This function will handle the signal to update buttons and menus depending of list content.
         """
        self.toggleButtons()
    
    def on_billview_row_inserted(self, model, path, iter):
        """ 
            This function will handle the signal to update buttons and menus depending of list content.
        """
        self.billView.get_selection().select_iter(iter)
        self.billView.scroll_to_cell(path,self.billView.get_column(0))
        #self.billView.row_activated(path,self.billView.get_column(0) )
        self.toggleButtons()
    
    def on_btnQuit_clicked(self, widget):
        """ 
            This function will handle the signal to close window sent by 
            bntQuit and mnuQuit widgets.
         """
        self.on_frmMain_destroy()

    def on_btnAdd_clicked(self, widget):
        """ 
            This function will handle the signal to add a new bill sent by 
            bntAdd and mnuAdd widgets.
         """
        self.addBill()
        self.updateStatusBar()

    def on_btnEdit_clicked(self, widget):
        """ 
            This function will handle the signal to edit the selected bill sent by 
            bntEdit and mnuEdit widgets.
         """
        self.editBill()

    def on_btnPaid_clicked(self, widget):
        """ 
            This function will handle the signal to set select bill as paid sent by 
            bntPaid and mnuPaid widgets.
         """
        self.payBill()

    def on_btnRemove_clicked(self, *args):
        """ 
            This function will handle the signal to remove a bill sent by 
            bntremove and mnuRemove widgets.
        """
        bill = self.getBill()[1]
        strMsg = 'do you really want to remove it?\n\n <b>%s - %0.2f </b>' % (bill.Payee,float(bill.AmountDue))
        result = Message().ShowQuestionOkCancel(strMsg, self.frmMain)
        if result:
            self.removeBill()

    def on_mnuAbout_activate(self, widget):
        """ 
            This function will handle the signal to show an about window sent by mnuAbout widget.
        """
        frmAbout = AboutDialog(self.gladefilename)
        frmAbout.run()

    def on_billView_button_press_event(self, widget, event):
        """ 
            This function will handle the signal to show a popup menu sent by 
            a right click on tvBill widget.
        """
        if event.button == 3 and event.type == gtk.gdk.BUTTON_PRESS and len(self.billList) > 0:
            
            path = self.billView.get_path_at_pos(int(event.x),int(event.y))
            
            selection = self.billView.get_selection()
            
            # Get the selected path(s)
            rows = selection.get_selected_rows()[0]
            if path[0] not in rows[1]:
                selection.unselect_all()
                selection.select_path(path[0])
            
            model, iteration = selection.get_selected()
            paid = (model.get_value(iteration, 5) == str(1))

            c = ContextMenu(self)
            c.addMenuItem('Add New', self.on_btnAdd_clicked, gtk.STOCK_ADD)
            c.addMenuItem('-', None)
            c.addMenuItem('Remove',self.on_btnRemove_clicked ,gtk.STOCK_REMOVE)
            c.addMenuItem('Edit', self.on_btnEdit_clicked, gtk.STOCK_EDIT)
            c.addMenuItem('-', None)
            if not paid:
                c.addMenuItem('Paid', self.on_btnPaid_clicked ,gtk.STOCK_APPLY,True)
            else:
                c.addMenuItem('set Open', self.on_btnPaid_clicked ,gtk.STOCK_UNDO,True)
            c.addMenuItem('-', None)
            c.addMenuItem('Cancel', None,gtk.STOCK_CANCEL)
            c.popup(None, None, None, event.button, event.get_time())

    def on_billView_cursor_changed(self, widget):
        """ 
            This function will handle the signal sent by tvBill widget
            when a row is selected and displays the selected record information 
        """
        try:
            sel = widget.get_selection()
            model, iteration = sel.get_selected()

            #b_id = model.get_value(iteration, 0)
            notes = model.get_value(iteration, 4)
            paid = model.get_value(iteration, 5)

            # Display the status for the selected row
            self.lblInfoPanel.set_text('%s' % (notes))
            self.toggleButtons(int(paid))
        except:
            # better show a dialog box here if erro is critical
            pass 
        
    def on_frmMain_destroy(self, *event):
        self.frmMain.set_sensitive(False)
        dialog = gtk.MessageDialog(self.frmMain,
                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, None)
        dialog.set_markup('<big><b>Are you sure you want to quit?</b></big>')
        dialog.connect("destroy", lambda w: self.frmMain.set_sensitive(True))
        answer = dialog.run()
        if answer == gtk.RESPONSE_YES:
            dialog.destroy()
            if len(event)==0:
                gtk.main_quit()
            return False

        if answer == gtk.RESPONSE_NO:
            dialog.destroy()
            return True

    # Business code
    def addBill(self):
        """
            Function used to add a new bew to the database.
            This will show a dialog where the user could add
            some info about the bill.
        """
        # Displays the Bill dialog
        frmBillDialog = BillDialog(None, parent=self.frmMain)
        response, bill = frmBillDialog.run()

        # Checks if the user did not cancel the action
        if (response == gtk.RESPONSE_OK):
            # Add new bill to database
            bill = self.dal.add(bill)
            if bill:
                self.billList.append(self.formatedRow(bill.Dictionary))
                self.updateStatusBar()

    def editBill(self):
        """
            Function used to persist changes made to the bill
        """
        # Get currently selected bill
        b_id,bill = self.getBill()
        # Displays the Bill dialog
        frmBillDialog = BillDialog(bill, parent=self.frmMain)
        response, bill = frmBillDialog.run()

        # Checks if the user did not cancel the action
        if (response == gtk.RESPONSE_OK):
            try:
                # Edit bill in the database
                self.dal.edit(b_id, bill)
                # Update list with updated record
                idx = self.billView.get_cursor()[0][0]
                self.billList[idx] = self.formatedRow(bill.Dictionary)
                self.updateStatusBar(idx)
            except:
                #better show a dialog window to this error
                print "Unexpected error:", sys.exc_info()[0]

    def payBill(self):
        """ 
            Toggles bill as paid/unpaid 
        """
        # Get currently selected bill and its id
        b_id, bill = self.getBill()

        print bool(bill.Paid)
        # Toggle paid field
        if bill.Paid:
            bill.Paid = 0
        else:
            bill.Paid = 1

        try:
            # Edit bill in the database
            self.dal.edit(b_id, bill)
            # Update list with updated record
            idx = self.billView.get_cursor()[0][0]
            self.billList[idx] = self.formatedRow(bill.Dictionary)
            self.updateStatusBar(idx)
        except:
            #better show a dialog window to this error
            print "Unexpected error:", sys.exc_info()[0]

    def removeBill(self):
        """
            Function used to remove a bill from the database.
        """
        b_id,bill = self.getBill()
        sel = self.billView.get_selection()
        model, iteration = sel.get_selected()
        try:
            ret = self.dal.delete(b_id)
 
            if ret.rowcount == 1:
                self.billList.remove(iteration)
                msg = ('The following bill was removed:\n' + bill.Payee)
                self.notify.show_message('Item deleted.',msg)
                self.updateStatusBar()
            else:
                Message().ShowError("Bill '%s' not deleted." % bill.Payee , self.frmMain)
        except:
            Message().ShowError(str(sys.exc_info()[0]), self.frmMain)

    def getBill(self):
        """ 
            Returns a bill object from the current selected record 
        """
        sel = self.billView.get_selection()
        model, iteration = sel.get_selected()

        b_id = model.get_value(iteration, 0)

        records = self.dal.get({'Id': b_id})
        # Return bill and id
        return b_id, records[0]
