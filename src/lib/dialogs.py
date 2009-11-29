# -*- coding: utf-8 -*-

__all__ = ['about_dialog', 'add_dialog', 'edit_dialog', 'preferences_dialog']

import sys
import os

try:
    import gtk
except ImportError:
    print "Please install gtk"
    raise SystemExit

try:
    import pygtk
    pygtk.require("2.0")
except ImportError:
    print "Please install pygtk"
    raise SystemExit

from gui.aboutdialog import AboutDialog
from gui.adddialog import AddDialog
from gui.prefdialog import PrefDialog
from gui.categoriesdialog import CategoriesDialog
from lib import i18n


class OneWindow(object):
    def __init__(self, dialog_class):
        self.dialog = None
        self.dialog_class = dialog_class
    
    def on_dialog_destroy(self):
        self.dialog = None

    def show(self, parent = None):
        if self.dialog:
            self.dialog.present()
        else:
            if parent:
                self.dialog = self.dialog_class(parent)
            else:
                self.dialog = self.dialog_class()
            self.dialog.connect("destroy", lambda *args: self.on_dialog_destroy())

about = OneWindow(AboutDialog)
prefs = OneWindow(PrefDialog)

def about_dialog(parent=None):
    about.show(parent)

def preferences_dialog(parent=None):
    prefs.show(parent)

def categories_dialog(parent=None):
    categories = CategoriesDialog(parent=parent)
    ret = categories.run()
    pref.destroy()

    return ret

def add_dialog(parent=None, selectedDate=None):
    record = None
    # Dialog Title
    dialog = AddDialog(title=_("Add a new bill"), parent=parent, record=record, selectedDate=selectedDate)
    response = dialog.window.run()
    # Checks if the user did not cancel the action
    if response == gtk.RESPONSE_ACCEPT:
        record = dialog.get_record()
    dialog.window.destroy()

    return record

def edit_dialog(record, parent=None):
    # Dialog Title
    dialog = AddDialog(title=_("Edit a bill"), parent=parent, record=record)
    response = dialog.window.run()
    # Checks if the user did not cancel the action
    if response == gtk.RESPONSE_ACCEPT:
        record = dialog.get_record()
    else:
        record = None
    dialog.window.destroy()

    return record
