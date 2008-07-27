# -*- coding: utf-8 -*-

__all__ = ['DateButton']

import gtk
import gobject
import time
import datetime
from timewidget import TimeWidget

from lib import i18n

class DateButton(gtk.Button):
    def __init__(self, parent=None):
        gtk.Button.__init__(self)
        self.parent_window = parent
        #TRANSLATORS: No date selected
        self.set_label(_("None"))
        self.date = None

        self.connect("clicked", self.show_calendar)

    def set_date(self, date):
        if not date:
            self.date = None
            self.set_label(_("None"))
            return

        # Create datetime object
        self.date = datetime.datetime.fromtimestamp(date)

        self.set_label(self.date.strftime(_('%Y/%m/%d %H:%M').encode('ASCII')))

    def get_date(self):
        if not self.date:
            return None
        return time.mktime(self.date.timetuple())

    def show_calendar(self, *arg):
        self.dialog = gtk.Dialog(title=_("Select Date and Time"),
                            parent=self.parent_window,
                            flags=gtk.DIALOG_MODAL |gtk.DIALOG_DESTROY_WITH_PARENT |gtk.DIALOG_NO_SEPARATOR,
                            buttons=(str(_("_None")), gtk.RESPONSE_REJECT,
                                     gtk.STOCK_OK, gtk.RESPONSE_OK))
        
        self.dialog.set_border_width(6)
        self.dialog.set_resizable(False)
        self.dialog.vbox.set_spacing(6)
        
        self._initialize_dialog_widgets()
        self._populate_fields()

        response = self.dialog.run()
        
        if response == gtk.RESPONSE_REJECT:
            self.set_date(None)
        elif response == gtk.RESPONSE_OK:
            # Extracts the date off the calendar widget
            day = self.calendar.get_date()[2]
            month = self.calendar.get_date()[1] + 1
            year = self.calendar.get_date()[0]
            # TODO: Add verification routine
            hour ,minute = self.time.getTime()
            self.date = datetime.datetime(year, month, day, int(hour), int(minute))
            self.set_label(self.date.strftime(_('%Y/%m/%d %H:%M').encode('ASCII')))

        self.dialog.destroy()

    def _initialize_dialog_widgets(self):
        dialog = gtk.Dialog(title=_("Select date and time"),
            parent=self.parent_window,
            flags=gtk.DIALOG_MODAL |gtk.DIALOG_DESTROY_WITH_PARENT |gtk.DIALOG_NO_SEPARATOR,
            buttons=(str(_("_None")), gtk.RESPONSE_REJECT,
                     gtk.STOCK_OK, gtk.RESPONSE_OK))
        
        dialog.set_border_width(6)
        dialog.set_resizable(False)
        
        if self.parent_window:
            dialog.set_transient_for(self.parent_window)
            dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)

        self.calendarlabel = gtk.Label()
        self.calendarlabel.set_markup_with_mnemonic("<b>_Date:</b>")
        self.calendarlabel.set_alignment(0.00, 0.50)

        self.vbox = gtk.VBox(False, 6)
        self.vbox.set_border_width(6)
        self.calendar = gtk.Calendar()
        self.calendarlabel.set_mnemonic_widget(self.calendar)
        # If we do have an existing alarm time, pass it to the widget
        self.timehbox = gtk.HBox(False, 4)
        title = gtk.Label()
        title.set_markup_with_mnemonic(_("<b>_Time:</b>"))
        self.timehbox.pack_start(title, expand=False)
        self.time = TimeWidget(self.date and time.mktime(self.date.timetuple()) or None)
        title.set_mnemonic_widget(self.time.hourSpinner)
        self.timehbox.pack_start(self.time)
        self.vbox.pack_start(self.calendarlabel, False, True, 0)
        self.vbox.pack_start(self.calendar, False, True, 0)
        self.vbox.pack_start(self.timehbox, False, True, 0)
        self.dialog.vbox.pack_start(self.vbox, expand=False, fill=True)

        self.dialog.show_all()


    def _populate_fields(self):
        if self.date:
            self.calendar.select_day(self.date.day)
            self.calendar.select_month(self.date.month - 1, self.date.year)
