# -*- coding: utf-8 -*-

import os
import shutil
from lib.common import APPNAME
from xdg.BaseDirectory import *

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
            src = os.path.join(os.path.realpath(os.curdir), "manage.py")
            dest = os.path.join(conf_dir, "manage.py")
            os.mkdir(conf_dir)
            shutil.copyfile(src, dest)

    # Data storage
    data_dir = os.path.join(xdg_data_home, APPNAME.lower())
    # Create the directory if it doesn't exist
    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)

    # Are all the django files in place?

if __name__ == "__main__":
    main()
