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

#include <iostream>
#include <map>
#include <list>
#include <streambuf>
#include <sstream>
#include <fstream>
#include "Exceptions.h"


/** \file Logging.h
 * \brief contains all functions and macros for the Logging system.
 *
 * To init the logging, please call initLogging(). After calling
 * this function you can use all logging-functions.
 * The best way to log is to use the defined macros.
 */


namespace PPLTCore{
    typedef std::ostringstream      LoggingStream;
    
    #define CORELOG_DEBUG(msg)      LOG_DEBUG(PPLTCore::Logger::getInstance("Core"), msg)
    #define CORELOG_INFO(msg)       LOG_INFO(PPLTCore::Logger::getInstance("Core"), msg)
    #define CORELOG_WARN(msg)       LOG_WARN(PPLTCore::Logger::getInstance("Core"), msg)
    #define CORELOG_ERROR(msg)      LOG_ERROR(PPLTCore::Logger::getInstance("Core"), msg)
    #define CORELOG_FATAL(msg)      LOG_FATAL(PPLTCore::Logger::getInstance("Core"), msg)

    #define MODLOG_DEBUG(msg)       LOG_DEBUG(PPLTCore::Logger::getInstance("Module"), msg)
    #define MODLOG_INFO(msg)        LOG_INFO(PPLTCore::Logger::getInstance("Module"), msg)
    #define MODLOG_WARN(msg)        LOG_WARN(PPLTCore::Logger::getInstance("Module"), msg)
    #define MODLOG_ERROR(msg)       LOG_ERROR(PPLTCore::Logger::getInstance("Module"), msg)
    #define MODLOG_FATAL(msg)       LOG_FATAL(PPLTCore::Logger::getInstance("Module"), msg)

    #define LOG_DEBUG(inst, msg)    LOG(inst, LLDEBUG, msg)
    #define LOG_INFO(inst, msg)     LOG(inst, LLINFO, msg)
    #define LOG_WARN(inst, msg)     LOG(inst, LLWARNING, msg)
    #define LOG_ERROR(inst, msg)    LOG(inst, LLERROR, msg)
    #define LOG_FATAL(inst, msg)    LOG(inst, LLFATAL, msg)
    #define LOG(inst, level, msg)   do{\
                                        std::ostringstream buff;\
                                        buff << msg; \
                                        inst->log(level, __FILE__, __LINE__, buff.str());\
                                    }while(0);


    void initLogging();

    
    /** This enumeration defines the available loglevels */
    typedef enum {
        LLDEBUG     = 10,
        LLINFO      = 20,
        LLWARNING   = 30,
        LLERROR     = 40,
        LLFATAL     = 100
    } LogLevel;
   

    /** This class defines the basic interface for an outputter.
     * Outputters have to recive a logging request and to put them into the 
     * output ie a file or the screen.*/
    class LogOutputter{
        public:
            LogOutputter();
            virtual ~LogOutputter();

            virtual void log(LogLevel level, std::string file_name, int line, std::string msg) = 0;
    };

    
    
    /** Uses the console for output. */
    class ConsoleOutputter: public LogOutputter {
        public:
            ConsoleOutputter();
            virtual void log(LogLevel level, std::string file_name, int line, std::string msg);
    };


    
    /** Uses a file for output. */
    class FileOutputter: public LogOutputter{
        private:
            std::ofstream    d_file;
        public:
            FileOutputter(std::string file);
            virtual ~FileOutputter();

            virtual void log(LogLevel level, std::string file, int line, std::string msg);
    };

    /** This class defnies the basic (root) logging class. */
    class Logger{
        private:            
            /** This static member holds all loaded loggers.*/
            static std::map<std::string, Logger *>  s_loggers;

            /** This list takes all ouputters. */
            std::list<LogOutputter *>               d_outputters;

            /** This member defines the actual logging level (filter). */
            LogLevel                                d_log_level;

            /** Defines the parent logger.
             * All logging request are send also to the parent. */
            Logger                                  *d_parent_logger;        
            

        protected:
            std::string                             d_name;

            
        public:
            Logger(std::string name);
            Logger(std::string name, Logger *parent);
            virtual ~Logger();
            
            void attachOutput(LogOutputter *output);
            
            /** This method sets the logging level (filter).*/
            void logLevel(LogLevel level);
            /** This method returns the actual logging level (filter) for this
             * logger. */
            LogLevel  logLevel( void );
            
            virtual void log(LogLevel level, std::string file_name, int line, std::string msg);
            
            void debug(std::string file_name, int line, std::string msg);
            void info(std::string file_name, int line, std::string msg);
            void warning(std::string file_name, int line, std::string msg);
            void error(std::string file_name, int line, std::string msg);
            void fatal(std::string file_name, int line, std::string msg);

            static Logger *getInstance(std::string name);
    };


   
}
#endif
