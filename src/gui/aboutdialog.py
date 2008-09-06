# -*- coding: utf-8 -*-

__all__ = ['AboutDialog']

import pygtk
pygtk.require('2.0')

import gtk
import lib.common as common

# Internationalization
from lib import i18n

try:
  import gnome
  def open_url(url): gnome.url_show(url)
except:
  import os
  def open_url(url): os.system("xdg-open %s" % url)

TRANSLATORS = _("translator-credits")

gtk.about_dialog_set_url_hook(lambda dialog, url, data: open_url(url), None)

class AboutDialog(gtk.AboutDialog):
    """
    About dialog class.
    """
    def __init__(self, parent=None):
        gtk.AboutDialog.__init__(self)

        # Set up the UI
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
