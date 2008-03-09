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

def about_dialog(parent=None):
    about = AboutDialog()
    ret = about.run()
    about.destroy()

    return ret

def preferences_dialog(parent=None):
    pref = PrefDialog(parent=parent)
    ret = pref.run()
    pref.destroy()

    return ret

def categories_dialog(parent=None):
    categories = CategoriesDialog(parent=parent)
    ret = categories.run()
    pref.destroy()

    return ret

def add_dialog(parent=None, selectedDate=None):
    record = None
    # Dialog Title
    dialog = AddDialog(title=_("Add a New Record"), parent=parent, record=record, selectedDate=selectedDate)
    response = dialog.run()
    # Checks if the user did not cancel the action
    if response == gtk.RESPONSE_ACCEPT:
        record = dialog.get_record()
    dialog.destroy()

    return record

def edit_dialog(record, parent=None):
    # Dialog Title
    dialog = AddDialog(title=_("Edit a Record"), parent=parent, record=record)
    response = dialog.run()
    # Checks if the user did not cancel the action
    if response == gtk.RESPONSE_ACCEPT:
        record = dialog.get_record()
    else:
        record = [record]
    dialog.destroy()

    return record
