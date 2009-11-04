# -*- coding: utf-8 -*-

__all__ = ['Toolbar']

import gtk

class Toolbar(gtk.Toolbar):
    def __init__(self):
        gtk.Toolbar.__init__(self)

        self.set_tooltips(True)
        self.set_border_width(1)

    def add_space(self):
        self.insert(gtk.SeparatorToolItem(), -1)

    def add_button(self, image, title, tip_text=None, callback=None):
        toolitem = gtk.ToolButton(image)
        toolitem.set_label(title)
        toolitem.set_tooltip_text(tip_text)
        if callback:
            toolitem.connect('clicked', callback)
        self.insert(toolitem,-1)

        return toolitem

    def add_stock(self, stock_id, tip_text=None, callback=None):
        toolitem = gtk.ToolButton(stock_id)
        toolitem.set_tooltip_text(tip_text)
        if callback:
            toolitem.connect('clicked', callback)
        self.insert(toolitem,-1)

    def add_toggle(self, stock_id, title, tip_text, callback):
        toolitem = gtk.ToggleToolButton(stock_id)
        toolitem.connect('toggled', callback)
        toolitem.set_tooltip_text(tip_text)
        self.insert(toolitem,-1)

    def add_widget(self, widget, tip_text, private_text):
        toolitem = gtk.ToolItem()
        toolitem.add(widget)
        toolitem.set_expand(False)
        toolitem.set_homogeneous(False)
        toolitem.set_tooltip_text(tip_text)
        self.insert(toolitem,-1)
