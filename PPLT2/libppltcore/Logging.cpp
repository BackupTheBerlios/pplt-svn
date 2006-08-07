/***************************************************************************
 *            Logging.cpp
 *
 *  Sun Apr 23 01:25:55 2006
 *  Copyright  2006  Hannes Matuschek
 *  hmatuschek@gmx.net
 ****************************************************************************/

#include "Logging.h"

using namespace PPLTCore;

std::map<std::string, Logger *> Logger::s_loggers; 

void PPLTCore::initLogging(){
    Logger  *root, *mod;
    
    // create a new "root" Logger:
    root = new Logger("Core");
    
    // attach module logger to root:
    mod  = new Logger("Module", root);

    //append console outputter at root:
    LogOutputter *out = new FileOutputter("test.log");
    root->attachOutput(out);
    
    //Test it:
    root = Logger::getInstance("Core");
    root->log(LLINFO, __FILE__, __LINE__, "Logging started...");
}



Logger::Logger(std::string name){
    d_log_level = LLDEBUG;
    d_name = name;
    Logger::s_loggers[name] =  this;
    d_parent_logger = 0;
}



Logger::Logger(std::string name, Logger *parent){
    d_log_level = LLDEBUG;
    d_name = name;
    Logger::s_loggers[name] = this;
    d_parent_logger = parent;
}



Logger::~Logger(){
    for(std::list<LogOutputter *>::iterator it = d_outputters.begin();
        it != d_outputters.end(); ++it){
            delete (*it);
    }
}



Logger *Logger::getInstance(std::string name){
    if(0 == Logger::s_loggers.count(name)){
        Logger::s_loggers[name] = new Logger(name);
        Logger::s_loggers[name]->attachOutput(new ConsoleOutputter());
        Logger::s_loggers[name]->log(LLINFO, __FILE__, __LINE__, name + " Logger created!");
    }    

    return Logger::s_loggers[name];        
}



void Logger::logLevel(LogLevel level){
    d_log_level = level;
}




LogLevel Logger::logLevel( void ){
    return d_log_level;
}



void Logger::log(LogLevel level, std::string file, int line, std::string msg){
    if(0 != d_parent_logger)
        d_parent_logger->log(level, file, line, msg);

    if(level < d_log_level)
        return;

    for(std::list<LogOutputter *>::iterator it = d_outputters.begin();
        it != d_outputters.end(); ++it){
            (*it)->log(level, file, line, msg);     
    }
}   

void Logger::debug(std::string file, int line, std::string msg)   { log(LLDEBUG,   file, line, msg); }
void Logger::info(std::string file, int line, std::string msg)    { log(LLINFO,    file, line, msg); }
void Logger::warning(std::string file, int line, std::string msg) { log(LLWARNING, file, line, msg); }
void Logger::error(std::string file, int line, std::string msg)   { log(LLERROR,   file, line, msg); }
void Logger::fatal(std::string file, int line, std::string msg)   { log(LLFATAL,   file, line, msg); }



void Logger::attachOutput(LogOutputter *output){
    d_outputters.push_back(output);
}    
