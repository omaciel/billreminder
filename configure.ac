dnl -*- Mode: autoconf -*-
dnl Process this file with autoconf to produce a configure script.
AC_PREREQ(2.53)
AC_INIT(billreminder, 0.3.1, http://code.google.com/p/billreminder/)
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
IT_PROG_INTLTOOL([0.35.0])

AM_PATH_PYTHON(2.4)

AC_ARG_WITH([session_bus_services_dir],
            AC_HELP_STRING([--with-session-bus-services-dir], [Path to DBus services directory]))

if test "x$with_dbus_service_dir" != "x"; then
	DBUS_SERVICES_DIR=$with_dbus_service_dir
else
	DBUS_SERVICES_DIR=${datadir}/dbus-1/services
fi
AC_SUBST(DBUS_SERVICES_DIR)

AM_CHECK_PYMOD([gobject], , , AC_MSG_ERROR([Python module gobject required to run BillReminder]))
AM_CHECK_PYMOD_VERSION([pysqlite2.dbapi2], [version], [2.3.0], , AC_MSG_ERROR([Python module pysqlite2 >= 2.3.0 required to run BillReminder]))
AM_CHECK_PYMOD([dbus], , , AC_MSG_ERROR([Python module dbus required to run BillReminder]))

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


