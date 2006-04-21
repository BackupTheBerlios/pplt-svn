#include "../include/Exceptions.h"
#include "../include/Logging.h"
#include <iostream>
#include <execinfo.h>

using namespace PPLTCore;

Error::Error(std::string message){
    void *bt[256];
    size_t  size;
    char **strings;
    
    CORELOG_ERROR(message);
    size = backtrace(bt, 256);
    strings = backtrace_symbols(bt, size);
    printf("BACKTRACE (%i)\n",size);
    for(int i=0;i<size;i++)
        printf(" %s\n",strings[i]);
    printf("-----\n");
    free(strings);
    
    d_message = message;
}
Error::~Error(){ }
std::string Error::Message(){ return d_message; }
void Error::Message( std::string message){d_message = message;}

CoreError::CoreError(std::string msg):Error(msg){ }
ModuleError::ModuleError(std::string msg): Error(msg){ }


NotImplementedYet::NotImplementedYet(std::string msg): CoreError(msg){ }


ModuleSetupError::ModuleSetupError(std::string message):ModuleError(message){ }
ModuleSetupError::~ModuleSetupError(){}
