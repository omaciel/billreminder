## Process this file with automake to produce Makefile.in

billreminder_libdir = $(pythondir)/billreminder/lib
billreminder_lib_in_files = sysvars.py.in
billreminder_lib_PYTHON = \
	__init__.py \
	actions.py \
	bill.py \
	bubble.py \
	common.py \
	config.py \
	dal.py \
	dbus_actions.py \
	dialogs.py \
	i18n.py \
	scheduler.py \
	sysvars.py \
	utils.py

all: sysvars.py

sysvars.py: sysvars.py.in
	sed -e s!\@datadir\@!$(datadir)! \
		< $< > $@

EXTRA_DIST = sysvars.py.in
CLEANFILES = sysvars.py
