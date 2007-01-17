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
        print 'showing message'
        notif = NotifyMessage()
        notif.AppName('BillReminder')
        notif.Title(title)
        notif.Body(msg)
        notif.Icon("/usr/share/pixmaps/esc.png")
        notif.Timeout(7)
        print 'got here'
        notif.Notify() 
        print 'message showed'
 
class NotifyMessage:
    """ This classes handle a way to show messagens 
        using a baloon style in notification area.
    """
    
    def __init__(self):
        """Constructor """
        self.__app_name = "BillReminder"
        self.__replaces_id = 0
        self.__app_icon = ""
        self.__summary = ""
        self.__body = ""
        self.__actions = []
        self.__hints = {}
        self.__expire_timeout = 1000
        
        try:
            __session_bus = dbus.SessionBus()
            __obj = __session_bus.get_object("org.freedesktop.Notifications","/org/freedesktop/Notifications")
            self.__interface = dbus.Interface(__obj, "org.freedesktop.Notifications")
        except Exception:
            self.__interface = None
        
    def AppName(self, app_name):
        self.__app_name = app_name
 
    def Ids(self, replaces_id):
        self.__replaces_id = replaces_id
 
    def Icon(self, app_icon):
        self.__app_icon = app_icon
 
    def Title(self, summary):
        self.__summary = summary
 
    def Body(self, body):
        self.__body = body
 
    def AddAction(self, action):
        t.append(action)
 
    def Timeout(self, expire_timeout):
        self.__expire_timeout = expire_timeout * 1000
 
    def MSTimeout(self, expire_timeout):
        self.__expire_timeout = expire_timeout
 
    def Notify(self):
        if self.__interface:
            self.__interface.Notify(self.__app_name, self.__replaces_id, self.__app_icon, self.__summary, self.__body, self.__actions, self.__hints, self.__expire_timeout)
         
        