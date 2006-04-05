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

    void initLogging();

    void Log(log4cplus::Logger log, log4cplus::LogLevel level, const char *file, int line,
                std::string func_name, std::string pat);

}
#endif
