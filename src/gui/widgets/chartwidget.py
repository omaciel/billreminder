#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

import sys
import cairo
from pycha import bar

class ChartWidget(gtk.HBox):
    def __init__(self):
        gtk.HBox.__init__(self)
        self.chart = gtk.Image()

        self.add(self.chart)

    def plot(self, data):
        """
        Populates chart with data passed in.
        """
        pass
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 400, 200)

        dataSet = (
            ('data', [(i, l[1]) for i, l in enumerate(data)]),

        )

        options = {
            'axis': {
                'x': {
                    'ticks': [dict(v=i, label=l[0]) for i, l in enumerate(data)],

                    'rotate': 25,
                    'label': 'Categories',
                },
                'y': {
                    #'tickCount': 2,
                    'label': 'Amount',
                }
            },
            'colorScheme': {
                'name': 'gradient',
                'args': {
                    'initialColor': 'red',
                },
            },
            'colorScheme': {
                'name': 'gradient',
                'args': {
                    'initialColor': 'red',
                },
               #'name': 'fixed',
               #'args': {
               #    'colors': ['#ff0000', '#00ff00', '#ff0000', '#00ff00'],
               #},
            },
            'legend': {
                'hide': True,
            },
            'padding': {
                'left': 45,
                'bottom': 45,
            },
        }

        chart = bar.VerticalBarChart(surface, options)

        chart.addDataset(dataSet)
        chart.render()

        #TODO: the widget's Image object should take a dynamically created image object
        surface.write_to_png('foobar.png')

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

        #data = [(None, 150.0), (u'House', 132.55000000000001)]
        #self.chart.plot(data)


def main():
    gtk.main()

if __name__ == "__main__":
    example = BasicWindow()
    main()
