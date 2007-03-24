#!/usr/bin/python
# -*- coding: utf-8 -*-

__all__ = ['NotifyIcon', 'NotifyMessage']

try:
    import pynotify
except ImportError:
    print "Please install pynotify"
    sys.exit(1)

import os
import gtk
import gobject
import dbus
import sys
import time
import common
from controller.utils import ContextMenu

class NotifyIcon:
    """ This class creates the tray icon notification - GTK 2.10 or above """
    
    def __init__(self,parent):
        """ Constructor """
        
        self.parent = parent
        
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
        c = ContextMenu(self)
        if self.parent.get_window_visibility():
            c.addMenuItem(_('Hide Window'), self.show_hide)
        else:
            c.addMenuItem(_('Show Window'), self.show_hide)
        
        c.addMenuItem('-', None)
        c.addMenuItem(_('Quit'), self.parent.on_btnQuit_clicked,gtk.STOCK_QUIT)
        
        print type(activate_time)
        c.popup(None, None, None, button, activate_time)
        del c    
        #self.menu.popup(None, None, None, button, activate_time)
        
    def destroy(self):
        """ Hide the systray icon. """
        self.tray.set_visible(False)
            
    def exists(self):
        """ Do nothing here, only returns that the class was instantiated."""
        return True
        
    def show_message(self, title, msg, timeout=7, icon="/usr/share/pixmaps/esc.png"): # TODO: Change image
        """ Show a message in notification area using gnome dbus objects. """
        print 'showing message'
        notif = NotifyMessage()
        notif.AppName('BillReminder')
        notif.Title(title)
        notif.Body(msg)
        notif.Icon(icon)
        notif.Timeout(timeout)
        notif.getHints(self.tray)
        print 'got here'
        notif.Notify() 
        print 'message showed'
 
class NotifyMessage:
    """ This classes handle a way to show messagens 
        using a baloon style in notification area. """
    
    def __init__(self):
        """ Constructor """
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
            __obj = __session_bus.get_object("org.freedesktop.Notifications", "/org/freedesktop/Notifications")
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
        self.__actions.append(action)
 
    def Timeout(self, expire_timeout):
        self.__expire_timeout = expire_timeout * 1000
 
    def MSTimeout(self, expire_timeout):
        self.__expire_timeout = expire_timeout
    
    def getHints(self, tray):
        hints = {}
        if tray:
           x = tray.get_geometry()[1].x
           y = tray.get_geometry()[1].y
           w = tray.get_geometry()[1].width
           h = tray.get_geometry()[1].height
           x += w/2
           if y < 100:
              # top-panel
              y += h/2
           else:
              # bottom-panel
              y -= h/2
           hints['x'] = x
           hints['y'] = y
        hints['desktop-entry'] = "billreminder"
        self.__hints = hints
        return hints
 
    def Notify(self):
        if self.__interface:
            self.__interface.Notify(self.__app_name, self.__replaces_id, self.__app_icon, self.__summary, self.__body, self.__actions, self.__hints, self.__expire_timeout)
