#!/usr/bin/python
# -*- coding: utf-8 -*-

__all__ = ['BillReminder']

#default python imports
import sys
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
import datetime
import os
import gobject
import dbus
import time

#custom imports
import common
import model.i18n
from model.dbus_manager import BillDBus
from model.dal import DAL
from model.bill import Bill
from controller.aboutdialog import AboutDialog
from controller.billdialog import BillDialog
from controller.trayicon import NotifyIcon
from controller.utils import ContextMenu, Message
import controller.utils

class BillReminder:
    """ This is the main window of the application """

    # set global columns ids for bills tree constants 
    (COL_ICON, COL_ID, COL_PAYEE, COL_DUEDATE, COL_AMOUNTDUE, COL_NOTES, COL_PAID) = range(7) 

    def __init__(self, view):
        
        self.view = view
                
        # connect all handled signals to our procedures

        #form events
        self.view.frmMain.connect('delete_event', self.on_frmMain_destroy)
        self.view.frmMain.connect('destroy', gtk.main_quit)
        #buttons events
        self.view.btnQuit.connect('clicked',self.on_btnQuit_clicked)
        self.view.btnAdd.connect('clicked', self.on_btnAdd_clicked)
        self.view.btnEdit.connect('clicked', self.on_btnEdit_clicked)
        self.view.btnRemove.connect('clicked', self.on_btnRemove_clicked)
        self.view.btnPaid.connect('clicked', self.on_btnPaid_clicked)
        self.view.btnUnpaid.connect('clicked', self.on_btnPaid_clicked)
        #menus events
        self.view.mnuQuit.connect('activate', self.on_btnQuit_clicked)
        self.view.mnuAbout.connect('activate', self.on_mnuAbout_activate)
        self.view.mnuAdd.connect('activate', self.on_btnAdd_clicked)
        self.view.mnuEdit.connect('activate', self.on_btnEdit_clicked)
        self.view.mnuRemove.connect('activate', self.on_btnRemove_clicked)
        self.view.mnuPaid.connect('activate', self.on_btnPaid_clicked)
        self.view.mnuUnpaid.connect('activate', self.on_btnPaid_clicked)

        #set default variables values

        # Current record holder
        self.currentBill = None 
        #Bill ID holder
        self.bill_id = None 
        #Create the listStore Model to use with the treeView
        self.billList = gtk.ListStore(gtk.gdk.Pixbuf, str, str, str, str, str, str) 

        #Here are some variables that can be reused later
        self.strId = _('Id')
        self.strPayee = _('Payee')
        self.strDueDate = _('Due Date')
        self.strAmountDue = _('Amount Due')
        self.strNotes = _('Notes')
        self.strPaid = _('Paid')

        #create objects variables

        # Connects to the database
        self.dal = DAL()
        
        self.table = 'tblbills'

        # prepare the environment

        #set unused buttons to disable mode
        self.toggleButtons()

        #Formats the tree view
        self.formatTreeView()

        # and populate it
        self.populateTreeView(self.dal.get(self.table, 'paid IN (0,1)'))
        
        if len(self.billList) > 0:
            self.view.billView.set_cursor(0)
        self.notify = NotifyIcon(self)
        
        self.dbus_service = BillDBus(self)
        # Launch Daemon
        gobject.timeout_add(10, os.system, 'python -OO notifier.py')
    
    def get_window_visibility(self):
        return self.view.frmMain.get_property("visible")
    
    def ShowHideWindow(self):
        if self.view.frmMain.get_property("visible"):
            self.view.frmMain.hide()
        else:
            self.view.frmMain.show()

    def toggleButtons(self, paid=None):
        """ Toggles all buttons conform number of records present and their state """
        if len(self.billList) > 0:
            self.view.btnEdit.set_sensitive(True)
            self.view.btnRemove.set_sensitive(True)
            self.view.mnuEdit.set_sensitive(True)
            self.view.mnuRemove.set_sensitive(True)
            """
            Enable/disable paid and unpiad buttons.
            If paid = True, paid button and menu will be enabled.
            """
            if paid:
                self.view.btnPaid.set_sensitive(False)
                self.view.btnUnpaid.set_sensitive(True)
                self.view.mnuPaid.set_sensitive(False)
                self.view.mnuUnpaid.set_sensitive(True)
            else:
                self.view.btnPaid.set_sensitive(True)
                self.view.btnUnpaid.set_sensitive(False)
                self.view.mnuPaid.set_sensitive(True)
                self.view.mnuUnpaid.set_sensitive(False)
        else:
            self.view.btnEdit.set_sensitive(False)
            self.view.btnRemove.set_sensitive(False)
            self.view.btnPaid.set_sensitive(False)
            self.view.btnUnpaid.set_sensitive(False)
            self.view.mnuEdit.set_sensitive(False)
            self.view.mnuRemove.set_sensitive(False)
            self.view.mnuPaid.set_sensitive(False)
            self.view.mnuUnpaid.set_sensitive(False)

    def formatTreeView(self):
        """ This functions prepares all the visual treeview issues used by the application. """
        #Add all of the List Columns to the treeView
        self.addBillListColumn(self.strPaid, self.COL_ICON, 20, True) 
        self.addBillListColumn(self.strId, self.COL_ID , 100, False)
        self.addBillListColumn(self.strPayee, self.COL_PAYEE, 260, True)
        self.addBillListColumn(self.strDueDate, self.COL_DUEDATE, 100, True)
        self.addBillListColumn(self.strAmountDue, self.COL_AMOUNTDUE, 100, True, 1.0)
        self.addBillListColumn(self.strNotes, self.COL_NOTES, 100, False)
        self.addBillListColumn(self.strPaid, self.COL_PAID, 100, False)

        #Attache the model to the treeView
        self.view.billView.set_model(self.billList)
        self.view.billView.set_rules_hint(True)
        
        self.view.billView.connect('cursor_changed', self.on_billView_cursor_changed)
        self.view.billView.connect('button_press_event', self.on_billView_button_press_event)
        self.billList.connect('row-deleted', self.on_billview_row_deleted)
        self.billList.connect('row-inserted', self.on_billview_row_inserted)
        # add double click and on insert event handles
        #self.billView.connect()

        
    def addBillListColumn(self, title, columnId, size=100, visible=True, xalign=0.0):
        """ This function adds a column to the list view.
        First it creates the gtk.TreeViewColumn and then sets
        some needed properties """
        
        if columnId == self.COL_ICON: 
            renderer = gtk.CellRendererPixbuf() 
        else: 
            renderer = gtk.CellRendererText()
        renderer.set_property('xalign', xalign)
        column = gtk.TreeViewColumn(title, renderer, text=columnId)
        column.set_resizable(True)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_min_width(size)
        column.set_clickable(True)
        column.set_visible(visible)
        column.set_alignment(xalign)
        column.set_sort_column_id(columnId)
        
        if columnId == self.COL_ICON: 
            self.view.billView.insert_column_with_data_func(-1, '', renderer, self.pixbufCellDataFunc) 
        else: 
            self.view.billView.append_column(column)
    
    def formatedRow(self, row):
        """ Formats a bill to be displayed as a row. """
        # Format the dueDate field
        dueDate = datetime.datetime.fromtimestamp(row['dueDate'])
        # TRANSLATORS: This is a date format. You can change the order.
        row['dueDate'] = dueDate.strftime(_('%Y/%m/%d').encode('ASCII'))
        # Format the amount field
        amountDue = "%0.2f" % float(row['amountDue'])
        row['amountDue'] = amountDue
        
        formated = [None, row['Id'], row['payee'], row['dueDate'], row['amountDue'], row['notes'], row['paid']] 
        return formated
    
    def updateStatusBar(self, index=0):
        """ This function is used to update status bar informations about the list """
        self.view.lblInfoPanel.set_text('')
        self.view.lblCountPanel.set_text('%d' % len(self.billList))
        if len(self.billList) > 0:
            self.view.billView.set_cursor(index)

    def populateTreeView(self, records):
        """ Populates the treeview control with the records passed """
        
        # Loops through bills collection
        for rec in records:
            try:
                bill = Bill(rec)
                self.billList.append(self.formatedRow(bill.Dictionary))
            except:
                #better show a DialogBox here if  the error is something crucial
                print "Unexpected error:", sys.exc_info()[0]
        # update statusbar information
        self.updateStatusBar()
        return

    def pixbufCellDataFunc(self, tree_column, cell, model, tree_iter):
        """ Draw icon """
        if model.get_value(tree_iter, self.COL_PAID) == '1':
            stock_id = 'gtk-apply'
        else:
            stock_id = ''
        cell.set_property('stock-id', stock_id)

    # Event handlers
    
    def on_billview_row_deleted(self, model, path):
        """ This function will handle the signal to update buttons and menus depending of list content. """
        self.toggleButtons()
    
    def on_billview_row_inserted(self, model, path, iter):
        """ This function will handle the signal to update buttons and menus depending of list content. """
        self.view.billView.get_selection().select_iter(iter)
        self.view.billView.scroll_to_cell(path,self.view.billView.get_column(0))
        #self.billView.row_activated(path,self.billView.get_column(0))
        self.toggleButtons()
    
    def on_btnQuit_clicked(self, widget):
        """ This function will handle the signal to close window sent by 
            bntQuit and mnuQuit widgets. """
        self.on_frmMain_destroy()

    def on_btnAdd_clicked(self, widget):
        """ This function will handle the signal to add a new bill sent by 
            bntAdd and mnuAdd widgets. """
        self.addBill()

    def on_btnEdit_clicked(self, widget):
        """ This function will handle the signal to edit the selected bill sent by 
            bntEdit and mnuEdit widgets. """
        self.editBill()

    def on_btnPaid_clicked(self, widget):
        """ This function will handle the signal to set select bill as paid sent by 
            bntPaid and mnuPaid widgets. """
        self.payBill()

    def on_btnRemove_clicked(self, *args):
        """ This function will handle the signal to remove a bill sent by 
            bntremove and mnuRemove widgets. """
        bill = self.getBill()[1]
        # TRANSLATORS: Don't translate words inside parentheses!
        strMsg = _('do you really want to remove it?\n\n <b>%(payee)s - %(amount)0.2f </b>') %  \
            {'payee': bill.Payee, 'amount': float(bill.AmountDue)}
        result = Message().ShowQuestionOkCancel(strMsg, self.view.frmMain)
        print result
        if result:
            self.removeBill()

    def on_mnuAbout_activate(self, widget):
        """ This function will handle the signal to show an about window sent by mnuAbout widget. """
        frmAbout = AboutDialog()
        frmAbout.run()

    def on_billView_button_press_event(self, widget, event):
        """ This function will handle the signal to show a popup menu sent by 
            a right click on tvBill widget. """
        if event.button == 3 and event.type == gtk.gdk.BUTTON_PRESS and len(self.billList) > 0:
            
            path = self.view.billView.get_path_at_pos(int(event.x), int(event.y))
            
            selection = self.view.billView.get_selection()
            
            # Get the selected path(s)
            try:
                rows = selection.get_selected_rows()[0]
                if path[0] not in rows[0]:
                    selection.unselect_all()
                    selection.select_path(path[0])
                
                model, iteration = selection.get_selected()
                paid = (model.get_value(iteration, self.COL_PAID) == str(1))
                error = False
            except:
                error = True
                pass

            c = ContextMenu(self)
            c.addMenuItem(_('Add New'), self.on_btnAdd_clicked, gtk.STOCK_NEW)
            c.addMenuItem('-', None)
            if not error:
                c.addMenuItem(_('Remove'), self.on_btnRemove_clicked, gtk.STOCK_DELETE)
                c.addMenuItem(_('Edit'), self.on_btnEdit_clicked, gtk.STOCK_EDIT)
                c.addMenuItem('-', None)
                if not paid:
                    c.addMenuItem(_('Paid'), self.on_btnPaid_clicked, gtk.STOCK_APPLY, True)
                else:
                    c.addMenuItem(_('Not Paid'), self.on_btnPaid_clicked, gtk.STOCK_UNDO, True)
                c.addMenuItem('-', None)
            c.addMenuItem(_('Cancel'), None, gtk.STOCK_CANCEL)
            c.popup(None, None, None, event.button, event.get_time())

    def on_billView_cursor_changed(self, widget):
        """ This function will handle the signal sent by tvBill widget
            when a row is selected and displays the selected record information """
        try:
            sel = widget.get_selection()
            model, iteration = sel.get_selected()

            #b_id = model.get_value(iteration, 0)
            notes = model.get_value(iteration, self.COL_NOTES)
            paid = model.get_value(iteration, self.COL_PAID)

            # Display the status for the selected row
            self.view.lblInfoPanel.set_text('%s' % (notes))
            self.toggleButtons(int(paid))
        except:
            # better show a dialog box here if erro is critical
            pass 
        
    def on_frmMain_destroy(self, *event):
        self.view.frmMain.set_sensitive(False)
        answer = self.view.confirmQuit(_('<big><b>Are you sure you want to quit?</b></big>'))
        if answer == gtk.RESPONSE_YES:
            if len(event) == 0:
                gtk.main_quit()
            return False

        if answer == gtk.RESPONSE_NO:
            return True

    # Business code
    def addBill(self):
        """ Function used to add a new bew to the database.
            This will show a dialog where the user could add
            some info about the bill. """
        # Displays the Bill dialog
        frmBillDialog = BillDialog(None, parent=self.view.frmMain)
        response, bill = frmBillDialog.run()

        # Checks if the user did not cancel the action
        if response == gtk.RESPONSE_OK:
            # Add new bill to database
            bill = self.dal.add(self.table, bill.Dictionary)
            if bill:
                self.billList.append(self.formatedRow(bill))
                self.updateStatusBar()

    def editBill(self):
        """ Function used to persist changes made to the bill """
        # Get currently selected bill
        b_id,bill = self.getBill()
        # Displays the Bill dialog
        frmBillDialog = BillDialog(bill, parent=self.view.frmMain)
        response, bill = frmBillDialog.run()
        # Checks if the user did not cancel the action
        if response == gtk.RESPONSE_OK:
            try:
                # Edit bill in the database
                self.dal.edit(self.table, b_id, bill.Dictionary)
                # Update list with updated record
                idx = self.view.billView.get_cursor()[0][0]
                self.billList[idx] = self.formatedRow(bill.Dictionary)
                print idx
                self.updateStatusBar(idx)
                self.toggleButtons(int(bill.Dictionary['paid']))
            except Exception, e:
                #better show a dialog window to this error
                print "Unexpected error:", sys.exc_info()[0]
                print str(e)

    def payBill(self):
        """ Toggles bill as paid/unpaid """
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
            self.dal.edit(self.table, b_id, bill.Dictionary)
            # Update list with updated record
            idx = self.view.billView.get_cursor()[0][0]
            self.billList[idx] = self.formatedRow(bill.Dictionary)
            self.updateStatusBar(idx)
            self.toggleButtons(bill.Paid)
        except:
            #better show a dialog window to this error
            print "Unexpected error:", sys.exc_info()[0]

    def removeBill(self):
        """ Function used to remove a bill from the database. """
        b_id, bill = self.getBill()
        sel = self.view.billView.get_selection()
        model, iteration = sel.get_selected()
        try:
            ret = self.dal.delete(self.table, b_id)
 
            if ret:
                self.billList.remove(iteration)
                msg = (_('The following bill was removed:\n') + '<b>%(payee)s</b> - <i>%(amountDue)0.2f</i>' \
                    % dict(payee=bill.Payee, amountDue=bill.AmountDue))
                self.notify.show_message(_('Item deleted.'), msg)
                self.updateStatusBar()
            else:
                Message().ShowError(_("Bill '%s' not deleted.") % bill.Payee, self.view.frmMain)
        except Exception, e:
            # Debug message error
            print str(e)
            Message().ShowError(str(sys.exc_info()[0]), self.view.frmMain)

    def getBill(self):
        """ Returns a bill object from the current selected record """
        sel = self.view.billView.get_selection()
        _model, iteration = sel.get_selected()
        
        b_id = _model.get_value(iteration, self.COL_ID)
        
        records = self.dal.get(self.table, {'Id': b_id})
        rec = records[0]
        
        # Return bill and id
        Bill(rec)
        return b_id, Bill(rec)
        
