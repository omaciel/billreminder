#!/usr/bin/python
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
