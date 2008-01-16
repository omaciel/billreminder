# -*- coding: utf-8 -*-

__all__ = ['ViewCategory']

import gtk

from gui.widgets.genericlistview import GenericListView
from lib import i18n

class ViewCategory(GenericListView):
    """
    This class represents a ListView for categories.
    """
    # TODO: list search

    def id_cell_data_function(self, column, cell, model, iter):
        id = model.get_value(iter, 0)
        cell.set_property('text', id)
        column.set_visible(False)

    def category_cell_data_function(self, column, cell, model, iter):
        category = model.get_value(iter, 2)
        cell.set_property('text', category)
        column.set_visible(True)

    def color_cell_data_function(self, column, cell, model, iter):
        color = model.get_value(iter, 3)
        cell.set_property('text', color)
        column.set_visible(False)

    # This dictionary represents the columns displayed by the listview.
    # It is indexed by the order you want them to be displayed, followed
    # by the column title and cellrenderer type.
    columns = {
        0: ['Id',
            gtk.CellRendererText(), id_cell_data_function],
        1: [None,
            gtk.CellRendererPixbuf(), None],
        2: [_('Category'),
            gtk.CellRendererText(), category_cell_data_function],
        3: [None,
            gtk.CellRendererText(), color_cell_data_function],
    }

    def __init__(self):
        GenericListView.__init__(self, self.columns)
        # Set the following column to invisible
        id = self.get_column(0)
        id.set_cell_data_func(id.get_cell_renderers()[0],
                              self.id_cell_data_function)
        id.set_visible(False)

        category = self.get_column(2)
        category.set_cell_data_func(category.get_cell_renderers()[0],
                                    self.category_cell_data_function)

        color = self.get_column(3)
        color.set_cell_data_func(color.get_cell_renderers()[0],
                              self.color_cell_data_function)
        color.set_visible(True)
