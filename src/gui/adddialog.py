# -*- coding: utf-8 -*-

__all__ = ['AddDialog']

import pygtk
pygtk.require('2.0')
import gtk
import datetime
import locale
import gobject

from lib import utils
from lib import common
from lib import scheduler
from lib.bill import Bill
from lib.actions import Actions
from lib.config import Config
from lib.utils import create_pixbuf
from lib import i18n
from gui.widgets.datebutton import DateButton
from gui.categoriesdialog import CategoriesDialog

class AddDialog(gtk.Dialog):
    """
    Class used to generate dialog to allow user to enter/edit records.
    """
    def __init__(self, title=None, parent=None, record=None, selectedDate=None):
        gtk.Dialog.__init__(self, title=title, parent=parent,
                            flags=gtk.DIALOG_MODAL,
                            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                                     gtk.STOCK_SAVE, gtk.RESPONSE_ACCEPT))
        self.set_icon_from_file(common.APP_ICON)

        if parent:
            self.set_transient_for(parent)
            self.set_position(gtk.WIN_POS_CENTER_ON_PARENT)

        # If we have a selected date, then set calendar to use it
        if not selectedDate:
            selectedDate = datetime.datetime.today()
        self.selectedDate = selectedDate

        # Configuration data
        if self.parent and self.parent.config:
            self.config = self.parent.config
        else:
            self.config = Config()

        # Private copy of any record passed
        self.currentrecord = record

        self.alarm = [None, None]

        # TODO: This needs to be run BEFORE connecting the widgets
        self._set_currency()

        # Set up the UI
        self._initialize_dialog_widgets()
        self._connect_fields()
        self.category_index_before = 0

        self.connect("response", self._on_response)

        # If a record was passed, we're in edit mode
        if record:
            self._populate_fields()
            #in edit mode we must disable repetition
            self.repeatSpinner.set_sensitive(False)
            self.frequency.set_sensitive(False)
            self.repeatlabel.set_sensitive(False)

        else:
            # Use alarm values from preferences
            if self.config.get('Alarm', 'show_alarm') == 'true':
                atime = self.config.get('Alarm', 'show_alarm_at_time')
                adays = self.config.getint('Alarm', 'show_alarm_before_days')
                alarmDate = scheduler.get_alarm_timestamp(adays, atime, selectedDate)
                self.alarmbutton.set_date(alarmDate)

    def _set_currency(self):
        self.decimal_sep = locale.localeconv()['mon_decimal_point']
        self.thousands_sep = locale.localeconv()['mon_thousands_sep']

        self.allowed_digts = [self.decimal_sep , self.thousands_sep]
        self.allowed_digts += [str(i) for i in range(10)]

    def _initialize_dialog_widgets(self):
        self.vbox.set_spacing(8)
        self.topcontainer = gtk.HBox(homogeneous=False, spacing=0)
        self.calbox = gtk.VBox(homogeneous=False, spacing=0)
        self.fieldbox = gtk.VBox(homogeneous=False, spacing=0)

        # Add calendar and label
        self.callabel = gtk.Label()
        self.callabel.set_markup("<b>%s</b> " % _("Due Date:"))
        self.callabel.set_alignment(0.00, 0.50)
        self.calendar = gtk.Calendar()
        ## repeat times
        self.repeatlabel = gtk.Label()
        self.repeatlabel.set_markup("<b>%s</b> " % _("Repeat:"))
        self.repeatlabel.set_alignment(0.00, 0.50)
        adj = gtk.Adjustment(00.0, 1.0, 23.0, 1.0)
        self.repeatSpinner = gtk.SpinButton(adj, 0, 0)
        self.repeatSpinner.set_tooltip_text(_("How many times to repeat this bill."))
        self.repeatSpinner.set_wrap(True)
        self.repeatSpinner.set_numeric(True)
        self.repeatSpinner.set_update_policy(gtk.UPDATE_IF_VALID)
        self.repeatSpinner.set_snap_to_ticks(True)
        ## Repeating bills
        self.frequency = gtk.combo_box_new_text()
        self.frequency.connect('changed', self._on_frequency_changed)
        #self.frequency.set_row_separator_func(self._determine_separator)
        self._populate_frequency()
        hbox = gtk.HBox(homogeneous=False, spacing=0)
        hbox.pack_start(self.repeatlabel, expand=True, fill=True, padding=0)
        hbox.pack_start(self.frequency, expand=True, fill=True, padding=0)
        hbox.pack_start(self.repeatSpinner, expand=True, fill=True, padding=0)
        ## Pack it all up
        self.calbox.pack_start(self.callabel,
           expand=True, fill=True, padding=5)
        self.calbox.pack_start(self.calendar,
           expand=True, fill=True, padding=5)
        self.calbox.pack_start(hbox,
           expand=True, fill=True, padding=5)

        # Fields
        ## Table of 5 x 2
        self.table = gtk.Table(rows=5, columns=2, homogeneous=False)
        ### Spacing to make things look better
        self.table.set_col_spacing(0, 6)
        self.table.set_row_spacing(0, 6)
        self.table.set_row_spacing(1, 6)
        self.table.set_row_spacing(2, 6)
        self.table.set_row_spacing(3, 6)

        ## Labels
        self.payeelabel = gtk.Label()
        self.payeelabel.set_markup("<b>%s</b> " % _("Payee:"))
        self.payeelabel.set_alignment(0.00, 0.50)
        self.amountlabel = gtk.Label()
        self.amountlabel.set_markup("<b>%s</b> " % _("Amount:"))
        self.amountlabel.set_alignment(0.00, 0.50)
        self.categorylabel = gtk.Label()
        self.categorylabel.set_markup("<b>%s</b> " % _("Category:"))
        self.categorylabel.set_alignment(0.00, 0.50)
        self.noteslabel = gtk.Label()
        self.noteslabel.set_markup("<b>%s</b> " % _("Notes:"))
        self.noteslabel.set_alignment(0.00, 0.50)
        self.alarmlabel = gtk.Label()
        self.alarmlabel.set_markup("<b>%s</b> " % _("Alarm:"))
        self.alarmlabel.set_alignment(0.00, 0.50)
        ## Fields
        ### Payee
        self.payee = gtk.ComboBoxEntry()
        self.payeecompletion = gtk.EntryCompletion()
        self.payee.child.set_completion(self.payeecompletion)
        self._populate_payee() # Populate combobox with payee from db
        ### Amount
        self.amount = gtk.Entry()
        self.amount.set_alignment(1.00)
        ### Category
        self.categorydock = gtk.HBox(homogeneous=False, spacing=0)
        self.category = gtk.ComboBox()
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
        self._populate_category() # Populate combobox with category from db
        ### Notes
        self.notesdock = gtk.ScrolledWindow()
        self.notesdock.set_shadow_type(gtk.SHADOW_OUT)
        self.notesdock.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.notes = gtk.TextView()
        self.notes.set_wrap_mode(gtk.WRAP_WORD)
        self.notesdock.add_with_viewport(self.notes)
        ### Buffer object for Notes field
        self.txtbuffer = self.notes.get_buffer()
        ### Alarm
        self.alarmbutton = DateButton(self)
        self.alarmbutton.set_tooltip_text(_("Select Date and Time"))
        # Event responsible for updating alarm date
        self.calendar.connect("day_selected", self._on_calendar_day_selected)
        self.calendar.select_day(self.selectedDate.day)
        self.calendar.select_month(self.selectedDate.month - 1, self.selectedDate.year)
        self.calendar.mark_day(self.selectedDate.day)


        ## Pack it all into the table
        self.table.attach(self.payeelabel, 0, 1, 0, 1, gtk.FILL, gtk.FILL)
        self.table.attach(self.amountlabel, 0, 1, 1, 2, gtk.FILL, gtk.FILL)
        self.table.attach(self.categorylabel, 0, 1, 2, 3, gtk.FILL, gtk.FILL)
        self.table.attach(self.noteslabel, 0, 1, 3, 4, gtk.FILL, gtk.FILL)
        self.table.attach(self.alarmlabel, 0, 1, 4, 5, gtk.FILL, gtk.FILL)
        self.table.attach(self.payee, 1, 2, 0, 1, gtk.FILL, gtk.FILL)
        self.table.attach(self.amount, 1, 2, 1, 2, gtk.FILL, gtk.FILL)
        self.table.attach(self.categorydock, 1, 2, 2, 3, gtk.FILL, gtk.FILL)
        self.table.attach(self.notesdock, 1, 2, 3, 4, gtk.FILL, gtk.FILL)
        self.table.attach(self.alarmbutton, 1, 2, 4, 5, gtk.FILL, gtk.FILL)

        ## Pack table
        self.fieldbox.pack_start(self.table, expand=True, fill=True, padding=0)

        # Everything
        self.topcontainer.pack_start(self.calbox,
             expand=False, fill=False, padding=10)
        self.topcontainer.pack_start(self.fieldbox,
             expand=False, fill=False, padding=10)
        self.vbox.pack_start(self.topcontainer,
             expand=False, fill=True, padding=10)

        # Show all widgets
        self.show_all()

    def _connect_fields(self):
        self.category.connect("changed", self._on_categorycombo_changed)
        self.categorybutton.connect("clicked",
            self._on_categoriesbutton_clicked)
        self.amount.connect("insert-text", self._on_amount_insert)


    def _determine_separator(self, model, iter, data=None):
        return model.get_value(iter, 1) == "---"

    def _populate_fields(self):
        # Format the amount field
        self.amount.set_text(utils.float_to_currency(self.currentrecord.AmountDue))
        # Format the dueDate field
        dt = scheduler.datetime_from_timestamp(self.currentrecord.DueDate)
        self.calendar.select_day(dt.day)
        self.calendar.select_month(dt.month - 1, dt.year)
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
        empty_color = create_pixbuf(rgb=(255,255,255))
        empty_color= empty_color.add_alpha (True, chr(255), chr(255),chr(255))
        for rec in records:
            #if [rec['categoryname'], rec['id']] not in categories:
            #TODO: Better put color creation in a function
            color = gtk.gdk.color_parse(rec['color'])
            red = color.red * 255 / 65535
            green = color.green * 255 / 65535
            blue = color.blue * 255 / 65535
            rgb = (red, green, blue)

            categories.append([create_pixbuf(rgb=rgb), rec['categoryname'], int(rec['id'])])
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

        repeat = int(self.repeatSpinner.get_value())
        frequency = self.frequency.get_active_text()
        # Extracts the date off the calendar widget
        # Create datetime object
        selectedDate = scheduler.time_from_calendar(self.calendar.get_date())

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
        if not payee.strip() or not self.amount.get_text().strip():
            return None

        amount = utils.currency_to_float(self.amount.get_text())

        if self.currentrecord is None:
            # Verify how many bills will be inserted
            # this will only work for new bills
            if frequency == scheduler.SC_ONCE:
                self.currentrecord = Bill(payee, category, selectedDate,
                    amount, sbuffer, 0, -1, alarm)
                return [self.currentrecord]
            else:
                # if we are to add more than one bill
                records = []
                records.append (Bill(payee, category, selectedDate,
                    amount, sbuffer + (' (%s of %s)' % (1,repeat)), 0, -1, alarm))
                # calc next dates depending of frequency chosen.
                for i in range(1, repeat):
                    selectedDate = scheduler.get_schedule_timestamp(frequency, selectedDate)
                    if alarm != -1:
                        alarm = scheduler.get_schedule_timestamp(frequency, alarm)
                    records.append (Bill(payee, category, selectedDate,
                        amount, sbuffer + (' (%s of %s)' % (i +1 ,repeat )), 0, -1, alarm))
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
            self.repeatSpinner.set_value(1)
            self.repeatSpinner.set_sensitive(False)
        else:
            self.repeatSpinner.set_sensitive(True)

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
            elif not self.amount.get_text().strip():
                message.ShowError(_("\"%s\" is required field.") % _("Amount"), self)
                self.emit_stop_by_name("response")
                self.amount.grab_focus()

    def _on_calendar_day_selected(self, widget):
        # Only reprogram alarm if it is not None
        if self.alarmbutton.get_date():
            # Use alarm values from preferences
            atime = self.config.get('Alarm', 'show_alarm_at_time')
            adays = self.config.getint('Alarm', 'show_alarm_before_days')
            # Extracts the date off the calendar widget
            selDate = self.calendar.get_date()
            selDate = scheduler.time_from_calendar(selDate)

            alarmDate = scheduler.get_alarm_timestamp(adays, atime, selDate)
            self.alarmbutton.set_date(alarmDate)
