# -*- coding: utf-8 -*-

__all__ = ['MainDialog']

import os

import pygtk
pygtk.require('2.0')
import gtk
import time
import datetime
from gobject import timeout_add

# Import widgets modules
from gui.widgets.statusbar import Statusbar
from gui.widgets.viewbill import ViewBill as ViewBill
from gui.widgets.trayicon import NotifyIcon
from gui.widgets.chartwidget import ChartWidget
from gui.widgets.timeline import Timeline, Bullet

# Import data model modules
from lib.bill import Bill
from lib.actions import Actions

# Import common utilities
from lib import common
from lib import dialogs
from lib import scheduler
#from lib.config import Configuration
from lib.Settings import Settings as Configuration
from lib.utils import Message
from lib.utils import get_dbus_interface
from lib.utils import force_string
from lib.utils import create_pixbuf
from lib.utils import float_to_currency
from lib import i18n

from lib.common import GCONF_PATH, GCONF_GUI_PATH, GCONF_ALARM_PATH
from lib.common import CFG_NAME
from lib.common import USER_CFG_PATH, DEFAULT_CFG_PATH
from os.path import exists, join

class MainDialog:
    search_text = ""
    _bullet_cache = {}

    def __init__(self):
        if exists(join(USER_CFG_PATH, CFG_NAME)):
            from lib.migrate_to_gconf import migrate
            migrate(join(USER_CFG_PATH, CFG_NAME))

        self.gconf_client = Configuration()
        self.message = Message()
        # Connects to the database
        self.actions = Actions()


        self.ui = gtk.Builder()
        self.ui.add_from_file(os.path.join(DEFAULT_CFG_PATH, "main.ui"))

        self.window = self.ui.get_object("main_window")
        self.window.set_title("%s" % common.APPNAME)
        self.window.set_icon_from_file(common.APP_ICON)

        # ViewBill
        self.list = ViewBill()
        self.list.connect('cursor_changed', self._on_list_cursor_changed)
        self.list.connect('row_activated', self._on_list_row_activated)
        self.list.connect('button_press_event', self._on_list_button_press_event)

        self.ui.get_object("bill_box").add(self.list)

        # Toolbar
        self.toolbar = self.ui.get_object("toolbar")

        # Menubar
        self._populate_menubar()

        # Statusbar
        self.statusbar = Statusbar()
        self.ui.get_object("statusbar_box").add(self.statusbar)

        # Timeline
        self.timeline = Timeline(callback=self.on_timeline_cb)
        self.timeline.connect("value-changed", self._on_timeline_changed)
        self.ui.get_object("timeline_box").add(self.timeline)

        # Chart
        self.chart = ChartWidget()
        self.chart.set_border_width(10)
        self.ui.get_object("chart_box").add(self.chart)

        # Restore position and size of window
        width = self.gconf_client.get('window_width')
        height = self.gconf_client.get('window_height')
        x = self.gconf_client.get('window_position_x')
        y = self.gconf_client.get('window_position_y')
        if width and height:
            self.window.resize(width, height)
        if x and y:
            self.window.move(x, y)

        self.window.show_all()

        # Whether to display toolbar or not
        self.on_showToolbar_toggled(self.ui.get_object("showToolbar"))
        self.list.grab_focus()

        if self.gconf_client.get('start_in_tray'):
            self.window.hide()

        self.toggle_buttons()

        # Connects to the Daemon
        self.iface = None
        iface = get_dbus_interface(common.DBUS_INTERFACE, common.DBUS_PATH)
        if iface:
            iface.connect_to_signal("bill_edited", self.reloadTreeView)
            iface.connect_to_signal("bill_edited", self.reloadTimeline)
            iface.connect_to_signal("show_main_window", self.window.show)
            self.iface = iface
            timeout_add(2000, self._send_tray_hints)

        self.set_action_strings()
        self.ui.connect_signals(self)

        # populate treeview
        self.reloadTreeView()
        self.notify = NotifyIcon(self)

    def set_action_strings(self):
        # for some reason the actions strings do not get translated yet
        # so we define them here so they would be picked up by the pyfile scanner
        self.ui.get_object("newBill").set_label(_("_New"))
        self.ui.get_object("newBill").set_tooltip(_("Add new bill"))

        self.ui.get_object("editBill").set_label(_("_Edit"))
        self.ui.get_object("editBill").set_tooltip(_("Edit a bill"))

        self.ui.get_object("removeBill").set_label(_("_Delete"))
        self.ui.get_object("removeBill").set_tooltip(_("Delete selected bill"))

        self.ui.get_object("markPaid").set_label(_("P_aid"))
        self.ui.get_object("markPaid").set_tooltip(_("Mark as paid"))

        self.ui.get_object("markNotPaid").set_label(_("No_t Paid"))
        self.ui.get_object("markNotPaid").set_tooltip(_("Mark as not paid"))

        self.ui.get_object("showToolbar").set_label(_("_Show Toolbar"))
        self.ui.get_object("showToolbar").set_tooltip(_("Show the toolbar"))

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

    def get_selected_record(self):
        """ Returns a bill object from the current selected record """
        if len(self.list.listStore) > 0:
            model_ = self.list.get_model()
            if self.list.get_cursor()[0]:
                index = self.list.get_cursor()[0][0]
            else:
                index = 0

            b_id = model_[index][0]

            records = self.actions.get_bills(id=b_id)
            self.currentrecord = records[0]

        else:
            self.currentrecord = None
        print "Current record is: %s" % self.currentrecord

    def populate_view(self, records):
        """ Populates the treeview control with the records passed """

        # Reset list
        self.list.listStore.clear()

        if not records:
            return 0

        # Loops through bills collection
        path = 0
        for rec in records:
            # Format the record prior to adding it to treeview
            row = self.format_row(rec)
            self.list.add(row)

        # Set the cursor to the first (top) record
        self.list.set_cursor(path)

        # Returns how many records there are in the treeview
        return len(records)

    def reloadTreeView(self, *arg):
        # Update list with updated record
        status = self.gconf_client.get('show_paid_bills')

        path = self.list.get_cursor()[0]
        self.list.listStore.clear()
        self.currentrecord = None

        first = self.timeline.start_date
        last = self.timeline.end_date
        # Get list of records
        records = self.actions.get_interval_bills(first, last, status)

        # Populate treeview
        self.populate_view(records)
        # Update status bar
        self.update_statusbar()
        # populate chart
        self._populate_chart(status, first, last)

        return len(records)

    def format_row(self, row):
        """ Formats a bill to be displayed as a row. """

        categoryName = row.category.name if row.category else _('None')
        categoryColor = row.category.color if row.category else '#d3d7cf'
        formatted = [
            row.id,
            create_pixbuf(color=categoryColor),
            categoryName,
            row.payee,
            row.dueDate.strftime(_('%m/%d').encode('ASCII')),
            row.amount,
            row.notes,
            int(row.paid),
            None
        ]

        return formatted


    def _populate_chart(self, status, start, end):

        records = []
        categories = []
        totals = []

        records = self.actions.get_monthly_totals(start, end, status)
        # Chart widget takes data in format (('CategoryName', amount),)
        categories = [cat or 'None' for cat, total in records]
        totals = [float(total) for cat,total in records]
        #records = [(c if c else 'None',float(t)) for c,t in records]

        # set bar colors
        all_categories = self.actions.get_categories()
        self.chart.chart.key_colors = dict([(cat.name or 'None', cat.color) for cat in all_categories])

        self.chart.plot(categories, totals)

    def _populate_menubar(self):
        try:
            saved_view = self.gconf_client.get('show_paid_bills')
        except:
            saved_view = 1
            self.gconf_client.set("show_paid_bills", saved_view)

        if saved_view == 0:
            self.ui.get_object("showNotPaid").set_active(True)
        elif saved_view == 1:
            self.ui.get_object("showPaid").set_active(True)
        else:
            self.ui.get_object("showAll").set_active(True)

        # Check whether we display the toolbar or not
        self.ui.get_object("showToolbar").set_active(self.gconf_client.get('show_toolbar'))


    def add_bill(self):
        selectedDate = self.timeline.value
        records = dialogs.add_dialog(parent=self.window, selectedDate=selectedDate)

        # Checks if the user did not cancel the action
        if records:
            # Add new bill to database
            for rec in records:
                bill = self.actions.add(rec)
                if bill:
                    self.list.add(self.format_row(bill))
            self.update_statusbar()
            # Reload records tree (something changed)
            self.reloadTreeView()
            self.reloadTimeline()

    def edit_bill(self):
        records = dialogs.edit_dialog(parent=self.window, record=self.currentrecord)

        # Checks if the user did not cancel the action
        if records:
            for rec in records:
                # Edit bill to database
                rec = self.actions.edit(rec)

            # Reload records tree (something changed)
            self.reloadTreeView()
            self.reloadTimeline()

    def remove_bill(self):
        self.actions.delete(self.currentrecord)
        self.list.remove()
        self.update_statusbar()
        self.reloadTreeView()
        self.reloadTimeline()

    def toggle_bill_paid(self):
        # Fetch record from database
        record = self.actions.get_bills(id=self.currentrecord.id)[0]
        # Toggle paid field
        record.paid = False if record.paid else True

        # Edit bill in the database
        transaction = self.actions.add(record)

        # Update our current copy
        self.currentrecord = self.actions.get_bills(id = self.currentrecord.id)[0]
        # Update timeline widget to reflect change
        self._bullet_cache[self.currentrecord.dueDate] = [self.currentrecord]
        # Update list with updated record
        idx = self.list.get_cursor()[0][0]
        self.update_statusbar(idx)
        self.reloadTreeView()
        self.reloadTimeline()

    def about(self):
        dialogs.about_dialog(parent=self.window)

    def preferences(self):
        dialogs.preferences_dialog(parent=self.window)

    # Methods
    def _quit_application(self):
        self.save_position()
        self.save_size()
        gtk.main_quit()
        return False

    def save_position(self):
        x, y = self.window.get_position()
        self.gconf_client.set('window_position_x', x)
        self.gconf_client.set('window_position_y', y)

    def save_size(self):
        width, height = self.window.get_size()
        self.gconf_client.set('window_width', width)
        self.gconf_client.set('window_height', height)

    def toggle_buttons(self, paid=None):
        """ Toggles all buttons conform number of records present and
            their state """

        for widget in ["editBill", "removeBill", "markPaid", "markNotPaid"]:
            self.ui.get_object(widget).set_sensitive(len(self.list.listStore) > 0)


        if len(self.list.listStore) > 0:
            self.ui.get_object("markPaid").set_sensitive(paid == False)
            self.ui.get_object("markNotPaid").set_sensitive(paid == True)

    def update_statusbar(self, index=0):
        """ This function is used to update status bar informations
            about the list """
        records = len(self.list.listStore)

        # Record count
        self.statusbar.Records(records)
        if self.currentrecord:
            # Display the status
            self.statusbar.Notes(self.currentrecord.notes)
            # Toggles toolbar buttons on/off
            self.toggle_buttons(self.currentrecord.paid)
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
            self.get_selected_record()

            c = self.ui.get_object("context_menu")
            c.popup(None, None, None, event.button, event.get_time())


    def _on_list_row_activated(self, widget, path, column):
        self._on_list_cursor_changed(widget)
        self.on_editBill_activate(None)

    def _on_list_cursor_changed(self, widget):
        # Get currently selected bill
        self.get_selected_record()
        # Update statusbar
        self.update_statusbar()

    def on_newBill_activate(self, toolbutton):
        self.add_bill()

    def on_editBill_activate(self, toolbutton):
        if self.currentrecord:
            self.edit_bill()

    def on_removeBill_activate(self, toolbutton):
        if self.currentrecord:
            resp = self.message.ShowQuestionYesNo(
                _("Do you really want to delete \"%s\"?") % \
                self.currentrecord.payee,
                self.window, _("Confirmation"))
            if resp:
                self.remove_bill()

    def on_markNotPaid_activate(self, toolbutton):
        self.on_markPaid_activate(toolbutton) # forward

    def on_markPaid_activate(self, toolbutton):
        if self.currentrecord:
            self.toggle_bill_paid()

    def on_btnAbout_activate(self, toolbutton):
        self.about()

    def on_btnPrefs_activate(self, toolbutton):
        self.preferences()

    def on_btnQuit_activate(self, toolbutton):
        self._quit_application()

    def on_delete_event(self, widget, event, data=None):
        self._quit_application()

    def _on_timeline_changed(self, widget, args):
        self.reloadTreeView()


    def switch_view(self, view_number):
        self.gconf_client.set('show_paid_bills', view_number)
        self.reloadTreeView()
        self.reloadTimeline()

    def on_showNotPaid_toggled(self, action):
        if action.get_active():
            self.switch_view(0)

    def on_showPaid_toggled(self, action):
        if action.get_active():
            self.switch_view(1)

    def on_showAll_toggled(self, action):
        if action.get_active():
            self.switch_view(2)

    def on_showToolbar_toggled(self, action):
        # Toggle toolbar's visibility
        if action.get_active():
            self.toolbar.show_all()
        else:
            self.toolbar.hide_all()

        self.gconf_client.set("show_toolbar", action.get_active())

    def reloadTimeline(self, *args):
        self._bullet_cache = {}
        self.timeline.refresh()

    def on_timeline_cb(self, date, display_type):
        # TODO: Improve tooltip
        # TODO: Improve cache

        if not date in self._bullet_cache.keys():
            self._bullet_cache[date] = self.actions.get_bills(dueDate=date)

        if self._bullet_cache[date]:
            status = self.gconf_client.get('show_paid_bills')
            amount = 0
            tooltip = ''
            bullet = Bullet()
            bullet.date = date

            for bill in self._bullet_cache[date]:
                amount += bill.amount
                if tooltip:
                    tooltip += '\n'
                tooltip += bill.payee + '\n' + str(float_to_currency(bill.amount))
                if bill.notes:
                    tooltip += '\n' + bill.notes

                if bill.paid:
                    if status == 0: return False
                    bullet.status = bullet.status | bullet.PAID
                elif date <= datetime.date.today():
                    if status == 1: return False
                    bullet.status = bullet.status | bullet.OVERDUE
                else:
                    if status == 1: return False
                    bullet.status = bullet.status | bullet.TO_BE_PAID

            bullet.amountDue = amount

            if len(self._bullet_cache[date]) > 1:
                bullet.multi = True
            bullet.tooltip = tooltip
            return bullet

        return None

def main():
    gtk.main()

if __name__ == "__main__":
    billreminder = MainDialog()
    main()
