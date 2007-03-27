#!/usr/bin/python
# -*- coding: utf-8 -*-

program = 'billreminder'

import locale
LC_ALL = locale.setlocale(locale.LC_ALL, '') 

print LC_ALL
try:
    import gettext
    from gettext import gettext as _
    gettext.install(program, unicode=True)
except ImportError:
    import sys
    print >> sys.stderr, ("You don't have gettext module, no " \
                          "internationalization will be used.")
    import __builtin__
    __builtin__.__dict__['_'] = lambda x: x