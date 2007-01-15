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
    import os
    import gobject
    import common
except:
    sys.exit(1)

class AboutDialog:
    """ This is the About dialog window """
    def __init__(self, gladefile):

        #Set the Glade file
        self.gladefile = gtk.glade.XML(common.ABOUTGLADEFILE, common.ABOUTDIALOG_NAME)

        # Header image
        image = gtk.Image()
        image.set_from_file(common.APP_HEADER)
        logo =  gtk.gdk.Pixbuf()

        #get form widgets and map it to objects
        #Get the actual dialog widget
        frmAbout = self.gladefile.get_widget(common.ABOUTDIALOG_NAME)
        frmAbout.set_position(gtk.WIN_POS_CENTER)
        frmAbout.set_modal(True)
        frmAbout.set_logo =  logo.get_from_image(image)

    def run(self):
        """This function will show the aboutDialog"""

        #run the dialog and store the response      
        result = frmAbout.run()

        #we are done with the dialog, destroy it
        frmAbout.destroy()

        #return the result
        return  result  
