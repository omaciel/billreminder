# -*- coding: utf-8 -*-

__all__ = ['Statusbar']

import gtk
import pango

from lib import i18n

class Statusbar(gtk.HBox):
    """ This class implements the note bar """
    def __init__(self):
        gtk.HBox.__init__(self)

        self.recordLabel = gtk.Label()
        self.recordLabel.set_justify(gtk.JUSTIFY_LEFT)
        self.recordLabel.set_markup("<b>%s </b>" % _("Bills:"))
        self.pack_start(self.recordLabel, expand=False, fill=True, padding=2)

        self.recordCount = gtk.Label()
        self.recordCount.set_justify(gtk.JUSTIFY_RIGHT)
        self.recordCount.set_markup("<b>0</b>")
        self.pack_start(self.recordCount, expand=False, fill=True, padding=2)

        self.noteLabel = gtk.Label()
        self.noteLabel.set_justify(gtk.JUSTIFY_LEFT)
        self.noteLabel.set_markup("<b>%s </b>" % _("Notes:"))
        self.pack_start(self.noteLabel, expand=False, fill=True, padding=2)

        self.noteValue = gtk.Label()
        self.noteValue.set_justify(gtk.JUSTIFY_LEFT)
        self.noteValue.set_markup("")
        self.pack_start(self.noteValue, expand=True, fill=True, padding=2)

        self.infoValue = gtk.Label()
        self.infoValue.set_justify(gtk.JUSTIFY_RIGHT)
        self.infoValue.set_markup("")
        self.pack_start(self.infoValue, expand=False, fill=True, padding=2)

        self.set_border_width(2)

    def Records(self, count):
        self.recordCount.set_markup("%(count)d  " % {'count': count})

    def Notes(self, notes=''):
        if notes:          
            # Add notes to status bar...
            self.noteValue.set_markup("%(notes)s" % \
                {'notes': notes.replace('\n', ' ')})
            # ... and a tooltip.
            self.noteValue.set_tooltip_text(notes.replace('\n', ' '))
            self.noteValue.set_ellipsize(pango.ELLIPSIZE_END)  
        else:
            self.noteValue.set_markup('')

    def Info(self, info=''):
        if info:
            # Add notes to status bar...
            self.infoValue.set_markup("<b>%(info)s</b>" % \
                {'info': info.replace('\n', ' ')})
            # ... and a tooltip.
            self.infoValue.set_tooltip_text(info.replace('\n', ' '))
        else:
            self.infoValue.set_markup('')
