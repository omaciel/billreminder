"""
Stores application settings

Part of this code copied from Gimmie (c) Alex Gravely

Copyright: John Stowers, 2006
License: GPLv2
"""
import gobject

#these dicts are used for mapping config setting types to type names
#and back again (isnt python cool...)
TYPE_TO_TYPE_NAME = {
    int     :   "int",
    bool    :   "bool",
    str     :   "string",
    list    :   "list"
}
STRING_TO_TYPE = {
    "int"       :   lambda x: int(x),
    "bool"      :   lambda x: string_to_bool(x),
    "string"    :   lambda x: str(x),
    "list"      :   lambda x: string_to_list(x)
}
TYPE_TO_STRING = {
    int     :   lambda x: str(x),
    bool    :   lambda x: str(x),
    str     :   lambda x: str(x),
    list    :   lambda x: list_to_string(x)
}

def string_to_bool(stringy):
    #Because bool("False") doesnt work as expected when restoring strings
    if stringy == "True":
        return True
    else:
        return False
    
def list_to_string(listy):
    s = ""
    if type(listy) is list:
        s = ",".join(listy) #cool
    return s
    
def string_to_list(string, listInternalVtype=str):
    l = string.split(",")
    internalTypeName = TYPE_TO_TYPE_NAME[listInternalVtype]
    for i in range(0, len(l)):
        l[i] = STRING_TO_TYPE[internalTypeName](l[i])
    return l

class Settings(gobject.GObject):
    """
    Class for storing conduit.GLOBALS.settings. Keys of type str, bool, int, 
    and list of strings supported at this stage.
    
    Also stores the special proxy settings.
    """
    __gsignals__ = {
        'changed' : (gobject.SIGNAL_RUN_LAST | gobject.SIGNAL_DETAILED, gobject.TYPE_NONE, ()),
    }

    #Default values for conduit settings
    DEFAULTS = {
        'startup_delay'             :   1,              #How long to wait before starting the backend
        'start_in_tray'             :   False,          #Show the application start minimized
        'show_startup_notification' :   True,
        'show_pay_notification',    :   True,
        'show_before_alarm'         :   True,
        'show_due_alarm'            :   True,
        'show_alarm'                :   True,
        'notification_days_limit'   :   15,
        'use_alert_dialog'          :   False,
        'show_alarm_before_days'    :   3,
        'show_alarm_at_time'        :   '13:00',
        'interval'                  :   60,
        'window_position_x'         :   0,
        'window_position_y'         :   0,
        'window_width'              :   550,
        'window_height'             :   300,
        'show_toolbar'              :   False,
        'show_menubar'              :   False,
        'show_paid_bills'           :   2,
        'due_date'                  :   0,
    }

    def __init__(self, **kwargs):
        gobject.GObject.__init__(self)

        #you can override the settings implementation at runtime
        #for testing purposes only
        try:
            from lib.defs import SETTINGS_IMPL
        except Exception, e:
            SETTINGS_IMPL = 'GConf'

        implName = kwargs.get("implName", conduit.SETTINGS_IMPL)
        if implName == "GConf":
            import SettingsGConf as SettingsImpl
        else:
            raise Exception("Settings Implementation %s Not Supported" % implName)

        self._settings = SettingsImpl.SettingsImpl(
            defaults=self.DEFAULTS, changedCb=self._key_changed)

    def _key_changed(self, key):
        self.emit('changed::%s' % key)

    def set_overrides(self, **overrides):
        """
        Sets values of settings that only exist for this setting, and are
        never saved, nor updated.
        """
        self._settings.set_overrides(**overrides)

    def get(self, key, **kwargs):
        """
        Returns the value of the key or the default value if the key is 
        not yet stored
        """
        return self._settings.get(key, **kwargs)

    def set(self, key, value, **kwargs):
        """
        Sets the key to value.
        """
        return self._settings.set(key, value, **kwargs)

    def save(self):
        """
        Performs any necessary tasks to ensure settings are saved between sessions
        """
        self._settings.save()


