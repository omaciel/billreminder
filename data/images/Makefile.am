## Process this file with automake to produce Makefile.in

pixmapdir = $(datadir)/pixmaps
pixmap_DATA = billreminder.png

hicolordir = $(datadir)/icons/hicolor

tango_icons = \
	billreminder16.png \
	billreminder20.png \
	billreminder22.png \
	billreminder24.png \
	billreminder32.png \
	billreminder48.png \
	billreminder64.png \
	billreminder72.png \
	billreminder96.png \
	billreminder128.png \
	billreminder.png \
	billreminder.svg

install-data-local:
	@-$(mkinstalldirs) $(DESTDIR)$(hicolordir)/16x16/apps
	$(INSTALL_DATA) $(srcdir)/billreminder16.png $(DESTDIR)$(hicolordir)/16x16/apps/billreminder.png
	@-$(mkinstalldirs) $(DESTDIR)$(hicolordir)/20x20/apps
	$(INSTALL_DATA) $(srcdir)/billreminder20.png $(DESTDIR)$(hicolordir)/20x20/apps/billreminder.png
	@-$(mkinstalldirs) $(DESTDIR)$(hicolordir)/22x22/apps
	$(INSTALL_DATA) $(srcdir)/billreminder22.png $(DESTDIR)$(hicolordir)/22x22/apps/billreminder.png
	@-$(mkinstalldirs) $(DESTDIR)$(hicolordir)/24x24/apps
	$(INSTALL_DATA) $(srcdir)/billreminder24.png $(DESTDIR)$(hicolordir)/24x24/apps/billreminder.png
	@-$(mkinstalldirs) $(DESTDIR)$(hicolordir)/32x32/apps
	$(INSTALL_DATA) $(srcdir)/billreminder32.png $(DESTDIR)$(hicolordir)/32x32/apps/billreminder.png
	@-$(mkinstalldirs) $(DESTDIR)$(hicolordir)/48x48/apps
	$(INSTALL_DATA) $(srcdir)/billreminder48.png $(DESTDIR)$(hicolordir)/48x48/apps/billreminder.png
	@-$(mkinstalldirs) $(DESTDIR)$(hicolordir)/64x64/apps
	$(INSTALL_DATA) $(srcdir)/billreminder64.png $(DESTDIR)$(hicolordir)/64x64/apps/billreminder.png
	@-$(mkinstalldirs) $(DESTDIR)$(hicolordir)/72x72/apps
	$(INSTALL_DATA) $(srcdir)/billreminder72.png $(DESTDIR)$(hicolordir)/72x72/apps/billreminder.png
	@-$(mkinstalldirs) $(DESTDIR)$(hicolordir)/96x96/apps
	$(INSTALL_DATA) $(srcdir)/billreminder96.png $(DESTDIR)$(hicolordir)/96x96/apps/billreminder.png
	@-$(mkinstalldirs) $(DESTDIR)$(hicolordir)/128x128/apps
	$(INSTALL_DATA) $(srcdir)/billreminder128.png $(DESTDIR)$(hicolordir)/128x128/apps/billreminder.png
	@-$(mkinstalldirs) $(DESTDIR)$(hicolordir)/scalable/apps
	$(INSTALL_DATA) $(srcdir)/billreminder.svg $(DESTDIR)$(hicolordir)/scalable/apps/billreminder.svg

uninstall-hook:
	rm -f $(DESTDIR)$(hicolordir)/scalable/apps/billreminder.svg
	rm -f $(DESTDIR)$(hicolordir)/128x128/apps/billreminder.png
	rm -f $(DESTDIR)$(hicolordir)/96x96/apps/billreminder.png
	rm -f $(DESTDIR)$(hicolordir)/72x72/apps/billreminder.png
	rm -f $(DESTDIR)$(hicolordir)/64x64/apps/billreminder.png
	rm -f $(DESTDIR)$(hicolordir)/48x48/apps/billreminder.png
	rm -f $(DESTDIR)$(hicolordir)/32x32/apps/billreminder.png
	rm -f $(DESTDIR)$(hicolordir)/24x24/apps/billreminder.png
	rm -f $(DESTDIR)$(hicolordir)/22x22/apps/billreminder.png
	rm -f $(DESTDIR)$(hicolordir)/20x20/apps/billreminder.png
	rm -f $(DESTDIR)$(hicolordir)/16x16/apps/billreminder.png

imagesdir = $(datadir)/billreminder/images
images_DATA = \
	billreminder.png \
	billreminder16.png \
	header.png
EXTRA_DIST = $(images_DATA)

noinst_DATA = \
	applet-critical.png \
	billreminder.ico \
	header.jpg

EXTRA_DIST += \
	$(noinst_DATA) \
	$(pixmap_DATA) \
	$(tango_icons) \
	$(images_DATA)

CLEANFILES =

gtk_update_icon_cache = gtk-update-icon-cache -f -t $(datadir)/icons/hicolor

install-data-hook:
	@-if test -z "$(DESTDIR)"; then \
		echo "Updating Gtk icon cache."; \
		$(gtk_update_icon_cache); \
	else \
		echo "*** Icon cache not updated. After install, run this:"; \
		echo "***   $(gtk_update_icon_cache)"; \
	fi
