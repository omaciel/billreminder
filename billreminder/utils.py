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
    import datetime
except:
    sys.exit(1)

class ContextMenu(gtk.Menu):
    """ Creates context menus accessed by mouse right click. """
    def __init__(self, *args):
        gtk.Menu.__init__(self)
        self.menuItem = None
    
    def addMenuItem(self, menuName, actionFunction=None, menuImage=None, forceName=False):
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

class Message:
    """ Generic prompt dialog """
    def ShowQuestionOkCancel(self,text, parentWindow= None, title = ''):
        dlg = gtk.MessageDialog (parentWindow, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, text)
        if title == '':
            dlg.set_title('Question')
        else:
            dlg.set_title(title)
            
        dlg.set_markup(text)
        response = dlg.run ()
        dlg.destroy ()
        return (response == gtk.RESPONSE_YES)
    
    def ShowError(self,text, parentWindow= None, title = ''):
        dlg= gtk.MessageDialog(parentWindow, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, text)
        if title == '':
            dlg.set_title('Error')
        else:
            dlg.set_title(title)
            
        dlg.set_markup(text)
        dlg.run()
        dlg.destroy ()
        return 

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
    return datetime.date(dtPieces[0], dtPieces[1], dtPieces[2])
