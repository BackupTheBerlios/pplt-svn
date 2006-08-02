#include "libPPLTCoreTest.h"

using namespace PPLTCore;
using namespace PPLTCore::Test;

void libPPLTCoreTest::initTestCase( void ){
    initLogging();
    module_loader = new soModuleLoader();
}

void libPPLTCoreTest::cleanupTestCase( void ){
    delete module_loader;
}

