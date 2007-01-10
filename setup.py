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
      description='BillReminder - And bills-hell is history',
      author='Og Maciel',
      author_email='og.maciel@gmail.com',
      url='http://billreminder.sourceforge.net/',
      packages=['billreminder'],
      scripts=['billy'],
      data_files=[('share/billreminder', ['billreminder.glade',
                                          'icon.ico',
                                          'billreminder.gladep',
				          'header.jpg']),
                  ('share/applications', ['billreminder.desktop']),
                  ('share/pixmaps', ['icon.ico'])
                 ],
	cmdclass={'install_data': InstallData
			}
	)
