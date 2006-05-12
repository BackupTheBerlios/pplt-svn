AC_PREREQ(2.59)
AC_INIT(libppltcore, "2.0.0", "hmatuschek@gmx.net")
AC_LANG(C++)
#AC_CONFIG_SRCDIR([cConnection.cpp])
AC_CONFIG_HEADER([config.h])

# Checks for programs.
AC_PROG_CXX
AC_PROG_CC

# Checks for libraries.
AC_CHECK_LIB(pthread, 
             pthread_mutex_init,,
             AC_MSG_ERROR([libpthread missing]))
AC_CHECK_LIB(dl,
             dlopen,,
             AC_MSG_ERROR([libld missing]))

# Checks for header files.
AC_HEADER_STDC
AC_CHECK_HEADERS([unistd.h])
AC_CHECK_HEADERS([pthread.h],,
                 AC_MSG_ERROR([pthread.h missing]))
AC_CHECK_HEADERS([log4cplus/logger.h],
                 AC_DEFINE(HAVE_LOG4CPLUS_LOGGER))

# Checks for typedefs, structures, and compiler characteristics.
AC_HEADER_STDBOOL
AC_C_CONST
AC_TYPE_SIZE_T
AC_HEADER_TIME

# Checks for library functions.
AC_FUNC_MALLOC
AC_FUNC_REALLOC
AC_CHECK_FUNCS([memmove])

AC_CONFIG_FILES([Makefile])
AC_OUTPUT
