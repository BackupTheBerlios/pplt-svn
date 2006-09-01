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



void libPPLTCoreTest::test_Events( void ){
    cModule             *loop;
    cStreamConnection   *con1, *con2;


    CORELOG_DEBUG("--- START EVENTTEST ---");
    ASSUME_NO_THROW(
        loop = module_loader->load("../plugins/libppltcoremodules.so", 
                                   "LoopbackModuleFactory", tModuleParameters());
    );

    con1 = dynamic_cast<cStreamConnection *>(loop->connect("aaa"));
    con2 = dynamic_cast<cStreamConnection *>(loop->connect("aaa"));
   
    ASSUME_NO_THROW( con1->events_enabled(false) );

    ASSUME_NO_THROW( con2->write("123",3) );
    ASSUME_TRUE( std::string("123") == con1->read(3) );

    ASSUME_NO_THROW( con1->events_enabled(true) );

    sleep(3);

    ASSUME_NO_THROW( con1->events_enabled(false) );
    ASSUME_NO_THROW( con2->write("123",3) );
    ASSUME_NO_THROW( con1->events_enabled(true) );

    sleep(3);

    ASSUME_NO_THROW( delete con1 );
    ASSUME_NO_THROW( delete con2 );

    ASSUME_NO_THROW( module_loader->unload(loop) );
}
