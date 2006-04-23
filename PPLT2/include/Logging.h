/***************************************************************************
 *            Logging.h
 *
 *  Sun Apr 23 01:15:01 2006
 *  Copyright  2006  Hannes Matuschek
 *  hmatuschek@gmx.net
 ****************************************************************************/

/*
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 */
 

#ifndef PPLT_LOGGING_H
#define PPLT_LOGGING_H

#include <log4cplus/logger.h>
#include <log4cplus/consoleappender.h>

/** \file Logging.h
 * \brief contains all functions and macros for the Logging system.
 *
 * To init the logging, please call @see initLogging(). After calling
 * the function you can use all logging-functions.
 * The best way to log is to use the defined macros.
 */
namespace PPLTCore{
    #define CORELOG_DEBUG(msg)      LOG4CPLUS_DEBUG(log4cplus::Logger::getInstance("Core"), msg)
    #define CORELOG_INFO(msg)       LOG4CPLUS_INFO(log4cplus::Logger::getInstance("Core"), msg)
    #define CORELOG_WARN(msg)       LOG4CPLUS_WARN(log4cplus::Logger::getInstance("Core"), msg)
    #define CORELOG_ERROR(msg)      LOG4CPLUS_ERROR(log4cplus::Logger::getInstance("Core"), msg)
    #define CORELOG_FATAL(msg)      LOG4CPLUS_FATAL(log4cplus::Logger::getInstance("Core"), msg)

    #define MODLOG_DEBUG(msg)       LOG4CPLUS_DEBUG(log4cplus::Logger::getInstance("Module"), msg)
    #define MODLOG_INFO(msg)        LOG4CPLUS_INFO(log4cplus::Logger::getInstance("Module"), msg)
    #define MODLOG_WARN(msg)        LOG4CPLUS_WARN(log4cplus::Logger::getInstance("Module"), msg)
    #define MODLOG_ERROR(msg)       LOG4CPLUS_ERROR(log4cplus::Logger::getInstance("Module"), msg)
    #define MODLOG_FATAL(msg)       LOG4CPLUS_FATAL(log4cplus::Logger::getInstance("Module"), msg)

    /** Logging initializer.
    * This function will init the logging system. Simply call this
    * function before calling any other PPLT stuff to get the logging
    * running. This function takes no parameters. */
    void initLogging();

    void Log(log4cplus::Logger log, log4cplus::LogLevel level, const char *file, int line,
                std::string func_name, std::string pat);

}
#endif
