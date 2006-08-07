#include "libPPLTCoreTest.h"

using namespace PPLTCore;
using namespace PPLTCore::Test;

#define PACKAGEPATH     "../plugins/libppltcoremodules.so"

void CoreModuleTest::setup( void ){
    module_loader = new soModuleLoader();
}

void CoreModuleTest::teardown( void ){
    delete module_loader;
}



void CoreModuleTest::test_RandomModule( void ){
    cModule             *rand;
    cIntegerConnection  *con;
    int                 tmp_int;
    std::string         tmp_str;


    // Try to load random module from std modules package:
    ASSUME_NO_THROW( 
        rand = module_loader->load(PACKAGEPATH,
                                   "RandomModuleFactory", 
                                   tModuleParameters());
    );

    // Try to connect to module:
    ASSUME_NO_THROW( con = dynamic_cast<cIntegerConnection *>(rand->connect("int")) );        

    // Try to get value:
    ASSUME_NO_THROW( tmp_int = con->get() );

    //check value range:
    ASSUME_TRUE( 0 <= tmp_int and RAND_MAX >= tmp_int ); 

    delete con;
    ASSUME_NO_THROW(module_loader->unload(rand));
}


void CoreModuleTest::test_LoopbackModule( void ){
    cModule             *loop;
    cStreamConnection   *con1, *con2;
    unsigned int        ret_len;
    std::string         buffer;

    // try to load module:
    ASSUME_NO_THROW(
        loop = module_loader->load(PACKAGEPATH,
                                   "LoopbackModuleFactory",
                                   tModuleParameters())
    );

    // try to create connections:
    ASSUME_NO_THROW( con1 = dynamic_cast<cStreamConnection *>(loop->connect("aaa")) );
    ASSUME_NO_THROW( con2 = dynamic_cast<cStreamConnection *>(loop->connect("aaa")) );
    ASSUME_TRUE( 0 != con1 and 0 != con2);

    // disable events:
    con1->events_enabled(false);
    con2->events_enabled(false);

    // try data correctness;
    ASSUME_NO_THROW( ret_len = con1->write("Hello world!", 12) );
    ASSUME_TRUE((unsigned int)12 == ret_len);
    ASSUME_NO_THROW( buffer = con2->read(12) );
    ASSUME_TRUE(std::string("Hello world!") == buffer);

    // try the behavior of the data stream:
    ASSUME_NO_THROW( ret_len = con1->write("a", 1) );
    ASSUME_TRUE((unsigned int)1 == ret_len);
    ASSUME_NO_THROW( ret_len = con1->write("b", 1) );
    ASSUME_TRUE((unsigned int)1 == ret_len);
    ASSUME_NO_THROW( buffer = con2->read(1) );
    ASSUME_TRUE(std::string("a") == buffer);
    ASSUME_NO_THROW( buffer = con2->read(1) );
    ASSUME_TRUE(std::string("b") == buffer);

    // try connection address counting:
    delete con2;
    ASSUME_THROW( con1->write("abc",3), ModuleError);
    ASSUME_NO_THROW( con2 = dynamic_cast<cStreamConnection *>(loop->connect("aaa")) );
    ASSUME_FALSE( 0 == con2);
    ASSUME_THROW( loop->connect("aaa"), ItemBusy );

    // try exception type:
    delete con2;
    ASSUME_THROW( con1->write("abc",3), ModuleError );
    
    // clean up
    delete con1;
    ASSUME_NO_THROW( module_loader->unload(loop) );
}



void CoreModuleTest::test_HexifierModule( void ){
    cModule             *loop, *hex;
    cStreamConnection   *con1, *con2;
    unsigned int        ret_len;
    std::string         buffer;

    ASSUME_NO_THROW( 
        loop = module_loader->load(PACKAGEPATH,
                                   "LoopbackModuleFactory",
                                   tModuleParameters())
    );

    ASSUME_NO_THROW(
        hex = module_loader->load(PACKAGEPATH,
                                  "HexifierModuleFactory", loop, "aaa",
                                  tModuleParameters())
    );

    ASSUME_NO_THROW(
        con1 = dynamic_cast<cStreamConnection *>(loop->connect("aaa"))
    );
    ASSUME_NO_THROW(
        con2 = dynamic_cast<cStreamConnection *>(hex->connect(""))
    );
    ASSUME_TRUE( 0 != con1 and 0 != con2 );

    con1->events_enabled(false);
    con2->events_enabled(false);
 
    ASSUME_NO_THROW( ret_len = con1->write("abc", 3) );
    ASSUME_TRUE((unsigned int)3 == ret_len);
    ASSUME_NO_THROW( buffer = con2->read(6) );
    ASSUME_TRUE(std::string("616263") == buffer);

    ASSUME_NO_THROW( ret_len = con2->write("616263", 6) );
    ASSUME_TRUE( (unsigned int)6 == ret_len );
    ASSUME_NO_THROW( buffer = con1->read(3) );
    ASSUME_TRUE( std::string("abc") == buffer );

    ASSUME_THROW( con2->write("111",3), ModuleError );

    // CLEAN UP:
    delete con1;
    delete con2;
    ASSUME_NO_THROW( module_loader->unload(hex) );
    ASSUME_NO_THROW( module_loader->unload(loop) );
}



void CoreModuleTest::test_HexDumpModule( void ){
    cModule             *hex, *loop;
    cStreamConnection   *con1, *con2;
    cSequenceConnection *dump;
    unsigned int        len;
    std::string         buffer;


    ASSUME_NO_THROW( 
        loop = module_loader->load(PACKAGEPATH,
                                   "LoopbackModuleFactory",
                                   tModuleParameters() )
    );

    ASSUME_NO_THROW( 
        hex = module_loader->load(PACKAGEPATH,
                                  "HexDumpModuleFactory", loop, "aaa",
                                  tModuleParameters())
    );

    ASSUME_NO_THROW( con1 = dynamic_cast<cStreamConnection *>(loop->connect("aaa")));
    ASSUME_NO_THROW( con2 = dynamic_cast<cStreamConnection *>(hex->connect("")));
    ASSUME_NO_THROW( dump = dynamic_cast<cSequenceConnection *>(hex->connect("dump")));
    ASSUME_TRUE( 0!=con1 and 0!=con2 and 0!=dump);

    con1->events_enabled(false);
    con2->events_enabled(false);
    dump->events_enabled(false);


    ASSUME_NO_THROW( len = con2->write("hello world",11) );
    ASSUME_TRUE( (unsigned int)11 == len );
    ASSUME_NO_THROW( buffer = con1->read(11) );
    ASSUME_TRUE( std::string("hello world") == buffer );

    ASSUME_NO_THROW( len = con1->write("hello world",11) );
    ASSUME_TRUE( (unsigned int)11 == len );
    ASSUME_NO_THROW( buffer = con2->read(11) );
    ASSUME_TRUE( (unsigned int)11 == buffer.length() );
    ASSUME_TRUE( std::string("hello world") == buffer );

    //cleanup:
    delete dump;
    delete con1;
    delete con2;
    ASSUME_NO_THROW( module_loader->unload(hex) );
    ASSUME_NO_THROW( module_loader->unload(loop) );
}



