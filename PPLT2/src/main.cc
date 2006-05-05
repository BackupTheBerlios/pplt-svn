#include "../include/cFloatSymbol.h"
#include "../include/soModuleLoader.h"
#include "../include/cModule.h"

using namespace PPLTCore;



int main(void){
    PPLTCore::initLogging();
    soModuleLoader  loader("../plugins/src/");
    cModule         *mod = loader.load("PPLTCoreStdPackage.so.2.0.0",
                                       "TimeModuleFactory", 
                                       tModuleParameters());
    cFloatSymbol    symb(mod, "timestamp");
    double          val1, val2;
    val1 = symb.get();
    std::cout << "Unix timestamp: " << val1 << "sec." <<std::endl;
    sleep(2);
    val2 = symb.get();
    std::cout << "Unix timestamp: " << val2 << "sec." <<std::endl;
    std::cout << "Diff: " << val2-val1 << std::endl;
    
    
return(0);        
}
