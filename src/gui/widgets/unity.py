# -*- coding: utf-8 -*-

try:
    from gi.repository import Unity, Dbusmenu
    UNITY = True
except:
    UNITY = False

class UnityIntegration:

    def __init__(self, parent):

        self.parent = parent

        self.launcher = Unity.LauncherEntry.get_for_desktop_id("billreminder.desktop")

        # This is broken
        ## Add quicklist
        #self.quicklist = Dbusmenu.Menuitem.new()
        #
        #new_bill = Dbusmenu.Menuitem.new()
        #new_bill.property_set(Dbusmenu.MENUITEM_PROP_LABEL, "Add New Bill")
        #new_bill.property_set_bool(Dbusmenu.MENUITEM_PROP_VISIBLE, True)
        #new_bill.connect("item-activated", self.on_new_bill_activate)
        #
        #self.quicklist.child_append(new_bill)
        #
        #self.launcher.set_property("quicklist", self.quicklist)

        self.parent.connect('bill-added', self.on_update_count)
        self.parent.connect('bill-updated', self.on_update_count)
        self.parent.connect('bill-removed', self.on_update_count)

        count = self.parent.actions.count_not_paid()
        self.set_count(count)

    def on_new_bill_activate(self, menuitem, arg):
        self.parent.ui.get_object("newBill").emit('activate')

    def on_update_count(self, signal, bill):
        count = self.parent.actions.count_not_paid()
        self.set_count(count)

    def set_count(self, count):
        self.launcher.set_property("count", count)
        if count:
            self.launcher.set_property("count_visible", True)
        else:
            self.launcher.set_property("count_visible", False)

    def set_urgency(self, urgency):
        self.launcher.set_property("urgency", urgency)

