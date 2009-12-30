import re
import os

try:
    import gconf
except ImportError:
    from gnome import gconf

import conduit.platform

import logging
log = logging.getLogger("Settings")
    
class SettingsImpl(conduit.platform.Settings):
    """
    Settings implementation which stores settings in GConf
    """
    
    CONDUIT_GCONF_DIR = "/apps/conduit/"
    VALID_KEY_TYPES = (bool, str, int, list, tuple)
    
    def __init__(self, defaults, changedCb):
        conduit.platform.Settings.__init__(self, defaults, changedCb)

        self._client = gconf.client_get_default()
        self._client.add_dir(self.CONDUIT_GCONF_DIR[:-1], gconf.CLIENT_PRELOAD_RECURSIVE)  
        self._notifications = []

    def _fix_key(self, key):
        """
        Appends the CONDUIT_GCONF_PREFIX to the key if needed
        
        @param key: The key to check
        @type key: C{string}
        @returns: The fixed key
        @rtype: C{string}
        """
        if not key.startswith(self.CONDUIT_GCONF_DIR):
            return self.CONDUIT_GCONF_DIR + key
        else:
            return key
            
    def _key_changed(self, client, cnxn_id, entry, data=None):
        """
        Callback when a gconf key changes
        """
        key = self._fix_key(entry.key)
        self._changedCb(key)
        
    def get(self, key, default=None):
        """
        Returns the value of the key or the default value if the key is 
        not yet in gconf
        """
        #check if the setting has been overridden for this session
        if key in self._overrides:
            try:
                #try and cast to correct type
                return type(self._defaults[key])(self._overrides[key])
            except:
                return self._overrides[key]

        #function arguments override defaults
        if default == None:
            default = self._defaults.get(key, None)
        vtype = type(default)

        #we now have a valid key and type
        if default == None:
            log.warn("Unknown key: %s, must specify default value" % key)
            return None

        if vtype not in self.VALID_KEY_TYPES:
            log.warn("Invalid key type: %s" % vtype)
            return None

        #for gconf refer to the full key path
        key = self._fix_key(key)

        if key not in self._notifications:
            self._client.notify_add(key, self._key_changed)
            self._notifications.append(key)
        
        value = self._client.get(key)
        if not value:
            self.set(key, default)
            return default

        if vtype is bool:
            return value.get_bool()
        elif vtype is str:
            return value.get_string()
        elif vtype is int:
            return value.get_int()
        elif vtype in (list, tuple):
            l = []
            for i in value.get_list():
                l.append(i.get_string())
            return l
            
        log.warn("Unknown gconf key: %s" % key)
        return None

    def set(self, key, value):
        """
        Sets the key value in gconf and connects adds a signal 
        which is fired if the key changes
        """
        #overidden settings only apply for this session, and are
        #not set
        if key in self._overrides:
            return True

        log.debug("Settings %s -> %s" % (key, value))
        if key in self._defaults:
            vtype = type(self._defaults[key])
        else:
            vtype = type(value)

        if vtype not in self.VALID_KEY_TYPES:
            log.warn("Invalid key type: %s" % vtype)
            return False

        #for gconf refer to the full key path
        key = self._fix_key(key)

        if vtype is bool:
            self._client.set_bool(key, value)
        elif vtype is str:
            self._client.set_string(key, value)
        elif vtype is int:
            self._client.set_int(key, value)
        elif vtype in (list, tuple):
            #Save every value as a string
            strvalues = [str(i) for i in value]
            self._client.set_list(key, gconf.VALUE_STRING, strvalues)

        return True
        
    def proxy_enabled(self):
        """
        @returns: True if the user has specified a http proxy via
        the http_proxy environment variable, or in gconf
        """
        return os.environ.has_key("http_proxy") or \
                self._client.get_bool("/system/http_proxy/use_http_proxy")
        
    def get_proxy(self):
        """
        Returns the details of the configured http proxy. 
        The http_proxy environment variable overrides the GNOME setting
        @returns: host,port,user,password
        """
        if self.proxy_enabled():
            #env vars have preference
            if os.environ.has_key("http_proxy"):
                #re taken from python boto
                pattern = re.compile(
                    '(?:http://)?' \
                    '(?:(?P<user>\w+):(?P<pass>.*)@)?' \
                    '(?P<host>[\w\-\.]+)' \
                    '(?::(?P<port>\d+))?'
                )
                match = pattern.match(os.environ['http_proxy'])
                if match:
                    return (match.group('host'),
                            int(match.group('port')),
                            match.group('user'),
                            match.group('pass'))
            #now try gconf
            if self._client.get_bool("/system/http_proxy/use_authentication"):
                return (self._client.get_string("/system/http_proxy/host"),
                        self._client.get_int("/system/http_proxy/port"),
                        self._client.get_string("/system/http_proxy/authentication_user"),
                        self._client.get_string("/system/http_proxy/authentication_password"))
            else:
                return (self._client.get_string("/system/http_proxy/host"),
                        self._client.get_int("/system/http_proxy/port"),
                        "",
                        "")

        return ("",0,"","")



