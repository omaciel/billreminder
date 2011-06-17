# -*- coding: utf-8 -*-

__all__ = ['NotifyIcon']

import sys
import os
import gtk
import time
try:
    import appindicator
    APPINDICATOR = True
except:
    APPINDICATOR = False

from lib import common
from lib.utils import ContextMenu

class NotifyIcon:
    """ This class creates the tray icon notification - GTK 2.10 or above """

    def __init__(self,parent):
        """ Constructor """

        self.parent = parent

        #show the icon
        self.start()

    def start(self):
        """ Function used to show an icon in notification area."""

        if APPINDICATOR:
            self.indicator = appindicator.Indicator("billreminder", "ApplicationStatus", appindicator.CATEGORY_APPLICATION_STATUS)
            self.indicator.set_status(appindicator.STATUS_ACTIVE)
            self.indicator.set_attention_icon(common.PANEL_ATTENTION_ICON)
            self.indicator.set_icon(common.PANEL_ICON)
            self.menu = self.show_menu(None, None, None)
            self.indicator.set_menu(self.menu)
            self.menu.show()
        else:
            self.tray = gtk.StatusIcon()
            self.tray.set_from_file(common.TRAY_ICON)
            self.tray.set_tooltip(_("BillReminder"))
            self.tray.connect("popup-menu", self.show_menu, None)
            self.tray.connect("activate", self.show_hide, None)

    def show_hide(self, status_icon, arg=None):
        """ Show and Hide the main window. """
        self.parent.show_hide_window()
        if isinstance(status_icon, gtk.MenuItem):
            menu_item = status_icon
            if self.parent.get_window_visibility():
                menu_item.set_label(_('Hide Window'))
            else:
                menu_item.set_label(_('Show Window'))

    def show_menu(self, status_icon, button, activate_time, arg=None):
        """ Show a popup menu when an user right clicks notification
            area icon. """
        c = ContextMenu(self)
        if self.parent.get_window_visibility():
            c.addMenuItem(_('Hide Window'), self.show_hide)
        else:
            c.addMenuItem(_('Show Window'), self.show_hide)

        c.addMenuItem('-', None)
        c.addMenuItem(_('Preferences'),
                      self.parent.on_btnPrefs_activate,
                      gtk.STOCK_PREFERENCES)
        c.addMenuItem(_('About'),
                      self.parent.on_btnAbout_activate,
                      gtk.STOCK_ABOUT)
        c.addMenuItem('-', None)
        c.addMenuItem(_('Quit'),
                      self.parent.on_btnQuit_activate,
                      gtk.STOCK_QUIT)

        if APPINDICATOR:
            return c

        print type(activate_time)
        c.popup(None,
                None,
                gtk.status_icon_position_menu,
                button,
                activate_time, self.tray)
        del c

    def destroy(self):
        """ Hide the systray icon. """
        self.tray.set_visible(False)

    def exists(self):
        """ Do nothing here, only returns that the class was instantiated."""
        return True

    def get_hints(self):
        hints = {}
        x = self.tray.get_geometry()[1].x
        y = self.tray.get_geometry()[1].y
        w = self.tray.get_geometry()[1].width
        h = self.tray.get_geometry()[1].height
        x += w/2
        if y < 100:
            # top-panel
            y += h/2
        else:
            # bottom-panel
            y -= h/2
        hints['x'] = x
        hints['y'] = y
        hints['desktop-entry'] = 'billreminder'
        self.hints = hints
        return hints
