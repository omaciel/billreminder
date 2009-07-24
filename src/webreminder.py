# -*- coding: utf-8 -*-

import os
import sys
import shutil
from lib.common import APPNAME
from xdg.BaseDirectory import *

runningfrom = ''
''
def main():

    # Configuration files
    conf_dir = os.path.join(xdg_config_home, APPNAME.lower())
    # If the configuration directory doesn't exist, then create it
    # and copy all the "django" files to it.

    # TODO: The location of where these files are is determined on the
    # following: if the application is installed in the system, then get
    # it from xdg_config_dirs, else get a copy from the checkout code.
    if not os.path.isdir(conf_dir):
        try:
            configfiles = os.path.join(xdg_config_dirs, APPNAME.lower())
            shutil.copytree(configfiles, conf_dir)
        except Exception, e:
            # Create the directory
            os.mkdir(conf_dir)
            # Get the location of where the source code lives
            curDir = os.path.abspath(os.path.dirname(sys.argv[0]))
            for f in ["__init__.py", "manage.py", "settings.py", "urls.py"]:
                src = os.path.join(os.path.realpath(curDir), f)
                dest = os.path.join(conf_dir, f)
                shutil.copyfile(src, dest)
            # Copy the django app itself
            shutil.copytree(os.path.join(curDir, "bills"), os.path.join(conf_dir, "bills"))

    # Data storage
    data_dir = os.path.join(xdg_data_home, APPNAME.lower())
    # Create the directory if it doesn't exist
    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)

if __name__ == "__main__":
    main()
