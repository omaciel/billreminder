## Process this file with automake to produce Makefile.in

billreminder_libdir = $(pythondir)/billreminder/lib
billreminder_lib_PYTHON = \
	__init__.py \
	actions.py \
	bill.py \
	bubble.py \
	common.py \
	config.py \
	dal.py \
	dbus_actions.py \
	defs.py \
	dialogs.py \
	i18n.py \
	migrate_to_gconf.py \
	scheduler.py \
	utils.py

defs.py: defs.py.in
	sed -e s!\@VERSION\@!$(VERSION)! \
	< $< > $@

CLEANFILES = \
	defs.py
	
DISTCLEANFILES = \
	$(CLEANFILES)
	
EXTRA_DIST = \
	defs.py.in
