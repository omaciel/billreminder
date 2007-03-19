#!/usr/bin/python
# -*- coding: utf-8 -*-

__all__ = ['AboutDialog']

import sys
try:
    import pygtk
    pygtk.require("2.0")
except:
      pass
try:
    import gtk
    import gtk.glade
    import os
    import gobject
    import common
except:
    sys.exit(1)

class AboutDialog:
    """ This is the About dialog window """
    
    def __init__(self):

        #Set the Glade file
        self.gladefile = gtk.glade.XML(common.ABOUTGLADEFILE, common.ABOUTDIALOG_NAME, domain='billreminder')

        #get form widgets and map it to objects
        #Get the actual dialog widget
        self.frmAbout = self.gladefile.get_widget(common.ABOUTDIALOG_NAME)
        self.frmAbout.set_position(gtk.WIN_POS_CENTER)
        self.frmAbout.set_modal(True)
        self.frmAbout.set_icon(gtk.gdk.pixbuf_new_from_file(common.APP_ICON))
        self.frmAbout.set_logo(gtk.gdk.pixbuf_new_from_file(common.APP_HEADER))
        self.frmAbout.set_name(_("BillReminder"))

    def run(self):
        """This function will show the aboutDialog"""

        #run the dialog and store the response      
        result = self.frmAbout.run()

        #we are done with the dialog, destroy it
        self.frmAbout.destroy()

        #return the result
        return  result  
        
