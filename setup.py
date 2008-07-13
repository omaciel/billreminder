#!/usr/bin/env python

from distutils.core import setup
from distutils.command.install_data import install_data
from distutils.dist import Distribution
from distutils.command.build import build
from distutils.dep_util import newer
from distutils.log import info
import glob
import os
import sys
import subprocess
import platform

from src.lib.common import APPVERSION

PO_DIR = 'po'
MO_DIR = os.path.join('build', 'mo')

class BillReminderDist(Distribution):
  global_options = Distribution.global_options + [
    ("without-gettext", None, "Don't build/install gettext .mo files")]

  def __init__ (self, *args):
    self.without_gettext = False
    Distribution.__init__(self, *args)


class BuildData(build):
  def run (self):
    build.run (self)

    if self.distribution.without_gettext:
      return

    for po in glob.glob (os.path.join (PO_DIR, '*.po')):
      lang = os.path.basename(po[:-3])
      mo = os.path.join(MO_DIR, lang, 'billreminder.mo')

      directory = os.path.dirname(mo)
      if not os.path.exists(directory):
        info('creating %s' % directory)
        os.makedirs(directory)

      if newer(po, mo):
        info('compiling %s -> %s' % (po, mo))
        try:
          rc = subprocess.call(['msgfmt', '-o', mo, po])
          if rc != 0:
            raise Warning, "msgfmt returned %d" % rc
        except Exception, e:
          print "Building gettext files failed.  Try setup.py --without-gettext [build|install]"
          print "%s: %s" % (type(e), e)
          sys.exit(1)

class InstallSchema(object):

  def run(self):
    try:
      rc = subprocess.call(['GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`', \
        'gconftool-2', '--makefile-install-rule', '/etc/gconf/schemas/billreminder.schemas'])
      if rc != 0:
        raise Warning, "gconftool returned %d" % rc
    except Exception, e:
      print "Registering the gconf schema has failed."
      print "%s: %s" % (type(e), e)
      sys.exit(1)

class InstallData(install_data):
  def run (self):
    self.data_files.extend (self._find_mo_files ())
    install_data.run (self)


  def _find_mo_files (self):
    data_files = []

    if not self.distribution.without_gettext:
      for mo in glob.glob (os.path.join (MO_DIR, '*', 'billreminder.mo')):
       lang = os.path.basename(os.path.dirname(mo))
       dest = os.path.join('share', 'locale', lang, 'LC_MESSAGES')
       data_files.append((dest, [mo]))

    return data_files


if platform.system() == 'FreeBSD':
  man_dir = 'man'
else:
  man_dir = 'share/man'

setup(name='BillReminder',
      version=APPVERSION,
      description="BillReminder, We may not pay your bills, but we'll do our best to help you remember to pay them!",
      author='Og Maciel',
      author_email='ogmaciel@gnome.org',
      url='http://billreminder.gnulinuxbrasil.org',
      license='BSD',
      scripts=['billreminder', 'billreminderd'],
      data_files=[
          ('share/applications', ['data/billreminder.desktop', 'data/billreminderd.desktop']),
          ('/etc/gconf/schemas', ['data/billreminder.schemas']),
          (os.path.join(man_dir, 'man1'), ['man/billreminder.1', 'man/billreminderd.1']),
          ('share/dbus-1/services', ['data/billreminder.service']),
          ('share/doc/billreminder-%s' % APPVERSION,
           ['AUTHORS', 'ChangeLog', 'CONTRIBUTORS', 'COPYING', 'COPYRIGHT', 'INSTALL', 
           'LICENSE', 'NEWS', 'MAINTAINERS', 'README', 'TODO']),
          ('share/xdg/autostart', ['data/billreminderd.desktop']),
          ('share/billreminder/images',
           ['data/images/billreminder16.png', 'images/applet-critical.png', 'images/billreminder.ico', 'images/billreminder.png', 'images/header.jpg', 'images/header.png']),
          ('share/pixmaps', ['data/images/billreminder.png']),
          ('share/icons/hicolor/scalable/apps', glob.glob('data/images/billreminder.svg')),
          ('share/icons/hicolor/16x16/apps', glob.glob('data/images/billreminder16.png')),
          ('share/icons/hicolor/22x22/apps', glob.glob('data/images/billreminder22.png')),
          ('share/icons/hicolor/24x24/apps', glob.glob('data/images/billreminder24.png')),
          ('share/icons/hicolor/48x48/apps', glob.glob('data/images/billreminder48.png')),
          ('share/icons/hicolor/96x96/apps', glob.glob('data/images/billreminder96.png')),
          ('share/icons/hicolor/128x128/apps', glob.glob('data/images/billreminder128.png')),
          ('share/icons/hicolor/16x16/actions', glob.glob('data/images/billreminder16.png')),
         ],
      package_dir={'billreminder': 'src'},
      #config_files=[('gconf/schemas', ['data/billreminder.schemas'], 'with-gconf-schema-file-dir')],
      #packages=['billreminder', 'billreminder.daemon', 'billreminder.db', 'billreminder.gui', 
      # 'billreminder.gui.widgets', 'billreminder.lib', 'data', 'data/images'],
      cmdclass={'build': BuildData, 'install_data': InstallData, 'install_schema': InstallSchema},
      distclass=BillReminderDist
     )

