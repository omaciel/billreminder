#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

from charting import Chart

class ChartWidget(gtk.EventBox):
    def __init__(self):
        gtk.EventBox.__init__(self)
        self.chart = Chart(
            max_bar_width = 40,
            animate = False,
            values_on_bars = True,
            stretch_grid = True,
            legend_width = 80)

        self.add(self.chart)

    def plot(self, data):
        """
        Populates chart with data passed in.
        """
        self.chart.plot(data)

class BasicWindow:

    # close the window and quit
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def __init__(self):
        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.window.set_title("Basic Window")

        self.window.set_size_request(500, 200)

        self.window.connect("delete_event", self.delete_event)

        #self.activity_chart = Chart(max_bar_width = 20, collapse_whitespace = True)
        self.chart = ChartWidget()

        place = gtk.Frame()
        place.add(self.chart)
        self.window.add(place)
        self.window.show_all()

        data = [["Rent", 790, '#808080'], ["Gas", 120], ["Food", 280],
                ["Education", 60], ["Utilities", 140, '#1a3def'], ["Insurance", 0], ["Travel", 0]]
        self.chart.plot(data)


def main():
    gtk.main()

if __name__ == "__main__":
    example = BasicWindow()
    main()
