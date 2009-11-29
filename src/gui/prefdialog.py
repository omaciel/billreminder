# -*- coding: utf-8 -*-

__all__ = ['PrefDialog']

import pygtk
pygtk.require('2.0')
import gtk
import gconf
import time
import datetime
import locale
import gobject
from subprocess import Popen

from lib import common
from lib import utils
from lib import i18n
from widgets.timewidget import TimeWidget
from lib.common import GCONF_PATH, GCONF_GUI_PATH, GCONF_ALARM_PATH

class PrefDialog(gtk.Dialog):
    """
    Class used to generate dialog to allow user to edit preferences.
    """
    def __init__(self, parent=None):
        title = _("Preferences")
        gtk.Dialog.__init__(self, title=title, parent=parent,
            flags=gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT |gtk.DIALOG_NO_SEPARATOR,
            buttons=(gtk.STOCK_CLOSE, gtk.RESPONSE_ACCEPT))

        self.set_position(gtk.WIN_POS_CENTER)
        self.set_border_width(6)
        self.set_resizable(False)
        self.set_icon_from_file(common.APP_ICON)

        self.props.skip_taskbar_hint = True

        self.gconf_client = gconf.client_get_default()

        self._initialize_dialog_widgets()
        self._populate_fields()
        self._connect_fields()
        self.connect("response", lambda self, *args: self.destroy())


    def _initialize_dialog_widgets(self):
        self.topcontainer = gtk.VBox(homogeneous=False, spacing=18)
        self.topcontainer.set_border_width(6)

        # Alert Group
        alertFrame = gtk.VBox(homogeneous=False, spacing=6)
        alertAlignment = gtk.Alignment()
        alertAlignment.set_padding(0, 0, 12, 0)
        title = gtk.Label()
        title.set_markup(_("<b>Alarms</b>"))
        title.set_alignment(0.00, 0.50)
        alertFrame.pack_start(title)
        alertFrame.pack_start(alertAlignment)

        alertContainer = gtk.VBox(homogeneous=False, spacing=6)
        self.alertCheckbox = gtk.CheckButton(_('_Alert before due date:'), use_underline=True)
        self.alertSpinButton = gtk.SpinButton()
        self.alertSpinButton.set_range(0, 360)
        self.alertSpinButton.spin(gtk.SPIN_STEP_FORWARD)
        self.alertSpinButton.set_increments(1, 7)
        alertDays = gtk.Label("%s" % _('day(s).'))
        self.notificationTime = TimeWidget()
        alertPreferredTime = gtk.Label()
        alertPreferredTime.set_markup_with_mnemonic(_('_Preferred time:'))
        alertPreferredTime.set_mnemonic_widget(self.notificationTime.hourSpinner)
        alertPreferredTime.set_alignment(0.00, 0.50)
        alertDefinition = gtk.Label(_('Get alerted when individual bills are due.'))
        alertDefinition.set_alignment(0.00, 0.90)

        # Add label defining what an alarm means.
        alertContainer.pack_start(alertDefinition, expand=False, fill=True, padding=0)

        # Container for alert checkbox and spin button for day selection.
        hbox = gtk.HBox(homogeneous=False, spacing=4)
        hbox.pack_start(self.alertCheckbox, expand=False, fill=True, padding=0)
        hbox.pack_start(self.alertSpinButton, expand=False, fill=False, padding=0)
        hbox.pack_start(alertDays, expand=False, fill=False, padding=0)
        alertContainer.pack_start(hbox, expand=False, fill=True, padding=0)

        # Container for preferred time for alerts.
        hbox = gtk.HBox(homogeneous=False, spacing=12)
        hbox.pack_start(alertPreferredTime, expand=False, fill=True, padding=0)
        hbox.pack_start(self.notificationTime, expand=True, fill=True, padding=0)
        alertContainer.pack_start(hbox, expand=False, fill=True, padding=0)

        alertAlignment.add(alertContainer)

        # Notification Group
        notifyFrame = gtk.VBox(homogeneous=False, spacing=6)
        title = gtk.Label()
        title.set_markup(_("<b>Notifications</b>"))
        title.set_alignment(0.00, 0.50)
        notifyAlignment = gtk.Alignment()
        notifyAlignment.set_padding(0, 0, 12, 0)
        notifyFrame.pack_start(title)
        notifyFrame.pack_start(notifyAlignment)
        notificationDefinition = gtk.Label(_('Define when to be notified of upcoming bills.'))
        notificationDefinition.set_alignment(0.00, 0.90)

        notificationsContainer = gtk.VBox(homogeneous=False, spacing=6)

        # Add label defining what a definition means.
        notificationsContainer.pack_start(notificationDefinition, expand=False, fill=False, padding=0)

        self.notifyCheckbox = gtk.CheckButton(_('_Notify before due date:'),
                                              use_underline=True)
        self.notifySpinButton = gtk.SpinButton()
        self.notifySpinButton.set_range(0, 360)
        self.notifySpinButton.spin(gtk.SPIN_STEP_FORWARD)
        self.notifySpinButton.set_increments(1, 7)
        notifyDays = gtk.Label("%s" % _('day(s).'))

        # Container for notification checkbox and spin button for day selection.
        hbox = gtk.HBox(homogeneous=False, spacing=4)
        hbox.pack_start(self.notifyCheckbox, expand=False, fill=True, padding=0)
        hbox.pack_start(self.notifySpinButton, expand=False, fill=False, padding=0)
        hbox.pack_start(notifyDays, expand=False, fill=False, padding=0)

        notificationsContainer.pack_start(hbox, expand=False, fill=True, padding=0)

        notifyAlignment.add(notificationsContainer)

        # Alert Type Group
        alertTypeFrame = gtk.VBox(homogeneous=False, spacing=6)
        title = gtk.Label()
        title.set_markup(_("<b>Alert Type</b>"))
        title.set_alignment(0.00, 0.50)
        alertTypeAlignment = gtk.Alignment()
        alertTypeAlignment.set_padding(0, 0, 12, 0)
        alertTypeFrame.pack_start(title)
        alertTypeFrame.pack_start(alertTypeAlignment)

        vbox = gtk.VBox(homogeneous=False, spacing=6)

        hbox = gtk.HBox(homogeneous=False, spacing=12)
        self.alertBubble = gtk.RadioButton(label=_("Notification _Bubble"))
        self.alertDialog = gtk.RadioButton(group=self.alertBubble,
            label=_("Alert _Dialog"))

        hbox.pack_start(self.alertBubble, expand=False, fill=False, padding=0)
        hbox.pack_start(self.alertDialog, expand=False, fill=False, padding=0)

        vbox.pack_start(hbox, expand=False, fill=False, padding=0)

        alertTypeAlignment.add(vbox)

        # Daemon Warning
        daemonContainer = gtk.VBox(homogeneous=False, spacing=6)
        self.daemonLabel = gtk.Label(
            _("<b>Warning:</b> BillReminder Notifier is \n" \
            "not running! You need to start it in order \n" \
            " to receive notifications."))
        self.daemonLabel.set_justify(gtk.JUSTIFY_CENTER)
        self.daemonLabel.set_use_markup(True)
        daemonImage = gtk.Image()
        daemonImage.set_from_stock('gtk-execute', 2)
        self.daemonButton = gtk.Button(label=_("_Start BillReminder Notifier"))
        self.daemonButton.set_relief(gtk.RELIEF_NONE)
        self.daemonButton.set_image(daemonImage)

        daemonContainer.pack_start(self.daemonLabel, expand=False, fill=True, padding=0)
        daemonContainer.pack_start(self.daemonButton, expand=False, fill=True, padding=0)

        # Everything
        self.topcontainer.pack_start(alertFrame, expand=False, fill=True, padding=0)
        self.topcontainer.pack_start(notifyFrame, expand=False, fill=True, padding=0)
        self.topcontainer.pack_start(alertTypeFrame, expand=False, fill=True, padding=0)

        if not utils.verify_dbus_service(common.DBUS_INTERFACE):
            self.topcontainer.pack_start(daemonContainer, expand=False, fill=True, padding=0)

        self.vbox.pack_start(self.topcontainer, expand=False, fill=True)

        self.show_all()

    def _populate_fields(self):

        self.notifyCheckbox.set_active( \
            self.gconf_client.get_bool(GCONF_ALARM_PATH + 'show_before_alarm'))
        self.alertCheckbox.set_active( \
            self.gconf_client.get_bool(GCONF_ALARM_PATH + 'show_alarm'))

        if not self.gconf_client.get_bool(GCONF_ALARM_PATH + 'use_alert_dialog'):
            self.alertBubble.set_active(True)
        else:
            self.alertDialog.set_active(True)

        # Number of days before showing alarm
        adays = self.gconf_client.get_int(GCONF_ALARM_PATH + 'notification_days_limit')
        self.notifySpinButton.set_value(adays and adays or 3)
        self.alertSpinButton.set_value(self.gconf_client.get_int(GCONF_ALARM_PATH + 'show_alarm_before_days'))

        atime = self.gconf_client.get_string(GCONF_ALARM_PATH + 'show_alarm_at_time')
        # Don't crash if running uninstalled and no gconf data
        atime = atime and atime.split(":") or ['13', '00']

        self.notificationTime.setHourMinute(atime[0], atime[1])


    def _connect_fields(self):
        self.notificationTime.hourSpinner.connect("value_changed", self._on_time_changed)
        self.notificationTime.minuteSpinner.connect("value_changed", self._on_time_changed)
        self.notifyCheckbox.connect("toggled",
            self._on_checkbox_toggled, 'show_before_alarm')
        self.alertCheckbox.connect("toggled",
            self._on_checkbox_toggled, 'show_alarm')
        self.notifySpinButton.connect("changed",
            self._on_spin_changed, 'notification_days_limit')
        self.alertSpinButton.connect("changed",
            self._on_spin_changed, 'show_alarm_before_days')
        self.alertDialog.connect("toggled",
            self._on_checkbox_toggled, 'use_alert_dialog')
        self.daemonButton.connect("clicked", self._launch_daemon)

    def _on_time_changed(self, spin):
        alarm = self.notificationTime.getTime()
        alarm = ":".join(["%.02d" % x for x in alarm])
        self.gconf_client.set_string(GCONF_ALARM_PATH + 'show_alarm_at_time', alarm)

    def _on_checkbox_toggled(self, togglebutton, item):
        self.gconf_client.set_bool(GCONF_ALARM_PATH + item, togglebutton.get_active())

    def _on_spin_changed(self, obj, item):
        self.gconf_client.set_int(GCONF_ALARM_PATH + item, int(obj.get_value()))

    def _launch_daemon(self, button):
        Popen('billreminderd', shell=True)
        button.hide()
        self.daemonLabel.set_markup( _("<b>Note:</b> BillReminder Notifier is now running."))
