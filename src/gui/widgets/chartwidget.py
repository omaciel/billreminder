#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

from charting import BarChart

class ChartWidget(gtk.EventBox):
   background = (0.975, 0.975, 0.975)
   x_offset = 90 # align all graphs to the left edge

   def __init__(self):
       gtk.EventBox.__init__(self)

       self.chart = BarChart(
           background = self.background,
           bar_base_color = (238,221,221),
           legend_width = self.x_offset,
           max_bar_width = 35,
           values_on_bars = True
       )

       self.add(self.chart)

   def plot(self, keys, values):
       """
       Populates chart with data passed in.
       """
       self.chart.plot(keys, values)


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

       self.chart.plot(['None', 'House'], [150.0, 132.55])


def main():
   gtk.main()

if __name__ == "__main__":
   example = BasicWindow()
   main()
