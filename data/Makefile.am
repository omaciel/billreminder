## Process this file with automake to produce Makefile.in

SUBDIRS = images

configdir = $(datadir)/billreminder
config_DATA = billreminder.cfg
EXTRA_DIST = $(config_DATA)

schema_in_files = billreminder.schemas.in
@INTLTOOL_SCHEMAS_RULE@

if GCONF_SCHEMAS_INSTALL
schemadir = $(GCONF_SCHEMA_FILE_DIR)
schema_DATA = $(schema_in_files:.schemas.in=.schemas)
EXTRA_DIST += $(schemas_DATA)
endif

servicedir = $(DBUS_SERVICES_DIR)
service_in_files = billreminder.service.in
service_DATA = billreminder.service
EXTRA_DIST += $(service_in_files)
CLEANFILES = $(service_DATA)

billreminder.service: billreminder.service.in
	sed -e s!\@bindir\@!$(bindir)! \
	< $< > $@

desktopdir = $(datadir)/applications
desktop_in_files = billreminder.desktop.in
desktop_DATA = $(desktop_in_files:.desktop.in=.desktop)
@INTLTOOL_DESKTOP_RULE@

EXTRA_DIST += $(desktop_in_files)
CLEANFILES += $(desktop_DATA)

autostartdir = $(sysconfdir)/xdg/autostart
autostart_in_files = billreminderd.desktop.in
autostart_DATA = $(autostart_in_files:.desktop.in=.desktop)
EXTRA_DIST += $(autostart_in_files)
CLEANFILES += $(autostart_DATA)

if GCONF_SCHEMAS_INSTALL
install-data-local:
	@GCONF_CONFIG_SOURCE=$(GCONF_SCHEMA_CONFIG_SOURCE) $(GCONFTOOL) \
		--makefile-install-rule $(schema_DATA) || \
		(echo ;\
		echo "*****************************************************"; \
		echo "Installation of schemas failed, install them manually"; \
		echo "*****************************************************";)
	@true
else
install-data-local:
	@echo "***************************************************************"
	@echo "Not installing schemas, disabled with --disable-schemas-install"
	@echo "***************************************************************"
	@true
endif

uninstall-hook:
	rm -fr $(configdir)
