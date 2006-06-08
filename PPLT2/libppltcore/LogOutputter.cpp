#include "Logging.h"

using namespace PPLTCore;

LogOutputter::LogOutputter(){ }
LogOutputter::~LogOutputter(){ }


/* 
 * a simple console logger... 
 */
ConsoleOutputter::ConsoleOutputter(){ }

void ConsoleOutputter::log(LogLevel level, std::string file, int line, std::string msg){
    switch(level){
        case LLDEBUG:
            std::cerr << "[DEBUG] ";
            break;
        case LLINFO:
            std::cerr << "[INFO] ";
            break;
        case LLWARNING:
            std::cerr << "[WARN] ";
            break;
        case LLERROR:
            std::cerr << "[ERROR] ";
            break;
        case LLFATAL:
            std::cerr << "[FATAL] ";
            break;
        default:
            std::cerr << "[???] ";
    };

    std::cerr << "in " << file << " at line " << line <<": " << msg << std::endl;
}



/*
 * a simple file logger...
 */
FileOutputter::FileOutputter(std::string file_name){
    d_file.open(file_name.c_str(), std::ios::app | std::ios::out);
}

FileOutputter::~FileOutputter(){
    d_file.close();
}

void FileOutputter::log(LogLevel level, std::string file , int line, std::string msg){
    switch(level){
        case LLDEBUG:
            d_file << "[DEBUG] ";
            break;
        case LLINFO:
            d_file << "[INFO] ";
            break;
        case LLWARNING:
            d_file << "[WARN] ";
            break;
        case LLERROR:
            d_file << "[ERROR] ";
            break;
        case LLFATAL:
            d_file << "[FATAL] ";
            break;
        default:
            d_file << "[???] ";
    };

    d_file << "in " << file << " at line " << line <<": " << msg << std::endl;
}
