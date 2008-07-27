# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import gobject
import datetime
from lib import i18n

class TimeWidget(gtk.HBox):
    def __init__(self, notificationTime=None):

        gtk.HBox.__init__(self, False, 4)

        # Create internal widgets
        self.__initialize_widgets()
        # Initialize their values
        self.__set_time(notificationTime)

    def __initialize_widgets(self):
        # Hour and minutes spinners
        """#More Compact
        vbox = gtk.VBox(False, 0)
        hbox.pack_start(vbox, True, True, 5)
        label = gtk.Label(_("Hour :"))
        label.set_alignment(0, 0.5)
        vbox.pack_start(label, False, True, 0)
        vbox.pack_start(self.hourSpinner, False, True, 0)
        vbox = gtk.VBox(False, 0)
        hbox.pack_start(vbox, True, True, 5)
        label = gtk.Label(_("Minute :"))
        label.set_alignment(0, 0.5)
        """
        self.hourSpinner = self.__set_spinner(00.0, 00.0, 23.0, 1.0)
        self.pack_start(self.hourSpinner, True, True, 0)
        self.pack_start(gtk.Label(":"), False, True, 0)
        self.minuteSpinner = self.__set_spinner(0.0, 0.0, 59.0, 1.0)
        self.pack_start(self.minuteSpinner, True, True, 0)
        self.pack_start(gtk.Label(_("(hh/mm)")), False, True, 0)
        """"
        vbox.pack_start(label, False, True, 0)
        vbox.pack_start(self.minuteSpinner, False, True, 0)
        """

    def __set_spinner(self, initial, low, high, increment=1.0):
        adj = gtk.Adjustment(initial, low, high, increment)
        spinner = gtk.SpinButton(adj, 0, 0)
        spinner.set_wrap(True)
        spinner.set_numeric(True)
        spinner.set_update_policy(gtk.UPDATE_IF_VALID)
        spinner.set_snap_to_ticks(True)
        spinner.connect("output", self.__on_output)

        return spinner

    def __set_time(self,  notificationTime=None):

        if notificationTime:
            dt = datetime.datetime.fromtimestamp(notificationTime)
        else:
            dt = datetime.datetime.now()
        hour = dt.hour
        minute = dt.minute
        self.hourSpinner.set_value(float(hour))
        self.minuteSpinner.set_value(float(minute))

    def __on_output(self, spinbutton):
        spinbutton.set_text("%02d" % spinbutton.get_adjustment().get_value())
        return True


    def setHourMinute(self, hour, minute):
        if not hour or not minute:
            return True

        self.hourSpinner.set_value(float(hour))
        self.minuteSpinner.set_value(float(minute))

    def getTime(self):
        return (self.hourSpinner.get_value_as_int(), self.minuteSpinner.get_value_as_int())
