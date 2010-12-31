dnl -*- Mode: autoconf -*-
dnl Process this file with autoconf to produce a configure script.
AC_PREREQ(2.53)
AC_INIT(billreminder, 0.4.0, http://billreminder.gnulinuxbrasil.org/)
AC_CONFIG_SRCDIR(billreminder.in)
AM_INIT_AUTOMAKE([1.7])
AC_CONFIG_MACRO_DIR([m4])
AM_MAINTAINER_MODE
AC_SUBST(ACLOCAL_AMFLAGS, "$ACLOCAL_FLAGS -I m4")

dnl put the ACLOCAL flags in the makefile
ACLOCAL="$ACLOCAL $ACLOCAL_FLAGS"

GETTEXT_PACKAGE=billreminder
AC_SUBST(GETTEXT_PACKAGE)
AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE, "$GETTEXT_PACKAGE", [Gettext package])
AM_GLIB_GNU_GETTEXT
IT_PROG_INTLTOOL([0.40.0])

AM_PATH_PYTHON(2.4)

AC_ARG_WITH([session_bus_services_dir],
            AC_HELP_STRING([--with-session-bus-services-dir], [Path to DBus services directory]))

if test "x$with_dbus_service_dir" != "x"; then
	DBUS_SERVICES_DIR=$with_dbus_service_dir
else
	DBUS_SERVICES_DIR=${datadir}/dbus-1/services
fi
AC_SUBST(DBUS_SERVICES_DIR)

AC_SUBST(VERSION)

AM_CHECK_PYMOD([gobject], , , AC_MSG_ERROR([Python module gobject required to run BillReminder]))

dnl This entire python check section borrowed from the hamster-applet project.
if test "x$PYTHON_VERSION" = "x2.5"; then
    AC_MSG_CHECKING([for python sqlite module])
    if AC_RUN_LOG([DISPLAY= $PYTHON -c '
try:
    import sqlite3
except ImportError, e:
    if str(e).find("sqlite3") >= 0:
        raise
except:
    pass
    ']); then
      AC_MSG_RESULT([yes])
    else
      AC_MSG_RESULT([no])
      AC_MSG_ERROR([Python 2.5: inbuilt sqlite is required to build BillReminder])
    fi
else
    AC_MSG_CHECKING([for pysqlite2 module])
    if AC_RUN_LOG([DISPLAY= $PYTHON -c '
try:
    import pysqlite2
except ImportError, e:
    if str(e).find("pysqlite2") >= 0:
        raise
except:
    pass
    ']); then
      AC_MSG_RESULT([yes])
    else
      AC_MSG_RESULT([no])
      AC_MSG_ERROR([Python 2.4: pysqlite2 module required to build BillReminder])
    fi
fi


AM_CHECK_PYMOD([dbus], , , AC_MSG_ERROR([Python module dbus required to run BillReminder]))

AC_PATH_PROG(GCONFTOOL, gconftool-2)
AM_GCONF_SOURCE_2

AC_OUTPUT([
Makefile
data/Makefile
data/images/Makefile
man/Makefile
po/Makefile.in
src/Makefile
src/daemon/Makefile
src/db/Makefile
src/gui/Makefile
src/gui/widgets/Makefile
src/lib/Makefile
])


