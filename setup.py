#!/usr/bin/python
# Copyright (C) 2007 by Og Maciel <og.maciel@gmail.com>
#
# Provided under MIT licence, please see included
# COPYRIGHT and/or COPYING file.

from distutils.core import setup
from distutils.command.install_data import install_data
from distutils.dep_util import newer
from distutils.log import info
import glob
import os
import sys

class InstallData(install_data):
	def run(self):
		install_data.run(self)


setup(name='BillReminder',
      version='0.1',
      description='BillReminder - A desktop bill reminder for Gnu/Linux.',
      author='Og Maciel',
      author_email='og.maciel@gmail.com',
      url='http://billreminder.sourceforge.net/',
      package_dir={'billreminder': 'src'},
      packages=['billreminder',
        'billreminder.model',
        'billreminder.model.db',
        'billreminder.view',
        'billreminder.controller'],
      scripts=['billreminder', 'src/startup.py', 'src/notifier.py'],
      data_files=[('/usr/share/billreminder/gui', 
        ['gui/billdialog.glade',
         'gui/maindialog.glade',
         'gui/aboutdialog.glade']),
         ('/usr/share/applications', ['billreminder.desktop']),
         ('/etc/xdg/autostart', ['billremindernotifier.desktop']),
         ('/usr/share/billreminder/images',
         ['images/billreminder.ico',
         'images/billreminder.png',
         'images/header.png'],
         ['/usr/bin', 'billreminder']),
         ('/usr/share/locale/sv/LC_MESSAGES', ['locale/sv/LC_MESSAGES/billreminder.mo'])
         ('/usr/share/locale/pt_BR/LC_MESSAGES', ['locale/pt_BR/LC_MESSAGES/billreminder.mo'])
        ],
      cmdclass={'install_data': InstallData}
      )
