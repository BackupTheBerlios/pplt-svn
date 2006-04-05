#include "Exceptions.h"
#include "Logging.h"
#include <iostream>

using namespace PPLTCore;

Error::Error(std::string message){
    CORELOG_ERROR(message);
    d_message = message;
}
Error::~Error(){ }
std::string Error::Message(){ return d_message; }
void Error::Message( std::string message){ d_message = message; }

CoreError::CoreError(std::string msg):Error(msg){ }
ModuleError::ModuleError(std::string msg): Error(msg){ }


NotImplementedYet::NotImplementedYet(std::string msg): CoreError(msg){ }


ModuleSetupError::ModuleSetupError(std::string message):ModuleError(message){ }
ModuleSetupError::~ModuleSetupError(){}

