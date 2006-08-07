#include "libPPLTCoreTest.h"

using namespace PPLTCore;
using namespace PPLTCore::Test;

void libPPLTCoreTest::setup( void ){
    initLogging();
    module_loader = new soModuleLoader();
}

void libPPLTCoreTest::teardown( void ){
    delete module_loader;
}

