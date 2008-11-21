# -*- coding: utf-8 -*-

__all__ = ['AddDialog']

import pygtk
pygtk.require('2.0')
import gtk
import gconf
import datetime
import locale
import gobject

from lib import utils
from lib import common
from lib import scheduler
from lib.bill import Bill
from lib.actions import Actions
from lib.utils import create_pixbuf
from lib import i18n
from gui.widgets.datebutton import DateButton
from gui.widgets.datepicker import DatePicker
from gui.categoriesdialog import CategoriesDialog
from lib.common import GCONF_PATH, GCONF_GUI_PATH, GCONF_ALARM_PATH

class AddDialog(gtk.Dialog):
    """
    Class used to generate dialog to allow user to enter/edit records.
    """
    def __init__(self, title=None, parent=None, record=None, selectedDate=None):
        gtk.Dialog.__init__(self, title=title, parent=parent,
                            #flags=gtk.DIALOG_MODAL|gtk.DIALOG_NO_SEPARATOR,
                            flags=gtk.DIALOG_NO_SEPARATOR,
                            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                                     gtk.STOCK_SAVE, gtk.RESPONSE_ACCEPT))

        self.set_icon_from_file(common.APP_ICON)
        self.set_border_width(6)
        self.set_resizable(False)

        if parent:
            self.set_transient_for(parent)
            self.set_position(gtk.WIN_POS_CENTER_ON_PARENT)

        # If we have a selected date, then set calendar to use it
        if not selectedDate:
            selectedDate = datetime.datetime.today()
        self.selectedDate = selectedDate

        self.gconf_client = gconf.client_get_default()

        # Private copy of any record passed
        self.currentrecord = record

        self.alarm = [None, None]

        # TODO: This needs to be run BEFORE connecting the widgets
        self._set_currency()

        # Set up the UI
        self._initialize_dialog_widgets()
        self._connect_fields()
        self._populate_widgets()
        self.category_index_before = 0

        self.connect("response", self._on_response)

    def _set_currency(self):
        self.decimal_sep = locale.localeconv()['mon_decimal_point']
        self.thousands_sep = locale.localeconv()['mon_thousands_sep']

        self.allowed_digts = [self.decimal_sep , self.thousands_sep]
        self.allowed_digts += [str(i) for i in range(10)]

    def _initialize_dialog_widgets(self):
        self.vbox.set_spacing(12)
        self.fieldbox = gtk.VBox(homogeneous=False, spacing=6)

        ## repeat times
        self.repeatlabel = gtk.Label()
        self.repeatlabel.set_markup_with_mnemonic(_("<b>_Repeat:</b>"))
        self.repeatlabel.set_alignment(0.00, 0.50)
        adj = gtk.Adjustment(00.0, 1.0, 23.0, 1.0)

        # Datepickers
        self.dueDateLabel = gtk.Label()
        self.dueDateLabel.set_markup_with_mnemonic(_("<b>Due Date:</b>"))
        self.dueDate = DatePicker()
        self.endDateLabel = gtk.Label()
        #TRANSLATORS: This is the end date for repeating bills.
        self.endDateLabel.set_markup_with_mnemonic(_("<b>End Date:</b>"))
        self.endDate = DatePicker()

        ## Repeating bills
        self.frequency = gtk.combo_box_new_text()
        self.repeatlabel.set_mnemonic_widget(self.frequency)
        #self.frequency.set_row_separator_func(self._determine_separator)

        # Fields
        ## Table of 6 x 2
        self.table = gtk.Table(rows=6, columns=2, homogeneous=False)
        ### Spacing to make things look better
        self.table.set_col_spacings(12)
        self.table.set_row_spacings(6)

        ## Labels
        self.payeelabel = gtk.Label()
        self.payeelabel.set_markup_with_mnemonic(_("<b>_Payee:</b>"))
        self.payeelabel.set_alignment(0.00, 0.50)
        self.amountlabel = gtk.Label()
        self.amountlabel.set_markup_with_mnemonic(_("<b>_Amount:</b>"))
        self.amountlabel.set_alignment(0.00, 0.50)
        self.categorylabel = gtk.Label()
        self.categorylabel.set_markup_with_mnemonic(_("<b>_Category:</b>"))
        self.categorylabel.set_alignment(0.00, 0.50)
        self.noteslabel = gtk.Label()
        self.noteslabel.set_markup_with_mnemonic(_("<b>_Notes:</b>"))
        self.noteslabel.set_alignment(0.00, 0.00)
        self.alarmlabel = gtk.Label()
        self.alarmlabel.set_markup_with_mnemonic(_("<b>A_larm:</b>"))
        self.alarmlabel.set_alignment(0.00, 0.50)
        ## Fields
        ### Payee
        self.payee = gtk.ComboBoxEntry()
        self.payeelabel.set_mnemonic_widget(self.payee)
        self.payeecompletion = gtk.EntryCompletion()
        self.payee.child.set_completion(self.payeecompletion)
        ### Amount
        self.amount = gtk.Entry()
        self.amountlabel.set_mnemonic_widget(self.amount)
        self.amount.set_alignment(1.00)
        ### Category
        self.categorydock = gtk.HBox(homogeneous=False, spacing=4)
        self.category = gtk.ComboBox()
        self.categorylabel.set_mnemonic_widget(self.category)
        px = gtk.CellRendererPixbuf()
        txt = gtk.CellRendererText()
        self.category.pack_start(px, False)
        self.category.pack_start(txt, False)
        self.category.add_attribute(px, "pixbuf", 0)
        self.category.add_attribute(txt, "text", 1)
        self.category.set_row_separator_func(self._determine_separator)

        self.categorybutton = gtk.Button()
        self.categorybutton.set_tooltip_text(_("Manage Categories"))
        self.categorybuttonimage = gtk.Image()
        self.categorybuttonimage.set_from_stock(gtk.STOCK_EDIT,
                                                gtk.ICON_SIZE_BUTTON)
        self.categorybutton.set_image(self.categorybuttonimage)
        self.categorydock.pack_start(self.category, expand=True,
                                     fill=True, padding=0)
        self.categorydock.pack_start(self.categorybutton, expand=False,
                                     fill=True, padding=0)

        ### Notes
        self.notesdock = gtk.ScrolledWindow()
        self.notesdock.set_shadow_type(gtk.SHADOW_OUT)
        self.notesdock.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.notes = gtk.TextView()
        self.noteslabel.set_mnemonic_widget(self.notes)
        self.notes.set_wrap_mode(gtk.WRAP_WORD)
        self.notesdock.add(self.notes)
        ### Buffer object for Notes field
        self.txtbuffer = self.notes.get_buffer()
        ### Alarm
        self.alarmbutton = DateButton(self)
        self.alarmlabel.set_mnemonic_widget(self.alarmbutton)
        self.alarmbutton.set_tooltip_text(_("Select Date and Time"))

        ## Pack it all into the table
        ### Label widgets
        self.table.attach(self.payeelabel,      0, 1, 0, 1, gtk.FILL, gtk.FILL)
        self.table.attach(self.amountlabel,     0, 1, 1, 2, gtk.FILL, gtk.FILL)
        self.table.attach(self.dueDateLabel,    0, 1, 2, 3, gtk.FILL, gtk.FILL)
        self.table.attach(self.categorylabel,   0, 1, 3, 4, gtk.FILL, gtk.FILL)
        self.table.attach(self.repeatlabel,     0, 1, 4, 5, gtk.FILL, gtk.FILL)
        self.table.attach(self.endDateLabel,    0, 1, 5, 6, gtk.FILL, gtk.FILL)
        ### "Value" widgets
        self.table.attach(self.payee,           1, 2, 0, 1, gtk.FILL, gtk.FILL)
        self.table.attach(self.amount,          1, 2, 1, 2, gtk.FILL, gtk.FILL)
        self.table.attach(self.dueDate,         1, 2, 2, 3, gtk.FILL, gtk.FILL)
        self.table.attach(self.categorydock,    1, 2, 3, 4, gtk.FILL, gtk.FILL)
        self.table.attach(self.frequency,       1, 2, 4, 5, gtk.FILL, gtk.FILL)
        self.table.attach(self.endDate,         1, 2, 5, 6, gtk.FILL, gtk.FILL)

        ## Pack table
        self.fieldbox.pack_start(self.table, expand=True, fill=True, padding=0)

        ## Container with optional fields
        vbox = gtk.VBox(homogeneous=False, spacing=2)
        hbox1 = gtk.HBox(homogeneous=False, spacing=2)
        hbox2 = gtk.HBox(homogeneous=False, spacing=2)

        ### "Value" widgets
        hbox1.pack_start(self.noteslabel, expand=False, fill=True, padding=0)
        hbox1.pack_start(self.notesdock, expand=True, fill=True, padding=0)
        hbox2.pack_start(self.alarmlabel, expand=False, fill=True, padding=0)
        hbox2.pack_start(self.alarmbutton, expand=True, fill=True, padding=0)

        vbox.pack_start(hbox1, expand=True, fill=True, padding=0)
        vbox.pack_start(hbox2, expand=True, fill=True, padding=0)
        ## Expander
        self.optExpander = gtk.Expander(_("<b>Optional Fields:</b>"))
        self.optExpander.set_use_markup(True)
        self.optExpander.set_expanded(False)
        self.optExpander.add(vbox)


        # Everything
        self.vbox.pack_start(self.fieldbox, expand=False, fill=True)
        self.vbox.pack_start(self.optExpander, expand=True, fill=True, padding=0)

        # Connect events

        # Show all widgets
        self.show_all()

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
            self.repeatlabel.set_sensitive(False)
            self.endDateLabel.set_sensitive(False)
            self.endDate.set_sensitive(False)

        else:
            self.dueDate.set_date(self.selectedDate)
            self.endDate.set_date(self.selectedDate)
            # Use alarm values from preferences
            showalarm = self.gconf_client.get_bool(GCONF_ALARM_PATH + 'show_alarm')
            atime = self.gconf_client.get_string(GCONF_ALARM_PATH + 'show_alarm_at_time')
            adays = self.gconf_client.get_int(GCONF_ALARM_PATH + 'show_alarm_before_days')
            if not atime:
                showalarm  ='true'
                atime = '13:00'
                adays = 3

            if showalarm == 'true':
                alarmDate = scheduler.get_alarm_timestamp(adays, atime, self.selectedDate)
                self.alarmbutton.set_date(alarmDate)


    def _connect_fields(self):
        self.category.connect("changed", self._on_categorycombo_changed)
        self.categorybutton.connect("clicked",
            self._on_categoriesbutton_clicked)
        self.amount.connect("insert-text", self._on_amount_insert)
        self.frequency.connect('changed', self._on_frequency_changed)
        self.dueDate.connect('date_changed', self._on_datepicker_date_changed)


    def _determine_separator(self, model, iter, data=None):
        return model.get_value(iter, 1) == "---"

    def _populate_widgets_with_record(self):
        # Format the amount field
        if self.currentrecord.AmountDue:
            self.amount.set_text(utils.float_to_currency(self.currentrecord.AmountDue))
        else:
            self.amount.set_text("")
        # Format the dueDate field
        dt = scheduler.datetime_from_timestamp(self.currentrecord.DueDate)
        self.dueDate.set_date(dt)
        utils.select_combo_text(self.payee, self.currentrecord.Payee)
        actions = Actions()
        records = actions.get_categories({'id': self.currentrecord.Category})
        if records:
            categoryname = records[0]['categoryname']
            utils.select_combo_text(self.category, categoryname, 1)
        else:
            self.category.set_active(0)

        self.txtbuffer.set_text(self.currentrecord.Notes)
        #self.chkPaid.set_active(self.currentrecord.Paid)

        if self.currentrecord.Alarm > 0:
            self.alarmbutton.set_date(self.currentrecord.Alarm)

    def _populate_payee(self):
        """ Populates combobox with existing payees """
        # Connects to the database
        actions = Actions()

        # List of payees from database
        payees = []
        records = actions.get_bills("paid IN (0,1) ORDER BY payee ASC")
        for rec in records:
            if rec['payee'] not in payees:
                payees.append(rec['payee'])

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
        store.append([scheduler.SC_ONCE, 0])
        store.append([scheduler.SC_MONTHLY, 1])
        store.append([scheduler.SC_WEEKLY, 2])
        # Set SC_ONCE as default
        self.frequency.set_active(0)

    def _populate_category(self, categoryname=None):
        """ Populates combobox with existing categories """
        # Connects to the database
        actions = Actions()

        # List of categories from database
        categories = []
        records = actions.get_categories("id > 0 ORDER BY categoryname ASC") or []

        ret = 0
        empty_color = create_pixbuf()
        for rec in records:
            #if [rec['categoryname'], rec['id']] not in categories:
            #TODO: Better put color creation in a function
            color = rec['color']

            categories.append([create_pixbuf(color=color), rec['categoryname'], int(rec['id'])])
            if categoryname and categoryname == rec['categoryname']:
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

        records = actions.get_categories({'categoryname': name})
        if records:
            cat_id = records[0]['id']

        return cat_id and int(cat_id) or None

    def get_record(self):

        frequency = self.frequency.get_active_text()
        # Extracts the date off the calendar widget
        # Create datetime object
        selectedDate = scheduler.timestamp_from_datetime(self.dueDate.get_date())
        # End date
        if frequency != scheduler.SC_ONCE:
            endDate = scheduler.timestamp_from_datetime(self.endDate.currentDate)
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
        alarm = self.alarmbutton.get_date()  or -1

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
            days = scheduler.get_schedule_timestamp(
                frequency, self.dueDate.get_date(), self.endDate.get_date())

            for day in days:
                if alarm != -1:
                    alarm = self.__get_alarm_date(day)
                rec = Bill(payee, category, day, amount, sbuffer, 0, -1, alarm)
                records.append (rec)

            print records
            return records
        else:
            # Edit existing bill
            self.currentrecord.Category = category
            self.currentrecord.Payee = payee
            self.currentrecord.DueDate = int(selectedDate)
            self.currentrecord.AmountDue = amount
            self.currentrecord.Notes = sbuffer
            self.currentrecord.Alarm = alarm

            #return the bill
            return [self.currentrecord]

    def _on_frequency_changed(self, widget):
        frequency = widget.get_active_text()
        if frequency == scheduler.SC_ONCE:
            self.endDateLabel.set_sensitive(False)
            self.endDate.set_sensitive(False)
        else:
            self.endDateLabel.set_sensitive(True)
            self.endDate.set_sensitive(True)

    def _on_categoriesbutton_clicked(self, button, new=False):
        # if new == True, a simpler categories dialog pops up
        categories = CategoriesDialog(parent=self, new=new)
        ret = categories.run()

        if ret == gtk.RESPONSE_OK:
            #TODO: We should handle the saving in the dialog itself.
            # the category hasn't been saved yet... so save it.
            if new:
                categories._on_savebutton_clicked(None)
            category = categories.currentrecord

            self._populate_category(category['categoryname'])

        categories.destroy()
        return ret

    def _on_categorycombo_changed(self, combobox):
        index = self.category.get_active()
        model = self.category.get_model()
        if index == len(model) - 1:
            self.category.set_active(self.category_index_before)
            self._on_categoriesbutton_clicked(combobox, True)
        self.category_index_before = index

    def _on_amount_insert(self, entry, string, len, position):
        for char in string:
            if char not in self.allowed_digts:
                print "Invalid Character: %s" % char
                entry.emit_stop_by_name("insert-text")
                gtk.gdk.beep()
                return

    def _on_response(self, dialog, response_id):
        message = utils.Message()
        if response_id == gtk.RESPONSE_ACCEPT:
            if not self._get_payee().strip() and \
                not self.amount.get_text().strip():
                message.ShowError(_("\"%s\" and \"%s\" are required fields.") \
                    % (_("Payee"), _("Amount")), self)
                self.emit_stop_by_name("response")
                self.payee.grab_focus()
            elif not self._get_payee().strip():
                message.ShowError(_("\"%s\" is required field.") % _("Payee"), self)
                self.emit_stop_by_name("response")
                self.payee.grab_focus()

    def _on_datepicker_date_changed(self, widget, args):
        # Only reprogram alarm if it is not None
        print "Date changed"
        # Update endDate to be equal to dueDate
        self.endDate.set_date(self.dueDate.get_date())

        if self.alarmbutton.get_date():
            # Extracts the date off the datepicker widget
            alarmDate = self.__get_alarm_date(self.dueDate.get_date())
            self.alarmbutton.set_date(alarmDate)

    def __get_alarm_date(self, date):
        # Use alarm values from preferences
        atime = self.gconf_client.get_string(GCONF_ALARM_PATH + 'show_alarm_at_time')
        adays = self.gconf_client.get_int(GCONF_ALARM_PATH + 'show_alarm_before_days')

        # If not running installed, there is no gconf schema.
        if not atime:
            atime = '13:00'
            adays = 3

        return scheduler.get_alarm_timestamp(adays, atime, date)

