# -*- coding: utf-8 -*-

__all__ = ['Statusbar']

import gtk

from lib import i18n

class Statusbar(gtk.HBox):
    """ This class implements the note bar """
    def __init__(self):
        gtk.HBox.__init__(self)

        self.recordLabel = gtk.Label()
        self.recordLabel.set_justify(gtk.JUSTIFY_LEFT)
        self.recordLabel.set_markup("<b>%s </b>" % _("Records:"))
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
        self.pack_start(self.noteValue, expand=False, fill=True, padding=2)

        self.set_border_width(2)

    def Records(self, count):
        self.recordCount.set_markup("%(count)d  " % {'count': count})

    def Notes(self, notes=''):
        if notes:
            self.noteValue.set_markup("%(notes)s" % \
                                      {'notes': notes.replace('\n', ' ')})
        else:
            self.noteValue.set_markup('')
