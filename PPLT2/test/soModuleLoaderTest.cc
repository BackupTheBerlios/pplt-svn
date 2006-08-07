#include "libPPLTCoreTest.h"

using namespace PPLTCore;
using namespace PPLTCore::Test;


void libPPLTCoreTest::test_ModuleFinding( void ){
    // check if a module-file can be found if it exists in the path:
    ASSUME_THROW( module_loader->load("notknown.so", "NotKnown", tModuleParameters()),
                   ItemNotFound);
                          
    // check for exception if factory can't be found:
    ASSUME_THROW( module_loader->load("../plugins/libppltcoremodules.so", "NotKnown", tModuleParameters()),
                   ItemNotFound);

    // checks if a exception will be raised if the given .so file is not one:
    ASSUME_THROW( module_loader->load("../plugins/NULLModule.h", "NotKnown", tModuleParameters()),
                   ItemNotFound);
    
}

void libPPLTCoreTest::test_ModuleLoading(void){
    cModule     *tmp;

    //checks if a module will be loaded correctly:
    ASSUME_NO_THROW( tmp = module_loader->load("../plugins/libppltcoremodules.so", "NULLModuleFactory", tModuleParameters()));
    ASSUME_FALSE( 0 == tmp );

    // checks if a module will be unloaded correctly:
    ASSUME_NO_THROW( module_loader->unload(tmp));
}


