import os
import gtk
import gobject
import dbus
import sys
import time
import pynotify
import common

class NotifyIcon:
    "This class creates the tray icon notification - GTK 2.10 or above"
    
    def __init__(self,parent):
        """ Constructor """
        
        self.parent = parent
        self.wTree = gtk.glade.XML(common.TRAYGLADEFILE)
        self.menu = self.wTree.get_widget("TrayMenu")
       
        #connecting signals
        dic = { "on_mnuShow_activate"    : self.show_hide,
                "on_mnuQuit_activate"    : self.parent.on_btnQuit_clicked
              }
        self.wTree.signal_autoconnect(dic)
        
        #show the icon
        self.start()

    def start(self):
        """ Function used to show an icon in notification area."""
        
        self.tray = gtk.StatusIcon()
        self.tray.set_from_file(common.APP_ICON)
        self.tray.set_tooltip("BillReminder")
        self.tray.connect("popup-menu", self.show_menu, None)
        self.tray.connect("activate", self.show_hide, None)
        
    def show_hide(self, status_icon, arg=None):
        """ Show and Hide the main window. """
        self.parent.ShowHideWindow()
        
    def show_menu(self, status_icon, button, activate_time, arg0=None):
        """ Show a popup menu when an user right clicks notification area icon."""
        self.menu.popup(None, None, None, button, activate_time)
        
    def destroy(self):
        """ Hide the systray icon. """
        self.tray.set_visible(False)
            
    def exists(self):
        """ Do nothing here, only returns that the class was instantiated."""
        return True
    def show_message(self,title, msg):
        """ Show a message in notification area using gnome dbus objects. """
        if not pynotify.init("Images Test"):
            return
        uri = "file://" + common.IMAGE_PATH + "applet-critical.png"
        n = pynotify.Notification(title,msg,uri)
        n.show()
 