#!/usr/bin/python
# -*- coding: utf-8 -*-

__all__ = ['BillReminderView']

#default python imports
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
#custom imports
import common


class BillReminderView:
    
    def __init__(self):
        """ BillReminder constructor. """

        # Set the Glade file
        self.gladefilename = common.MAINGLADEFILE
        self.formName = common.MAINFORM_NAME
        self.gladefile = gtk.glade.XML(self.gladefilename, self.formName, domain='billreminder')

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
        self.mnubPanel = self.gladefile.get_widget('mnubPanel')

        #menu widgets
        self.mnuAbout = self.gladefile.get_widget('mnuAbout')
        self.mnuQuit = self.gladefile.get_widget('mnuQuit')
        self.mnuAdd = self.gladefile.get_widget('mnuAdd')
        self.mnuEdit = self.gladefile.get_widget('mnuEdit')
        self.mnuPaid = self.gladefile.get_widget('mnuPaid')
        self.mnuUnpaid = self.gladefile.get_widget('mnuUnpaid')
        self.mnuRemove = self.gladefile.get_widget('mnuRemove')
        self.mnuViewPaid = self.gladefile.get_widget('mnuViewPaid')
        self.mnubPanel = self.gladefile.get_widget('mnubPanel')

        #status panel widgets
        self.lblCountPanel = self.gladefile.get_widget('lblCountPanel')
        self.lblInfoPanel = self.gladefile.get_widget('lblInfoPanel')
        
        #bottom panel widgets
        self.bPanel = self.gladefile.get_widget('bPanel')
        self.lblbPanelPayee = self.gladefile.get_widget('lblbPanelPayee')
        self.lblbPanelAmount = self.gladefile.get_widget('lblbPanelAmount')
        self.lblbPanelDuedate = self.gladefile.get_widget('lblbPanelDuedate')
        self.lblbPanelNote = self.gladefile.get_widget('lblbPanelNote')
        self.lblbPanelPaid = self.gladefile.get_widget('lblbPanelPaid')
        self.imgbPanelIcon = self.gladefile.get_widget('imgbPanelIcon')
        self.imgbPanelIconPlus = self.gladefile.get_widget('imgbPanelIconPlus')


        #Get the treeView from the widget Tree
        self.billView = self.gladefile.get_widget("tvBills")

    def confirmQuit(self, str):
        dialog = gtk.MessageDialog(self.frmMain,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, None)
        dialog.set_markup(str)
        dialog.connect("destroy", lambda w: self.frmMain.set_sensitive(True))
        ret = dialog.run()
        dialog.destroy()
        return ret
        
