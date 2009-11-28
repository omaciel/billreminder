## Process this file with automake to produce Makefile.in

SUBDIRS = images

# GConf Schemas
schemasdir = $(GCONF_SCHEMA_FILE_DIR)
schemas_in_files = billreminder.schemas.in
schemas_DATA = $(schemas_in_files:.schemas.in=.schemas)

CLEANFILES = $(schemas_DATA)

#DBus Service
servicedir = $(DBUS_SERVICES_DIR)
service_in_files = billreminder.service.in
service_DATA = $(service_in_files:.service.in=.service)

CLEANFILES += $(service_DATA)

billreminder.service: billreminder.service.in
	sed -e s!\@bindir\@!$(bindir)! \
	< $< > $@

desktopdir = $(datadir)/applications
desktop_in_files = billreminder.desktop.in
desktop_DATA = $(desktop_in_files:.desktop.in=.desktop)

CLEANFILES += $(desktop_DATA)

autostartdir = $(sysconfdir)/xdg/autostart
autostart_in_files = billreminderd.desktop.in
autostart_DATA = $(autostart_in_files:.desktop.in=.desktop)
CLEANFILES += $(autostart_DATA)

# Build rules
@INTLTOOL_DESKTOP_RULE@
@INTLTOOL_SCHEMAS_RULE@


if GCONF_SCHEMAS_INSTALL
		for p in $(schemas_DATA) ; do \
			GCONF_CONFIG_SOURCE=$(GCONF_SCHEMA_CONFIG_SOURCE) $(GCONFTOOL) --makefile-install-rule $$p ; \
		done
else
	for p in $(schemas_DATA) ; do \
		GCONF_CONFIG_SOURCE=$(GCONF_SCHEMA_CONFIG_SOURCE) $(GCONFTOOL) --makefile-uninstall-rule $$p ; \
	done
endif

resources_DATA = \
	main.ui

EXTRA_DIST = \
	$(schemas_in_files) \
	$(service_in_files) \
	$(desktop_in_files) \
	$(autostart_in_files) \
        $(resources_DATA)
