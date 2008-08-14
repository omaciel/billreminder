## Process this file with automake to produce Makefile.in

SUBDIRS = data man po src

bin_SCRIPTS = \
	billreminder \
	billreminderd

CLEANFILES = \
	src/*/*.pyc \
	src/*/*.pyo

billreminder: billreminder.in
	-sed -e s!\@PYTHONDIR\@!$(pythondir)! \
		< $< > $@

EXTRA_DIST = billreminder.in
CLEANFILES += billreminderd

billreminderd: billreminderd.in
	-sed -e s!\@PYTHONDIR\@!$(pythondir)! \
		< $< > $@

EXTRA_DIST += billreminderd.in
CLEANFILES += billreminderd
