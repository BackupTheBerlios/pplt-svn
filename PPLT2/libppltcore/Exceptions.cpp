/***************************************************************************
 *            Exceptions.cpp
 *
 *  Sun Apr 23 01:25:40 2006
 *  Copyright  2006  Hannes Matuschek
 *  hmatuschek@gmx.net
 ****************************************************************************/

#include "Exceptions.h"

using namespace PPLTCore;

Error::Error(){ }

Error::Error(std::string message){
    // log the exception message
    log_message(message);   
    // log traceback...    
    do_traceback();
}


Error::Error(const char *temp, ...){
    va_list     ap;
    
    // create string from va_list: (like fprintf()) and log it
    va_start(ap, temp); 
    log_message(temp, ap);
    va_end(ap);
    
    // make the traceback
    do_traceback();
}


void Error::do_traceback(void){
    /* FIXME
     * Implement the translation of symbol into readable from using the regexp
     * "^((.*)\\(([[:alnum:]_]+)\\)|(.*)) \\[(.+)\\]$" */
    #ifdef HAVE_EXECINFO
        void                *bt[256];
        size_t              size;
        char                **strings;
        std::ostringstream  dump("",std::ios::ate);
    
        size = backtrace(bt, 256);
        strings = backtrace_symbols(bt, size);

        dump << "BACKTRACE ("<<size<<")\n";
        for(unsigned int i=0;i<size;i++)
            dump << " " << format_traceback(strings[i]) << std::endl;
        dump << "----- ";

        CORELOG_DEBUG(dump.str());
        free(strings);
    #endif
}



std::string Error::format_traceback(const char *line){
    //wxRegEx     reg(wxT("([^@]+)[\\(([[:alnum:]_]+)\\)|] \\[0x[:alnum:]+\\]")); 
    std::string ret(line);
    /*wxString    match;

    if(!reg.Matches(wxString(line, *wxConvCurrent))){
        std::cout << "No match..." << std::endl;
        return "";
    }        
    ret += "In ";
    ret += reg.GetMatch(match, 1).mbc_str();*/
    return ret;
}



void Error::log_message(std::string msg){
    d_message = msg;
    CORELOG_ERROR(msg);
}

void Error::log_message(const char *temp, va_list ap){
    char        *message;
    vasprintf(&message, temp, ap);
    log_message(std::string(message));
    free(message);
}

Error::~Error(){ }

std::string Error::Message(){ return d_message; }

void Error::Message( std::string message){d_message = message;}



CoreError::CoreError(){ }
CoreError::CoreError(std::string msg):Error(msg){ }
CoreError::CoreError(const char *temp, ...){
    va_list     ap;
    
    va_start(ap, temp);
    log_message(temp, ap);
    va_end(ap);
    
    do_traceback();
}


ModuleError::ModuleError(){ }
ModuleError::ModuleError(std::string msg): Error(msg){ }
ModuleError::ModuleError(const char *temp, ...){
    va_list     ap;
    
    va_start(ap, temp);
    log_message(temp, ap);
    va_end(ap);

    do_traceback();
}    
    

NotImplementedYet::NotImplementedYet(){ }
NotImplementedYet::NotImplementedYet(std::string msg): CoreError(msg){ }
NotImplementedYet::NotImplementedYet(const char *temp, ...){
    va_list     ap;
    
    va_start(ap, temp);
    log_message(temp, ap);
    va_end(ap);
    
    do_traceback();
}    

ItemNotFound::ItemNotFound(){ }
ItemNotFound::ItemNotFound(std::string msg): Error(msg){ }
ItemNotFound::ItemNotFound(const char *temp, ...){
    va_list     ap;
    
    va_start(ap, temp);
    log_message(temp, ap);
    va_end(ap);
    
    do_traceback();    
}


ItemBusy::ItemBusy(){ }
ItemBusy::ItemBusy(std::string msg): Error(msg){ }
ItemBusy::ItemBusy(const char *temp, ...){
    va_list     ap;
    
    va_start(ap, temp);
    log_message(temp, ap);
    va_end(ap);
    
    do_traceback();    
}



SymbolReconversionError::SymbolReconversionError(){}
SymbolReconversionError::SymbolReconversionError(std::string msg): Error(msg){ }
SymbolReconversionError::SymbolReconversionError(const char *temp, ...){
    va_list     ap;
    
    va_start(ap, temp);
    log_message(temp, ap);
    va_end(ap);
    
    do_traceback();    
}



ModuleSetupError::ModuleSetupError(){ }
ModuleSetupError::ModuleSetupError(std::string message):ModuleError(message){ }
ModuleSetupError::ModuleSetupError(const char *temp, ...){
    va_list     ap;
    
    va_start(ap, temp);
    log_message(temp, ap);
    va_end(ap);
    
    do_traceback();    
}
