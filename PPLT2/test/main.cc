#include "libppltcore/ppltcore.h"

using namespace PPLTCore;

int main(void){
    initLogging();

    soModuleLoader  loader("/home/hannes/Projekte/PPLT/PPLT2/plugins");
    cModule         *mod1 = loader.load("ppltstdmodules.so", "TimeModuleFactory", tModuleParameters());
    cSymbol         sym(mod1, "timestamp");

    std::cout << "Now: "<< sym.getFloat() << " ...\n"; 

    
   
return(0);
}

