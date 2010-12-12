# -*- coding: utf-8 -*-

__all__ = ['AddDialog']

import os
import pygtk
pygtk.require('2.0')
import gtk
import datetime
import locale
import gobject

from lib import utils
from lib import common
from lib import scheduler
from db.entities import Bill, Category
from lib.actions import Actions
from lib.utils import create_pixbuf
from lib import i18n
from gui.widgets.datebutton import DateButton
from gui.widgets.datepicker import DatePicker
from gui.categoriesdialog import CategoriesDialog
#from lib.config import Configuration
from lib.Settings import Settings as Configuration

class AddDialog(object):
    """
    Class used to generate dialog to allow user to enter/edit records.
    """
    def __init__(self, title=None, parent=None, record=None, selectedDate=None):
        self.ui = gtk.Builder()
        self.ui.add_from_file(os.path.join(common.DEFAULT_CFG_PATH, "add_bill.ui"))

        self.window = self.ui.get_object("add_bill_dialog")

        self.window.set_icon_from_file(common.APP_ICON)

        if parent:
            self.window.set_transient_for(parent)

        # If we have a selected date, then set calendar to use it
        if not selectedDate:
            selectedDate = datetime.date.today()
        self.selectedDate = selectedDate

        self.gconf_client = Configuration()

        # Private copy of any record passed
        self.currentrecord = record

        self.alarm = [None, None]

        # TODO: This needs to be run BEFORE connecting the widgets
        self._set_currency()

        # Set up the UI
        self._initialize_dialog_widgets()


        self._populate_widgets()
        self.category_index_before = 0

        self.ui.connect_signals(self)

    def _set_currency(self):
        self.decimal_sep = locale.localeconv()['mon_decimal_point']
        self.thousands_sep = locale.localeconv()['mon_thousands_sep']

        self.allowed_digts = [self.decimal_sep , self.thousands_sep]
        self.allowed_digts += [str(i) for i in range(10)]

    def _initialize_dialog_widgets(self):
        self.frequency = self.ui.get_object("frequency")

        self.dueDate = DatePicker()
        self.ui.get_object("due_date_box").add(self.dueDate)
        self.dueDate.connect('date_changed', self._on_datepicker_date_changed)

        self.endDate = DatePicker()
        self.ui.get_object("end_date_box").add(self.endDate)
        self.endDate.connect('date_changed', self._on_datepicker_date_changed)

        self.payee = self.ui.get_object("payee")
        self.payeecompletion = gtk.EntryCompletion()
        self.payee.child.set_completion(self.payeecompletion)

        self.amount = self.ui.get_object("amount")

        self.category = self.ui.get_object("category")
        px = gtk.CellRendererPixbuf()
        txt = gtk.CellRendererText()
        self.category.pack_start(px, False)
        self.category.pack_start(txt, False)
        self.category.add_attribute(px, "pixbuf", 0)
        self.category.add_attribute(txt, "text", 1)
        self.category.set_row_separator_func(self._determine_separator)

        self.categorybutton = self.ui.get_object("edit_categories")

        self.notes = self.ui.get_object("notes")
        self.txtbuffer = self.notes.get_buffer()

        self.alarmbutton = DateButton(self.window)
        self.alarmbutton.set_tooltip_text(_("Select Date and Time"))
        self.ui.get_object("alarm_button_box").add(self.alarmbutton)
        self.ui.get_object("alarm_label").set_mnemonic_widget(self.alarmbutton)

        self.window.show_all()

    def _populate_widgets(self):
        """ Populate dialog widgets so they can be used. """
        self._populate_frequency()
        self._populate_payee() # Populate combobox with payee from db
        self._populate_category() # Populate combobox with category from db

        # If a record was passed, we're in edit mode
        if self.currentrecord:
            self._populate_widgets_with_record()
            #in edit mode we must disable repetition
            self.frequency.set_sensitive(False)
            self.endDate.set_sensitive(False)

        else:
            self.dueDate.set_date(self.selectedDate)
            self.endDate.set_date(self.selectedDate)
            # Use alarm values from preferences
            showalarm = self.gconf_client.get('show_alarm')
            atime = self.gconf_client.get('show_alarm_at_time')
            adays = self.gconf_client.get('show_alarm_before_days')

            if showalarm:
                alarmDate = scheduler.get_alarm_timestamp(adays, atime, self.selectedDate)
                self.alarmbutton.set_date(alarmDate)


    def _determine_separator(self, model, iter, data=None):
        return model.get_value(iter, 1) == "---"

    def _populate_widgets_with_record(self):
        # Format the amount field
        if self.currentrecord.amount:
            self.amount.set_text(utils.float_to_currency(self.currentrecord.amount))
        else:
            self.amount.set_text("")
        # Format the dueDate field
        dt = self.currentrecord.dueDate
        self.dueDate.set_date(dt)
        utils.select_combo_text(self.payee, self.currentrecord.payee)

        if self.currentrecord.category:
            actions = Actions()
            cat_name = self.currentrecord.category.name
            records = actions.get_categories(name=cat_name)
            if records:
                categoryname = records[0].name
                utils.select_combo_text(self.category, categoryname, 1)
        else:
            self.category.set_active(0)

        if self.currentrecord.notes:
            self.txtbuffer.set_text(self.currentrecord.notes)
        #self.chkPaid.set_active(self.currentrecord.Paid)

        if self.currentrecord.alarmDate:
            self.alarmbutton.set_date(self.currentrecord.alarmDate)

    def _populate_payee(self):
        """ Populates combobox with existing payees """
        # Connects to the database
        actions = Actions()

        # List of payees from database
        payees = []
        records = actions.get_bills()
        for rec in records:
            if rec.payee not in payees:
                payees.append(rec.payee)

        store = gtk.ListStore(gobject.TYPE_STRING)
        for payee in payees:
            store.append([payee])

        self.payee.set_model(store)
        self.payeecompletion.set_model(store)
        self.payee.set_text_column(0)
        self.payeecompletion.set_text_column(0)
        self.payeeEntry = self.payee.child
        self.selectedText = ''

    def _get_payee(self):
        """ Extracts information typed into comboboxentry """
        if self.payee.get_active_iter() is not None:
            model = self.payee.get_model()
            iteration = self.payee.get_active_iter()
            if iteration:
                return model.get_value(iteration, 0)
        else:
            return self.payeeEntry.get_text()

    def _populate_frequency(self):
        """ Populates combobox with allowable frequency. """
        store = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_INT)
        self.frequency.set_model(store)

        cell = gtk.CellRendererText()
        self.frequency.pack_start(cell, True)
        self.frequency.add_attribute(cell, 'text', 0)

        for i, frequency in enumerate([scheduler.SC_ONCE,
                                       scheduler.SC_MONTHLY,
                                       scheduler.SC_WEEKLY]):
            store.append([frequency, i])

        # Set SC_ONCE as default
        self.frequency.set_active(0)
        self.on_frequency_changed(self.frequency)

    def _populate_category(self, categoryname=None):
        """ Populates combobox with existing categories """
        # Connects to the database
        actions = Actions()

        # List of categories from database
        categories = []
        records = actions.get_categories()

        ret = 0
        empty_color = create_pixbuf()
        for rec in records:
            #if [rec['categoryname'], rec['id']] not in categories:
            #TODO: Better put color creation in a function
            color = rec.color and rec.color or '#000'

            categories.append([create_pixbuf(color=color), rec.name, int(rec.id)])
            if categoryname and categoryname == rec.name:
                ret = len(categories) + 1

        store = gtk.ListStore(gtk.gdk.Pixbuf, str, int)

        self.category.set_model(store)
        store.append([empty_color, _("None"), 0])
        store.append([None, "---", -1])

        for category in categories:
            store.append(category)
        store.append([None, "---", -1])
        store.append([empty_color, _("New Category"), -2])
        self.category.set_active(ret)

        return ret

    def _get_category(self):
        """ Extracts information typed into comboboxentry """

        actions = Actions()

        if self.category.get_active_iter() is not None:
            model = self.category.get_model()
            iteration = self.category.get_active_iter()
            if iteration:
                name = model.get_value(iteration, 1)
        else:
            name = None

        if not name or name == _("None"):
            return None

        records = actions.get_categories(name=name)
        if records:
            return records[0]
        else:
            return None

    def get_record(self):

        frequency = self.frequency.get_active_text()
        # Extracts the date off the calendar widget
        # Create datetime object
        selectedDate = self.dueDate.get_date()
        # End date
        if frequency != scheduler.SC_ONCE:
            endDate = self.endDate.get_date()
            # Notify user that the endDate is set in the past
            if endDate < selectedDate:
                endDate = selectedDate
                message = utils.Message()
                text = _("The end date is set to a date prior to the start date. Setting it to match the start date.")
                title = _("Date set in the past")
                message.ShowInfo(text=text, parentWindow=self, title=title)
        else:
            endDate = None

        #buffer = self.txtNotes.get_buffer()
        startiter, enditer = self.txtbuffer.get_bounds()
        sbuffer = self.txtbuffer.get_text(startiter, enditer)

        # Gets the payee
        payee = self._get_payee()

        # Gets the category
        category = self._get_category()

        # Gets the alarm date
        alarm = self.alarmbutton.get_date()  or None

        # Validate form
        if not payee.strip():
            return None

        if self.amount.get_text().strip():
            amount = utils.currency_to_float(self.amount.get_text())
        else:
            amount = None

        if self.currentrecord is None:
            # Verify how many bills will be inserted
            # this will only work for new bills
            records = []

            # Figures out how many times we're repeating this bill
            days = scheduler.get_schedule_date(
                frequency, selectedDate, endDate)

            for day in days:
                if alarm:
                    alarm = self.__get_alarm_date(day)
                rec = Bill(payee=payee, amount=amount, dueDate=day, alarmDate=alarm, notes=sbuffer, repeats=False)

                # Bill repeats...
                if len(days) > 1:
                    rec.repeats = True
                # ... and has a category.
                if category:
                    rec.category = category
                records.append(rec)
            return records
        else:
            # Edit existing bill
            self.currentrecord.payee = payee
            self.currentrecord.dueDate = selectedDate
            self.currentrecord.amount = amount
            self.currentrecord.notes = sbuffer
            self.currentrecord.alarmDate = alarm
            if category:
                self.currentrecord.category = category

            #return the bill
            return [self.currentrecord]

    def on_frequency_changed(self, widget):
        frequency = widget.get_active_text()
        if frequency == scheduler.SC_ONCE:
            self.endDate.set_sensitive(False)
        else:
            self.endDate.set_sensitive(True)

    def on_edit_categories_clicked(self, button, new = False):
        category = None

        # if new == True, a simpler categories dialog pops up
        self.window.category = self.category
        categories = CategoriesDialog(parent = self.window, new = new)
        ret = categories.run()

        if ret == gtk.RESPONSE_OK:
            #TODO: We should handle the saving in the dialog itself.
            # the category hasn't been saved yet... so save it.
            if new:
                categories._on_savebutton_clicked(None)
            category = categories.currentrecord

        categories.destroy()

        # Always re-populate the categories dropdown widget, regardless if
        # newer category was added. If something was returned, select it.
        if category:
            self._populate_category(category.name)
        else:
            self._populate_category()

        return ret

    def on_category_changed(self, combobox):
        index = self.category.get_active()
        model = self.category.get_model()
        if index == len(model) - 1:
            self.category.set_active(self.category_index_before)
            self.on_edit_categories_clicked(combobox, True)
        self.category_index_before = index

    def on_amount_insert_text(self, entry, string, len, position):
        for char in string:
            if char not in self.allowed_digts:
                print "Invalid Character: %s" % char
                entry.emit_stop_by_name("insert-text")
                gtk.gdk.beep()
                return

    def on_save_clicked(self, widget):
        message = utils.Message()
        if not self._get_payee().strip() and \
            not self.amount.get_text().strip():
            message.ShowError(_("\"%s\" and \"%s\" are required fields.") \
                % (_("Payee"), _("Amount")), self.window)
            self.payee.grab_focus()
        elif not self._get_payee().strip():
            message.ShowError(_("\"%s\" is required field.") % _("Payee"), self.window)
            self.payee.grab_focus()
        elif not self.amount.get_text().strip():
            message.ShowError(_("\"%s\" is required field.") % _("Amount"), self.window)
            self.amount.grab_focus()
        else:
            self.window.response(gtk.RESPONSE_ACCEPT)

    def _on_datepicker_date_changed(self, widget, args):

        startDate = self.dueDate.get_date()
        endDate = self.endDate.get_date()

        if widget == self.dueDate:
            if startDate > endDate:
                # Update endDate to be equal to dueDate
                self.endDate.set_date(self.dueDate.get_date())
                message = utils.Message()
                text = _("The end date is set to a date prior to the start date. Setting it to match the start date.")
                title = _("Date set in the past")
                message.ShowInfo(text=text, parentWindow=self.window, title=title)
        else:
            if startDate > endDate:
                # Update endDate to be equal to dueDate
                self.endDate.set_date(self.dueDate.get_date())
                message = utils.Message()
                text = _("The end date is set to a date prior to the start date. Setting it to match the start date.")
                title = _("Date set in the past")
                message.ShowInfo(text=text, parentWindow=self.window, title=title)

        if self.alarmbutton.get_date():
            # Extracts the date off the datepicker widget
            alarmDate = self.__get_alarm_date(self.dueDate.get_date())
            self.alarmbutton.set_date(alarmDate)

    def __get_alarm_date(self, date):
        # Use alarm values from preferences
        atime = self.gconf_client.get('show_alarm_at_time')
        adays = self.gconf_client.get('show_alarm_before_days')

        return scheduler.get_alarm_timestamp(adays, atime, date)
