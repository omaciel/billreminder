#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['MainDialog']

import pygtk
pygtk.require('2.0')
import gtk
from gobject import timeout_add

# Import widgets modules
from gui.widgets.toolbar import Toolbar
from gui.widgets.statusbar import Statusbar
from gui.widgets.viewbill import ViewBill as ViewBill
from gui.widgets.trayicon import NotifyIcon

# Import data model modules
from lib.bill import Bill
from lib.dal import DAL
from lib.actions import Actions
from db.billstable import BillsTable

# Import common utilities
from lib import common
from lib import dialogs
from lib.utils import ContextMenu
from lib.utils import get_dbus_interface
from lib.utils import force_string
from lib.utils import create_pixbuf
from lib import i18n
from lib.config import Config


class MainDialog:

    menu_ui = '''
        <ui>
            <menubar name="MenuBar">
              <menu action="File">
                <menuitem action="New"/>
                <menuitem action="Edit"/>
                <menuitem action="Delete"/>
                <separator/>
                <menuitem action="Paid"/>
                <menuitem action="NotPaid"/>
                <separator/>
                <menuitem action="Preferences"/>
                <separator/>
                <menuitem action="Quit"/>
              </menu>
              <menu action="View">
                <menuitem action="PaidRecords"/>
                <menuitem action="NotPaidRecords"/>
                <menuitem action="AllRecords"/>
              </menu>
              <menu action="Help">
                <menuitem action="About"/>
              </menu>
            </menubar>
        </ui>'''

    def __init__(self):
        self.config = Config()

        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("%s" % common.APPNAME)
        self.window.set_border_width(0)
        self.window.set_size_request(500, 300)
        self.window.set_icon_from_file(common.APP_ICON)
        self.window.connect("delete_event", self.on_delete_event)

        self.box = gtk.VBox(homogeneous=False, spacing=0)

        # ViewBill
        self.list = ViewBill()
        self.list.connect('cursor_changed', self._on_list_cursor_changed)
        self.list.connect('button_press_event',
                          self._on_list_button_press_event)

        # Menubar
        self._populate_menubar()

        # Toolbar
        self.toolbar = Toolbar()
        self._populate_toolbar()

        # ScrolledWindow
        self.scrolledwindow = gtk.ScrolledWindow()
        self.scrolledwindow.set_shadow_type(gtk.SHADOW_OUT)
        self.scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                       gtk.POLICY_AUTOMATIC)
        self.scrolledwindow.add(self.list)

        # Statusbar
        self.statusbar = Statusbar()

        # Pack it all up
        self.box.pack_start(self.toolbar,
            expand=False, fill=True, padding=0)
        self.box.pack_start(self.scrolledwindow,
            expand=True, fill=True, padding=0)
        self.box.pack_start(self.statusbar,
            expand=False, fill=True, padding=2)

        self.window.add(self.box)

        # Restore position and size of window
        width = self.config.getint('GUI', 'width')
        height = self.config.getint('GUI', 'height')
        x = self.config.getint('GUI', 'x')
        y = self.config.getint('GUI', 'y')
        if width and height:
            self.window.resize(width, height)
        if x and y:
            self.window.move(x, y)

        self.window.show_all()

        if self.config.getboolean('General', 'start_in_tray'):
            self.window.hide()

        self.toggle_buttons()

        # Connects to the database
        self.actions = Actions()
        if self.config.getint('GUI', 'show_paid_bills') == 0:
            self._populateTreeView(self.actions.get_bills( \
                                   'paid = 1 ORDER BY dueDate DESC'))
        elif self.config.getint('GUI', 'show_paid_bills') == 1:
            self._populateTreeView(self.actions.get_bills( \
                                   'paid = 0 ORDER BY dueDate DESC'))
        else:
            self._populateTreeView(self.actions.get_bills( \
                                   'paid IN (0,1) ORDER BY dueDate DESC'))
        self.notify = NotifyIcon(self)

        # Connects to the Daemon
        self.iface = None
        iface = get_dbus_interface(common.DBUS_INTERFACE, common.DBUS_PATH)
        if iface:
            iface.connect_to_signal("bill_edited", self.reloadTreeView)
            iface.connect_to_signal("show_main_window", self.window.show)
            self.iface = iface
            timeout_add(2000, self._send_tray_hints)

    # Methods:  UI
    def _send_tray_hints(self):
        self.iface.set_tray_hints(force_string(self.notify.get_hints()))
        timeout_add(60000, self._send_tray_hints)

    def get_window_visibility(self):
        return self.window.get_property("visible")

    def show_hide_window(self):
        if self.window.get_property("visible"):
            self.window.hide()
        else:
            self.window.show()

    def _change_view(self, action, current):
        #TODO: Change the records selection based on option chose
        self.config.set("GUI", "show_paid_bills", str(current.get_current_value()))
        self.config.save()
        self.reloadTreeView()
        return True

    def _get_selected_record(self):
        """ Returns a bill object from the current selected record """
        if len(self.list.listStore) > 0:
            model_ = self.list.get_model()
            if self.list.get_cursor()[0]:
                index = self.list.get_cursor()[0][0]
            else:
                index = 0

            b_id = model_[index][0]

            try:
                records = self.actions.get_bills({'Id': b_id})
                self.currentrecord = Bill(records[0])
            except Exception, e:
                print str(e)
                self.currentrecord = None
        else:
            self.currentrecord = None

    def _populateTreeView(self, records):
        """ Populates the treeview control with the records passed """

        # Loops through bills collection
        path = 0
        for rec in records:
            self.list.add(self._formated_row(rec))

        self.list.set_cursor(path)
        return len(records)

    def reloadTreeView(self, *arg):
        # Update list with updated record
        path = self.list.get_cursor()[0]
        self.list.listStore.clear()
        self.currentrecord = None
        if self.config.getint('GUI', 'show_paid_bills') == 0:
            length = self._populateTreeView(self.actions.get_bills( \
                                   'paid = 1 ORDER BY dueDate DESC'))
        elif self.config.getint('GUI', 'show_paid_bills') == 1:
            length = self._populateTreeView(self.actions.get_bills( \
                                   'paid = 0 ORDER BY dueDate DESC'))
        else:
            length = self._populateTreeView(self.actions.get_bills( \
                                   'paid IN (0,1) ORDER BY dueDate DESC'))

        if path and length:
            self.list.set_cursor(path)
        self._update_statusbar()
        return length

    def _formated_row(self, row):
        """ Formats a bill to be displayed as a row. """
        # Make sure the row is created using fields in proper order
        fields = BillsTable.Fields
        # Initial list
        formated = []
        # Loop through 'fields' and color code them
        for key in fields:
            if key == "catId":
                actions = Actions()
                records = actions.get_categories({'id': row[key]})
                if records:
                    name = records[0]['categoryname']
                    color = records[0]['color']
                    color = gtk.gdk.color_parse(color)
                    red = color.red * 255 / 65535
                    green = color.green * 255 / 65535
                    blue = color.blue * 255 / 65535
                    rgb = (red, green, blue)
                else:
                    name = _("None")
                    color = "#000"
                    rgb = (255, 255, 255)
                formated.append(create_pixbuf((8, 16), rgb))
                formated.append(name)
            else:
                formated.append(row[key])
        #formated.append(color)

        return formated

    def _populate_toolbar(self):
        self.btnNew = self.toolbar.add_button(gtk.STOCK_NEW,
            _("New"), _("Add a new record"), self.on_btnNew_clicked)
        self.btnEdit = self.toolbar.add_button(gtk.STOCK_EDIT,
            None, _("Edit a record"), self.on_btnEdit_clicked)
        self.btnRemove = self.toolbar.add_button(gtk.STOCK_DELETE,
            None, _("Delete selected record"), self.on_btnDelete_clicked)
        self.toolbar.add_space()
        self.btnPaid = self.toolbar.add_button(gtk.STOCK_APPLY,
            _("Paid"), _("Mark as paid"), self.on_btnPaid_clicked)
        self.btnPaid.set_is_important(True)
        self.btnUnpaid = self.toolbar.add_button(gtk.STOCK_UNDO,
            _("Not Paid"), _("Mark as not paid"), self.on_btnPaid_clicked)
        self.btnUnpaid.set_is_important(True)
        self.toolbar.add_space()
        self.btnPref = self.toolbar.add_button(gtk.STOCK_PREFERENCES,
            None, _("Edit preferences"), self.on_btnPref_clicked)
        self.btnAbout = self.toolbar.add_button(gtk.STOCK_ABOUT,
            None, _("About the application"), self.on_btnAbout_clicked)

    def _populate_menubar(self):
        # Create a UIManager instance
        uimanager = gtk.UIManager()

        # Add the accelerator group to the toplevel window
        accelgroup = uimanager.get_accel_group()
        self.window.add_accel_group(accelgroup)

        # Create an ActionGroup
        actiongroup = gtk.ActionGroup('UIManagerExample')
        self.actiongroup = actiongroup

        # Create actions
        actiongroup.add_actions([
            ('File', None, _("_File")),
            ('New', gtk.STOCK_NEW, _("_Add New"), '<Control>n', _("Add a new record"), self.on_btnNew_clicked),
            ('Edit', gtk.STOCK_EDIT, None, '<Control>e', _("Edit a record"), self.on_btnEdit_clicked),
            ('Delete', gtk.STOCK_DELETE, None, '<Control>d', _("Delete selected record"), self.on_btnDelete_clicked),
            ('Paid', gtk.STOCK_APPLY, _("_Paid"), '<Control>p', _("Mark as paid"), self.on_btnPaid_clicked),
            ('NotPaid', gtk.STOCK_UNDO, _("_Not Paid"), '<Control>u', _("Mark as not paid"), self.on_btnPaid_clicked),
            ('Preferences', gtk.STOCK_PREFERENCES, None, None, _("Edit preferences"), self.on_btnPref_clicked),
            ('Quit', gtk.STOCK_QUIT, None, '<Control>q', _("Quit the Program"), self.on_btnQuit_clicked),
            ('View', None, _("_View")),
            ('Help', None, _("_Help")),
            ('About', gtk.STOCK_ABOUT, None, None, _("About the application"), self.on_btnAbout_clicked),
            ])

        # Prevent crash when using old config file
        try:
            saved_view = self.config.getint('GUI', 'show_paid_bills')
        except:
            saved_view = 1
            self.config.set("GUI", "show_paid_bills", str(saved_view))
            self.config.save()

        actiongroup.add_radio_actions([
            ('PaidRecords', None, _("_Paid Only"), None, _("Display all paid records only"), 0),
            ('NotPaidRecords', None, _("_Not Paid Only"), None, _("Display all unpaid records only"), 1),
            ('AllRecords', None, _("_All Records"), None, _("Display all records"), 2),
        ], saved_view , self._change_view)

        # Add the actiongroup to the uimanager
        uimanager.insert_action_group(actiongroup, 0)

        # Add a UI description
        uimanager.add_ui_from_string(self.menu_ui)

        # Create a MenuBar
        menubar = uimanager.get_widget('/MenuBar')

        self.menuNew = uimanager.get_widget('/MenuBar/File/New')
        self.menuEdit = uimanager.get_widget('/MenuBar/File/Edit')
        self.menuRemove = uimanager.get_widget('/MenuBar/File/Delete')
        self.menuPaid = uimanager.get_widget('/MenuBar/File/Paid')
        self.menuUnpaid = uimanager.get_widget('/MenuBar/File/NotPaid')

        # Pack it
        self.box.pack_start(menubar, expand=False, fill=True, padding=0)

    def add_bill(self):
        record = dialogs.add_dialog(parent=self.window)

        # Checks if the user did not cancel the action
        if record:
            # Add new bill to database
            bill = self.actions.add_bill(record.Dictionary)
            if bill:
                self.list.add(self._formated_row(bill))
                self._update_statusbar()
                #self.bill_id = id_
                #self.refreshBillList(False)

    def edit_bill(self):
        record = dialogs.edit_dialog(parent=self.window,
                                     record=self.currentrecord)

        # Checks if the user did not cancel the action
        if record:
            try:
                # Edit bill to database
                self.actions.edit_bill(record.Dictionary)
                # Update list with updated record
                idx = self.list.get_cursor()[0][0]
                self.list.listStore[idx] = \
                                self._formated_row(record.Dictionary)
                self._update_statusbar(idx)
            except Exception, e:
                print str(e)

    def remove_bill(self):
        try:
            if self.actions.delete_bill(self.currentrecord.Id):
                self.list.remove()
                self._update_statusbar()
        except Exception, e:
            print str(e)

    def toggle_bill_paid(self):
        # Toggle paid field
        self.currentrecord.Paid = (self.currentrecord.Paid == 0) and 1 or 0

        try:
            # Edit bill to database
            self.actions.edit_bill(self.currentrecord.Dictionary)
            # Update list with updated record
            idx = self.list.get_cursor()[0][0]
            self.list.listStore[idx] = \
                            self._formated_row(self.currentrecord.Dictionary)
            self._update_statusbar(idx)
        except Exception, e:
            print str(e)

    def about(self):
        dialogs.about_dialog(parent=self.window)

    def preferences(self):
        dialogs.preferences_dialog(parent=self.window)
        self.config.reload()
        if self.iface:
            self.iface.reload_config()

    # Methods
    def _quit_application(self):
        self.save_position()
        self.save_size()
        gtk.main_quit()
        return False

    def save_position(self):
        x, y = self.window.get_position()
        self.config.set('GUI', 'x', x)
        self.config.set('GUI', 'y', y)
        self.config.save()

    def save_size(self):
        width, height = self.window.get_size()
        self.config.set('GUI', 'width', width)
        self.config.set('GUI', 'height', height)
        self.config.save()

    def toggle_buttons(self, paid=None):
        """ Toggles all buttons conform number of records present and
            their state """
        if len(self.list.listStore) > 0:
            self.btnEdit.set_sensitive(True)
            self.menuEdit.set_sensitive(True)
            self.btnRemove.set_sensitive(True)
            self.menuRemove.set_sensitive(True)
            """
            Enable/disable paid and unpiad buttons.
            If paid = True, paid button and menu will be enabled.
            """
            if paid:
                self.btnPaid.set_sensitive(False)
                self.menuPaid.set_sensitive(False)
                self.btnUnpaid.set_sensitive(True)
                self.menuUnpaid.set_sensitive(True)
            else:
                self.btnPaid.set_sensitive(True)
                self.menuPaid.set_sensitive(True)
                self.btnUnpaid.set_sensitive(False)
                self.menuUnpaid.set_sensitive(False)
        else:
            self.btnEdit.set_sensitive(False)
            self.menuEdit.set_sensitive(False)
            self.btnRemove.set_sensitive(False)
            self.menuRemove.set_sensitive(False)
            self.btnPaid.set_sensitive(False)
            self.menuPaid.set_sensitive(False)
            self.btnUnpaid.set_sensitive(False)
            self.menuUnpaid.set_sensitive(False)

    def _update_statusbar(self, index=0):
        """ This function is used to update status bar informations
            about the list """
        records = len(self.list.listStore)

        # Record count
        self.statusbar.Records(records)
        if self.currentrecord:
            # Display the status
            self.statusbar.Notes(self.currentrecord.Notes)
            # Toggles toolbar buttons on/off
            self.toggle_buttons(self.currentrecord.Paid)
        else:
            # Clear the status for the selected row
            self.statusbar.Notes("")
            # Toggles toolbar buttons on/off
            self.toggle_buttons()

    # Event handlers
    def _on_list_button_press_event(self, widget, event):
        """ This function will handle the signal to show a popup menu
            sent by a right click on tvBill widget. """
        if event.button == 3 and event.type == gtk.gdk.BUTTON_PRESS:
            self._get_selected_record()
            timeout_add(100, self._create_list_contextmenu, widget, event)

    def _create_list_contextmenu(self, widget, event):
        c = ContextMenu(self)
        c.addMenuItem(_('_Add New'),
                      self.on_btnNew_clicked, gtk.STOCK_NEW, True)
        if self.currentrecord: #len(self.list.listStore) > 0
            c.addMenuItem('-', None)
            c.addMenuItem(None,
                          self.on_btnDelete_clicked, gtk.STOCK_DELETE)
            c.addMenuItem(None,
                          self.on_btnEdit_clicked, gtk.STOCK_EDIT)
            c.addMenuItem('-', None)
            if not self.currentrecord.Paid:
                c.addMenuItem(_('_Paid'),
                          self.on_btnPaid_clicked, gtk.STOCK_APPLY, True)
            else:
                c.addMenuItem(_('Not _Paid'),
                          self.on_btnPaid_clicked, gtk.STOCK_UNDO, True)
        c.addMenuItem('-', None)
        c.addMenuItem(None, None, gtk.STOCK_CANCEL)
        c.popup(None, None, None, 3, event.get_time())


    def _on_list_cursor_changed(self, widget):
        # Get currently selected bill
        self._get_selected_record()
        # Update statusbar
        self._update_statusbar()

    def on_btnNew_clicked(self, toolbutton):
        self.add_bill()

    def on_btnEdit_clicked(self, toolbutton):
        if self.currentrecord:
            self.edit_bill()

    def on_btnDelete_clicked(self, toolbutton):
        if self.currentrecord:
            self.remove_bill()

    def on_btnPaid_clicked(self, toolbutton):
        if self.currentrecord:
            self.toggle_bill_paid()

    def on_btnAbout_clicked(self, toolbutton):
        self.about()

    def on_btnPref_clicked(self, toolbutton):
        self.preferences()

    def on_btnQuit_clicked(self, toolbutton):
        self._quit_application()

    def on_delete_event(self, widget, event, data=None):
        self._quit_application()

def main():
    gtk.main()

if __name__ == "__main__":
    billreminder = MainDialog()
    main()
