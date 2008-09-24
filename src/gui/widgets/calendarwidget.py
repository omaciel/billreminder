#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

import gobject
import datetime

from lib import i18n

MINDATE = 1900
MAXDATE = 3000

class CalendarWidget(gtk.HBox):

    currentDate = None

    #     #define a custom signal
    __gsignals__ = dict(date_changed=(gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,)))

    def __init__(self, currentDate=None):
        gtk.HBox.__init__(self, False, 4)

        if not currentDate:
            currentDate = datetime.datetime.today()

        self.currentDate = currentDate
        self.currentYear = self.currentDate.year
        self.currentMonth = self.currentDate.month

        self.initialize_interface()
        self.initialize_values()

    def set_currentDate (self, value):
        self.currentDate  = value
        self.currentYear = self.currentDate.year
        self.currentMonth = self.currentDate.month
        self.emit_date_changed_signal()

    def emit_date_changed_signal(self):
        self.emit("date_changed", self.currentDate)


    def get_months (self):
        year = self.currentYear
        months = [datetime.datetime(year, x, 1).strftime("%B") for x in range(1,13)]

        return months

    def initialize_interface(self):

        label1 = gtk.Label()
        label1.set_markup_with_mnemonic(_("<b>_Monthly Report:</b>"))

        self.monthSelector = gtk.combo_box_new_text()
        self.monthSelector.connect("changed", self._on_monthSelector_changed)
        self.populate_month_selector()

        label2 = gtk.Label()
        label2.set_markup_with_mnemonic(_("<b>_Year:</b>"))

        placeHolder1 = gtk.Label()

        # gtk.Adjustment(value=0, lower=0, upper=0, step_incr=0, page_incr=0, page_size=0)
        adj = gtk.Adjustment(self.currentYear, MINDATE, MAXDATE, 1)
        self.yearSpinner = gtk.SpinButton(adj, 0, 0)
        self.yearSpinner.set_numeric(True)
        self.yearSpinner.set_update_policy(gtk.UPDATE_IF_VALID)
        self.yearSpinner.set_snap_to_ticks(True)
        self.yearSpinner.connect("changed", self._on_yearSpinner_changed)

        label1.set_mnemonic_widget(self.monthSelector)
        label2.set_mnemonic_widget(self.yearSpinner)

        placeHolder2 = gtk.Label()

        self.pack_start(label1, expand=False, fill=False, padding=4)
        self.pack_start(self.monthSelector, expand=False, fill=False, padding=4)
        self.pack_start(placeHolder1, expand=True, fill=True, padding=0)
        self.pack_start(placeHolder2, expand=True, fill=True, padding=0)
        self.pack_start(label2, expand=False, fill=False, padding=4)
        self.pack_start(self.yearSpinner, expand=False, fill=False, padding=4)

    def initialize_values(self):
        self.monthSelector.set_active(self.currentMonth - 1)
        self.yearSpinner.set_value(self.currentYear)

    def populate_month_selector(self):
        store = gtk.ListStore(gobject.TYPE_STRING)
        self.monthSelector.set_model(store)

        for month in self.get_months():
            store.append([month])

    def _on_yearSpinner_changed(self, spin):
        self.update_current_date()

    def _on_monthSelector_changed(self, combo):
        self.update_current_date()

    def update_current_date(self):
        index = self.monthSelector.get_active()

        month = index + 1
        year = int(self.yearSpinner.get_value())

        changedDate = datetime.datetime(year, month, 1)
        self.set_currentDate(changedDate)

gobject.type_register(CalendarWidget)

class BasicWindow:

    # close the window and quit
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def __init__(self):
        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.window.set_title("Basic Window")

        #self.window.set_size_request(500, 200)

        self.window.connect("delete_event", self.delete_event)

        self.calendar = CalendarWidget()
        self.calendar.connect("date_changed", self._on_calendar_date_changed)
        self.window.add(self.calendar)

        self.window.show_all()

    def _on_calendar_date_changed(self, widget, args):
        print args

def main():
    gtk.main()

if __name__ == "__main__":
    example = BasicWindow()
    main()
