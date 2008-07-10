## Process this file with automake to produce Makefile.in

SUBDIRS = images

servicedir = $(DBUS_SERVICES_DIR)
service_in_files = billreminder.service.in
service_DATA = billreminder.service
EXTRA_DIST += $(service_in_files)
CLEANFILES = $(service_DATA)

%.service: %.service.in
	sed -e s!\@bindir\@!$(bindir)! \
	< $< > $@

@INTLTOOL_DESKTOP_RULE@

desktopdir = $(datadir)/applications
desktop_in_files = billreminder.desktop.in
desktop_DATA = $(desktop_in_files:.desktop.in=.desktop)
EXTRA_DIST += $(desktop_in_files)
CLEANFILES += $(desktop_DATA)

autostartdir = $(sysconfdir)/xdg/autostart
autostart_in_files = billreminderd.desktop.in
autostart_DATA = $(autostart_in_files:.desktop.in=.desktop)
EXTRA_DIST += $(autostart_in_files)
CLEANFILES += $(autostart_DATA)

schemadir = $(sysconfdir)/gconf/schemas
schema_DATA = openlh-server.schemas
EXTRA_DIST = $(schema_DATA)

