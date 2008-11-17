#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

import gobject
import datetime

from lib import i18n

class DatePicker(gtk.VBox):

    currentDate = None

    #     #define a custom signal
    __gsignals__ = dict(
        date_changed=(
            gobject.SIGNAL_RUN_FIRST,
            gobject.TYPE_NONE, 
            (gobject.TYPE_PYOBJECT,)
        )
    )

    def __init__(self, date=None):
        gtk.VBox.__init__(self, False, 4)

        if not date:
            date = datetime.datetime.today()
        self.currentDate = date

        # Create a new calendar
        self.calendar = gtk.Calendar()
        self.calendar.connect("day-selected-double-click", self.on_day_selected)
        self.calendar.select_month(date.month, date.year)
        self.calendar.select_day(date.day)

        # Label to display the date selected
        #TRANSLATORS: This is the date that is selected from the calendar. Try to keep it small.
        self.entry = gtk.Label(self.currentDate.strftime(_('%m/%d/%Y').encode('ASCII')))

        # Expander for the calendar
        self.expander = gtk.Expander()
        self.expander.set_expanded(False)
        self.expander.set_label_widget(self.entry)

        vbox = gtk.VBox(False, 4)
        vbox.pack_start(self.calendar, expand=True, padding=1)

        self.expander.add(vbox)

        self.pack_start(self.expander)

    def emit_date_changed_signal(self):
        # Hide the calendar
        self.expander.set_expanded(False)

        self.emit("date_changed", self.currentDate)

    def on_day_selected(self, calendar):
        (year, month, day) = self.calendar.get_date()
        self.currentDate = datetime.datetime(year, month+1, day)
        #TRANSLATORS: This is the date that is selected from the calendar. Try to keep it small.
        self.entry.set_label(self.currentDate.strftime(_('%m/%d/%Y').encode('ASCII')))


        self.emit_date_changed_signal()

class BasicWindow(object):

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

        hbox = gtk.HBox()

        datepicker = DatePicker(datetime.datetime(1974, 6, 8))
        hbox.pack_start(datepicker)
        self.window.add(hbox)
        self.window.show_all()

def main():
    gtk.main()

if __name__ == "__main__":
    example = BasicWindow()
    main()
