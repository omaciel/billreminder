#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['AboutDialog']

import pygtk
pygtk.require('2.0')
import gtk
import webbrowser

import lib.common as common
from lib import i18n

TRANSLATORS = _("translator-credits")


class AboutDialog(gtk.AboutDialog):
    """
    About dialog class.
    """
    def __init__(self, parent=None):
        gtk.AboutDialog.__init__(self)

        # Set up the UI
        gtk.about_dialog_set_url_hook(self.open_url)
        self._initialize_dialog_widgets()
        self.set_icon_from_file(common.APP_ICON)

    def _initialize_dialog_widgets(self):
        self.set_name(common.APPNAME)
        self.set_version(common.APPVERSION)
        self.set_copyright(common.COPYRIGHTS)
        self.set_logo(gtk.gdk.pixbuf_new_from_file(common.APP_HEADER))
        self.set_translator_credits(TRANSLATORS)
        self.set_license(common.LICENSE)
        self.set_website(common.WEBSITE)
        self.set_website_label(_("BillReminder Website"))
        self.set_authors(common.AUTHORS)
        self.set_artists(common.ARTISTS)

        # Show all widgets
        self.show_all()
    
    # Make sure the URLs are clickable
    def open_url(self, dlg, url):
        webbrowser.open_new(url)