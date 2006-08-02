#include "libPPLTCoreTest.h"

using namespace PPLTCore;
using namespace PPLTCore::Test;

#define PACKAGEPATH     "../plugins/libppltcoremodules.so"

void libPPLTCoreTest::test_RandomModule( void ){
    cModule             *rand;
    cIntegerConnection  *con;
    int                 tmp_int;
    std::string         tmp_str;


    // Try to load random module from std modules package:
    QASSERT_NOTHROW( 
        rand = module_loader->load(PACKAGEPATH,
                                   "RandomModuleFactory", 
                                   tModuleParameters())
    );

    // Try to connect to module:
    QASSERT_NOTHROW( con = dynamic_cast<cIntegerConnection *>(rand->connect("int")) );        

    // Try to get value:
    QASSERT_NOTHROW( tmp_int = con->get() );

    //check value range:
    QVERIFY( 0 <= tmp_int and RAND_MAX >= tmp_int ); 

    delete con;
    QASSERT_NOTHROW(module_loader->unload(rand));
}


void libPPLTCoreTest::test_LoopbackModule( void ){
    cModule             *loop;
    cStreamConnection   *con1, *con2;
    unsigned int        ret_len;
    std::string         buffer;

    // try to load module:
    QASSERT_NOTHROW(
        loop = module_loader->load(PACKAGEPATH,
                                   "LoopbackModuleFactory",
                                   tModuleParameters())
    );

    // try to create connections:
    QASSERT_NOTHROW( con1 = dynamic_cast<cStreamConnection *>(loop->connect("aaa")) );
    QASSERT_NOTHROW( con2 = dynamic_cast<cStreamConnection *>(loop->connect("aaa")) );
    QVERIFY( 0 != con1 and 0 != con2);

    // disable events:
    con1->events_enabled(false);
    con2->events_enabled(false);

    // try data correctness;
    QASSERT_NOTHROW( ret_len = con1->write("Hello world!", 12) );
    QVERIFY((unsigned int)12 == ret_len);
    QASSERT_NOTHROW( buffer = con2->read(12) );
    QVERIFY(std::string("Hello world!") == buffer);

    // try the behavior of the data stream:
    QASSERT_NOTHROW( ret_len = con1->write("a", 1) );
    QVERIFY((unsigned int)1 == ret_len);
    QASSERT_NOTHROW( ret_len = con1->write("b", 1) );
    QVERIFY((unsigned int)1 == ret_len);
    QASSERT_NOTHROW( buffer = con2->read(1) );
    QVERIFY(std::string("a") == buffer);
    QASSERT_NOTHROW( buffer = con2->read(1) );
    QVERIFY(std::string("b") == buffer);

    // try connection address counting:
    delete con2;
    QASSERT_NOTHROW( con2 = dynamic_cast<cStreamConnection *>(loop->connect("aaa")) );
    QVERIFY( 0 != con2);
    QASSERT_THROW( loop->connect("aaa"), ItemBusy );

    // try exception type:
    delete con2;
    QASSERT_THROW( con1->write("abc",3), ModuleError );
    
    // clean up
    delete con1;
    QASSERT_NOTHROW( module_loader->unload(loop) );
}



void libPPLTCoreTest::test_HexifierModule( void ){
    cModule             *loop, *hex;
    cStreamConnection   *con1, *con2;
    unsigned int        ret_len;
    std::string         buffer;

    QASSERT_NOTHROW( 
        loop = module_loader->load(PACKAGEPATH,
                                   "LoopbackModuleFactory",
                                   tModuleParameters())
    );

    QASSERT_NOTHROW(
        hex = module_loader->load(PACKAGEPATH,
                                  "HexifierModuleFactory", loop, "aaa",
                                  tModuleParameters())
    );

    QASSERT_NOTHROW(
        con1 = dynamic_cast<cStreamConnection *>(loop->connect("aaa"))
    );
    QASSERT_NOTHROW(
        con2 = dynamic_cast<cStreamConnection *>(hex->connect(""))
    );
    QVERIFY( 0 != con1 and 0 != con2 );

    con1->events_enabled(false);
    con2->events_enabled(false);
 
    QASSERT_NOTHROW( ret_len = con1->write("abc", 3) );
    QVERIFY((unsigned int)3 == ret_len);
    QASSERT_NOTHROW( buffer = con2->read(6) );
    QVERIFY(std::string("616263") == buffer);

    QASSERT_NOTHROW( ret_len = con2->write("616263", 6) );
    QVERIFY( (unsigned int)6 == ret_len );
    QASSERT_NOTHROW( buffer = con1->read(3) );
    QVERIFY( std::string("abc") == buffer );

    QASSERT_THROW( con2->write("111",3), ModuleError );

    // CLEAN UP:
    delete con1;
    delete con2;
    QASSERT_NOTHROW( module_loader->unload(hex) );
    QASSERT_NOTHROW( module_loader->unload(loop) );
}



void libPPLTCoreTest::test_HexDumpModule( void ){
    cModule             *hex, *loop;
    cStreamConnection   *con1, *con2;
    cSequenceConnection *dump;
    unsigned int        len;
    std::string         buffer;


    QASSERT_NOTHROW( 
        loop = module_loader->load(PACKAGEPATH,
                                   "LoopbackModuleFactory",
                                   tModuleParameters() )
    );

    QASSERT_NOTHROW( 
        hex = module_loader->load(PACKAGEPATH,
                                  "HexDumpModuleFactory", loop, "aaa",
                                  tModuleParameters())
    );

    QASSERT_NOTHROW( con1 = dynamic_cast<cStreamConnection *>(loop->connect("aaa")));
    QASSERT_NOTHROW( con2 = dynamic_cast<cStreamConnection *>(hex->connect("")));
    QASSERT_NOTHROW( dump = dynamic_cast<cSequenceConnection *>(hex->connect("dump")));
    QVERIFY( 0!=con1 and 0!=con2 and 0!=dump);

    con1->events_enabled(false);
    con2->events_enabled(false);
    dump->events_enabled(false);


    QASSERT_NOTHROW( len = con2->write("hello world",11) );
    QVERIFY( (unsigned int)11 == len );
    QASSERT_NOTHROW( buffer = con1->read(11) );
    QVERIFY( std::string("hello world") == buffer );

    QASSERT_NOTHROW( len = con1->write("hello world",11) );
    QVERIFY( (unsigned int)11 == len );
    QASSERT_NOTHROW( buffer = con2->read(11) );
    QVERIFY( (unsigned int)11 == buffer.length() );
    QVERIFY( std::string("hello world") == buffer );

    //cleanup:
    delete dump;
    delete con1;
    delete con2;
    QASSERT_NOTHROW( module_loader->unload(hex) );
    QASSERT_NOTHROW( module_loader->unload(loop) );
}



