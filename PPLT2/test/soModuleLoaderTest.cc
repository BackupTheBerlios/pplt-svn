#include "soModuleLoaderTest.h"

using namespace PPLTCore;
using namespace PPLTCore::Test;

CPPUNIT_TEST_SUITE_REGISTRATION(soModuleLoaderTest);

void soModuleLoaderTest::setUp( void ){
    // init module loader:
    module_loader = new soModuleLoader();
}

void soModuleLoaderTest::tearDown( void ){ 
    delete module_loader;
}

void soModuleLoaderTest::test_ModuleFinding( void ){
    cModule     *tmp;
    
    // check if a module-file can be found if it exists in the path:
    CPPUNIT_ASSERT_THROW( module_loader->load("notknown.so", "NotKnown", tModuleParameters()),
                          ItemNotFound);
                          
    // check for exception if factory can't be found:
    CPPUNIT_ASSERT_THROW( module_loader->load("../plugins/ppltstdmodules.so", "NotKnown", tModuleParameters()),
                          ItemNotFound);

    // checks if a exception will be raised if the given .so file is not one:
    CPPUNIT_ASSERT_THROW( module_loader->load("../plugins/NULLModule.h", "NotKnown", tModuleParameters()),
                          ItemNotFound);
    
}

void soModuleLoaderTest::test_ModuleLoading(void){
    cModule     *tmp;

    //checks if a module will be loaded correctly:
    CPPUNIT_ASSERT_NO_THROW( tmp = module_loader->load("../plugins/ppltstdmodules.so", "NULLModuleFactory", tModuleParameters()) );

    // checks if a module will be unloaded correctly:
    CPPUNIT_ASSERT_NO_THROW( module_loader->unload(tmp) );
}


