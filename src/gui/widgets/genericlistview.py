# -*- coding: utf-8 -*-

"""
Copyright (c) 2007, Og Macieli <omaciel@foresightlinux.org>

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted
provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice, this list of
      conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice, this list
      of conditions and the following disclaimer in the documentation and/or other materials
      provided with the distribution.
    * Neither the name of the Og Maciel nor the names of its contributors may be used to
      endorse or promote products derived from this software without specific prior written
      permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
“AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import gtk
import gobject

class GenericListView(gtk.TreeView):
    """
    This class represent a generic ListView
    """

    def __init__ (self, columns=None):
        """
        Constructor

        @type columns: dictionary
        @param columns: Dictionary containing ordered list of the columns to be displayed,
            with the index as its key, followed by a list containing the column
            title, and gtk.CellRenderer type.
            Ex: columns = {0: [None, gtk.CellRendererToggle()]}
        @rtype: None
        @return: None.
        """
        # Call the super class
        gtk.TreeView.__init__ (self)

        # If columns were passed, use them.  Else, columns from derived class.
        if columns:
            self.columns = columns

        #self.set_fixed_height_mode(True)

        # Setup the list
        self._setupListView(self.columns)

    def _setupListView(self, columns):
        """
        Initializes the ListView object by dynamically creating a ListStore
        and adding necessary columns based on the @columns parameter.

        @type columns: dictionary
        @param columns: Dictionary containing ordered list of the columns to be displayed,
            with the index as its key, followed by a list containing the column
            title, gtk.CellRenderer type, and custom function.
            Ex: columns = {0: [None, gtk.CellRendererToggle(), myfunction]}
        @rtype: None
        @return: None.
        """
        # Temporary containers for datatypes and treeviewcolumns
        dataTypes = []
        treeViewColumns = []
        # Extract information from dictionary value
        for key, value in columns.items():
            # Column title
            title = value[0]
            # Column gtk.CellRenderer
            cellrenderer = value[1]

            # Get data type 
            dataType = self._getColumnInfo(cellrenderer)
            # Get gtk.TreeViewColumn
            tvColumn = self._getTreeViewColumn(title, cellrenderer, key)
            # Add to temporary datatype and treeviewcolumns containers
            dataTypes.append(dataType)
            treeViewColumns.append(tvColumn)

        # Defines the TreeStore
        self.listStore = gtk.TreeStore(*dataTypes)
        self.filtered_model = self.listStore.filter_new()
        
        self.sorted_model = gtk.TreeModelSort(self.filtered_model)
        
        # Associates the listStore to the ListView object
        self.set_model(self.sorted_model)

        # Add columns to the List
        for column in treeViewColumns:
            self.append_column(column)

        # If TRUE, hint to the theme engine to draw rows in alternating colors.
        self.set_rules_hint(True)

    def _getTreeViewColumn(self, title, type, index):
        """
        Returns a gtk.TreeViewColumn with the title, gtk.CellRenderer,
        and attributes based on the title and CellRendererType passed.

        @type title: string
        @param title: String containing text to display as column header.
        @type type: gtk.CellRenderer
        @param type: gtk.CellRenderer to associate with column.
        @type index: integer
        @param index: This is the location where the new gtk.TreeViewColumn will obtain its data.
        @rtype: gtk.TreeViewColumn
        @return: Returns a gtk.TreeViewColumn with the title, gtk.CellRenderer,
            and attributes based on the title and CellRendererType passed.
        """
        if isinstance(type, gtk.CellRendererToggle):
            tvcolumn = gtk.TreeViewColumn(title, type, active=index)
        elif isinstance(type, gtk.CellRendererPixbuf):
            tvcolumn = gtk.TreeViewColumn(title, type, pixbuf=index)
        elif isinstance(type, gtk.CellRendererText):
            tvcolumn = gtk.TreeViewColumn(title, type, text=index)
        else:
            tvcolumn = gtk.TreeViewColumn(title, type, text=index)

        tvcolumn.set_resizable(True)
        tvcolumn.set_clickable(True)
        tvcolumn.set_sort_column_id(index)

        return tvcolumn

    def _getColumnInfo(self, value):
        """
        Return the data type to be used when building a gtk.ListStore.

        @type value: gtk.CellRenderer
        @param value: The gtk.CellRenderer associated with column.
        @rtype: GObject
        @return: Returns a tuple containing the data type (GObject).
        """
        if isinstance(value, gtk.CellRendererToggle):
            value.connect ("toggled", self.toggled_item)
            type = gobject.TYPE_BOOLEAN
        elif isinstance(value, gtk.CellRendererText):
            type = gobject.TYPE_STRING
        elif isinstance(value, gtk.CellRendererPixbuf):
            type = gtk.gdk.Pixbuf
        else:
            type = gobject.TYPE_NONE

        return type

    # Events
    # TODO: Remove this from here and move it to the inherited class.
    def toggled_item(self, cell, path):
        """
        Toggles CellRendererToggle on/off.

        @type : integer
        @param : .
        @rtype: list
        @return: .
        """
        self.listStore[path][0] = not self.listStore[path][0]

    # Control Procedures 
    def add(self, value, parent=None):
        """
        Add an item to the internal liststore

        @type value: list
        @param value: List containing the data to add to the internal liststore.
        @type parent: gtk.TreeIter
        @param parent: Parent node or None.
        @rtype: gtk.TreeIter
        @return: A gtk.TreeIter pointing at the new row.
        """
        return self.listStore.append(parent, value)

    def addList(self, values, parent=None):
        """
        Add multiple itens to the internal liststore

        @type values: list
        @param values: List of lists containing the data to add to the internal liststore.
        @type parent: gtk.TreeIter
        @param parent: Parent node or None.
        @rtype: None
        @return: None.
        """
        # Removes the model so the addition is quicker
        self.set_model(None)
        # Freezes list so to cancel refresh event
        self.freeze_child_notify()

        for value in values:
            self.listStore.append(parent, value)

        # set model back
        self.set_model(self.listStore)
        # Unfreeze the list
        self.thaw_child_notify()

    def remove(self):
        """
        Remove the selected row

        @rtype: None
        @return: None.
        """
        #http://eccentric.cx/misc/pygtk/pygtkfaq.html#13.8
        selection = self.get_selection() 
        model, iter = selection.get_selected()
        if iter:
          path = model.get_path(iter)
          model.remove(iter)
          # now that we removed the selection, play nice with 
          # the user and select the next item
          selection.select_path(path)

          # well, if there was no selection that meant the user
          # removed the last entry, so we try to select the 
          # last item
          if not selection.path_is_selected(path):
             row = path[0]-1
             # test case for empty lists
             if row >= 0:
                selection.select_path((row,))

    def getSelectedRow(self):
        """
        Get the entire selected row.

        @rtype: list
        @return: Returns a list containing the data from the selected row.
        """
        selection = self.get_selection()
        model, paths = selection.get_selected_rows()

        # Returns first selected row
        return paths[0]

    def getSelectedItem(self, index):
        """
        Return the indexed item from the selected row.

        @type index: integer
        @param index: Index of the column item to return.
        @rtype: str
        @return: Returns the value for the cell in the selected row.
        """
        selection = self.get_selection()
        model, iter, = selection.get_selected()
        return  self.store.get_value(iter, index)

    def getCount(self):
        """
        Returns the number of itens in the list.

        @rtype: int
        @return: Returns the number of itens in the list.
        """

        return len(self.listStore)
