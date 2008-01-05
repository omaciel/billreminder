#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['DateButton']

import gtk
import gobject
import time
import datetime

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
                            flags=gtk.DIALOG_MODAL,
                            buttons=(str(_("None")), gtk.RESPONSE_REJECT,
                                     gtk.STOCK_OK, gtk.RESPONSE_OK))

        self._initialize_dialog_widgets()
        self._populate_fields()

        response = self.dialog.run()
        print response
        if response == gtk.RESPONSE_REJECT:
            self.set_date(None)
        elif response == gtk.RESPONSE_OK:
            # Extracts the date off the calendar widget
            day = self.calendar.get_date()[2]
            month = self.calendar.get_date()[1] + 1
            year = self.calendar.get_date()[0]
            # TODO: Add verification routine
            hour ,minute = self.time.child.get_text().split(_('%H:%M')[2])
            self.date = datetime.datetime(year, month, day, int(hour), int(minute))
            self.set_label(self.date.strftime(_('%Y/%m/%d %H:%M').encode('ASCII')))

        self.dialog.destroy()

    def _initialize_dialog_widgets(self):
        dialog = gtk.Dialog(title=_("Select date and time"),
                            parent=self.parent_window,
                            flags=gtk.DIALOG_MODAL,
                            buttons=(str(_("None")), gtk.RESPONSE_REJECT,
                                     gtk.STOCK_OK, gtk.RESPONSE_OK))

        if self.parent_window:
            dialog.set_transient_for(self.parent_window)
            dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)

        self.calendarlabel = gtk.Label()
        self.calendarlabel.set_markup("<b>%s </b>" % _("Date:"))
        self.calendarlabel.set_alignment(0.00, 0.50)

        self.timelabel = gtk.Label()
        self.timelabel.set_markup("<b>%s </b>" % _("Time:"))
        self.timelabel.set_alignment(0.00, 0.50)

        self.nothing = gtk.Label()

        self.table = gtk.Table(rows=3, columns=3, homogeneous=False)
        self.calendar = gtk.Calendar()

        self.time = gtk.ComboBoxEntry()
        self.time.child.set_width_chars(6)

        self.table.attach(self.calendarlabel, 0, 3, 0, 1, gtk.FILL, gtk.FILL)
        self.table.attach(self.timelabel, 0, 1, 2, 3, gtk.FILL, gtk.FILL)
        self.table.attach(self.calendar, 0, 3, 1, 2, gtk.FILL, gtk.FILL)
        self.table.attach(self.time, 1, 2, 2, 3, gtk.FILL, gtk.FILL)
        self.table.attach(self.nothing, 2, 3, 2, 3, gtk.FILL | gtk.EXPAND, gtk.FILL)
        self.dialog.vbox.pack_start(self.table, expand=False, fill=True, padding=10)

        self.dialog.show_all()


    def _populate_fields(self):
        store = gtk.ListStore(gobject.TYPE_STRING)
        for i in range(24):
            store.append([_('%H:%M').replace('%H',
                        "%02d" % i).replace('%M', '00')])
            store.append([_('%H:%M').replace('%H',
                        "%02d" % i).replace('%M', '30')])

        self.time.set_model(store)
        self.time.set_text_column(0)
        self.time.child.set_text(datetime.time().strftime(_('%H:%M').encode('ASCII')))

        if self.date:
            self.calendar.select_day(self.date.day)
            self.calendar.select_month(self.date.month - 1, self.date.year)
            self.time.child.set_text(self.date.strftime(_('%H:%M').encode('ASCII')))
