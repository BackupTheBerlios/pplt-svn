#include "CoreModuleTest.h"

using namespace PPLTCore;
using namespace PPLTCore::Test;


CPPUNIT_TEST_SUITE_REGISTRATION(CoreModuleTest);


void CoreModuleTest::setUp( void ){ }



void CoreModuleTest::tearDown( void ){ }



void CoreModuleTest::test_RandomModule( void ){
    cModule             *rand;
    cIntegerConnection  *con;
    int                 tmp_int;
    std::string         tmp_str;


    // Try to load random module from std modules package:
    CPPUNIT_ASSERT_NO_THROW( 
        rand = d_module_loader.load("../plugins/ppltstdmodules.so", 
                                    "RandomModuleFactory", 
                                    tModuleParameters()) 
    );

    // Try to connect to module:
    CPPUNIT_ASSERT_NO_THROW( con = dynamic_cast<cIntegerConnection *>(rand->connect("int")) );        

    // Try to get value:
    CPPUNIT_ASSERT_NO_THROW( tmp_int = con->get() );

    //check value range:
    CPPUNIT_ASSERT( 0 <= tmp_int and RAND_MAX >= tmp_int ); 

    delete con;
    CPPUNIT_ASSERT_NO_THROW(d_module_loader.unload(rand));
}


void CoreModuleTest::test_LoopbackModule( void ){
    cModule             *loop;
    cStreamConnection   *con1, *con2;
    unsigned int        ret_len;
    std::string         buffer;

    // try to load module:
    CPPUNIT_ASSERT_NO_THROW(
        loop = d_module_loader.load("../plugins/ppltstdmodules.so",
                                    "LoopbackModuleFactory",
                                    tModuleParameters())
    );

    // try to create connections:
    CPPUNIT_ASSERT_NO_THROW( con1 = dynamic_cast<cStreamConnection *>(loop->connect("aaa")) );
    CPPUNIT_ASSERT_NO_THROW( con2 = dynamic_cast<cStreamConnection *>(loop->connect("aaa")) );
    CPPUNIT_ASSERT( 0 != con1 and 0 != con2);

    // disable events:
    con1->events_enabled(false);
    con2->events_enabled(false);

    // try data correctness;
    CPPUNIT_ASSERT_NO_THROW( ret_len = con1->write("Hello world!", 12) );
    CPPUNIT_ASSERT_EQUAL((unsigned int)12, ret_len);
    CPPUNIT_ASSERT_NO_THROW( buffer = con2->read(12) );
    CPPUNIT_ASSERT_EQUAL(std::string("Hello world!"), buffer);

    // try the behavior of the data stream:
    CPPUNIT_ASSERT_NO_THROW( ret_len = con1->write("a", 1) );
    CPPUNIT_ASSERT_EQUAL((unsigned int)1, ret_len);
    CPPUNIT_ASSERT_NO_THROW( ret_len = con1->write("b", 1) );
    CPPUNIT_ASSERT_EQUAL((unsigned int)1, ret_len);
    CPPUNIT_ASSERT_NO_THROW( buffer = con2->read(1) );
    CPPUNIT_ASSERT_EQUAL(std::string("a"), buffer);
    CPPUNIT_ASSERT_NO_THROW( buffer = con2->read(1) );
    CPPUNIT_ASSERT_EQUAL(std::string("b"), buffer);

    // try connection address counting:
    delete con2;
    CPPUNIT_ASSERT_NO_THROW( con2 = dynamic_cast<cStreamConnection *>(loop->connect("aaa")) );
    CPPUNIT_ASSERT( 0 != con2);
    CPPUNIT_ASSERT_THROW( loop->connect("aaa"), ItemBusy );

    // try exception type:
    delete con2;
    CPPUNIT_ASSERT_THROW( con1->write("abc",3), ModuleError );
    
    // clean up
    delete con1;
    CPPUNIT_ASSERT_NO_THROW( d_module_loader.unload(loop) );
}



void CoreModuleTest::test_HexifierModule( void ){
    cModule             *loop, *hex;
    cStreamConnection   *con1, *con2;
    unsigned int        ret_len;
    std::string         buffer;

    CPPUNIT_ASSERT_NO_THROW( 
        loop = d_module_loader.load("../plugins/ppltstdmodules.so",
                                    "LoopbackModuleFactory",
                                    tModuleParameters())
    );

    CPPUNIT_ASSERT_NO_THROW(
        hex = d_module_loader.load("../plugins/ppltstdmodules.so",
                                   "HexifierModuleFactory", loop, "aaa",
                                   tModuleParameters())
    );

    CPPUNIT_ASSERT_NO_THROW(
        con1 = dynamic_cast<cStreamConnection *>(loop->connect("aaa"))
    );
    CPPUNIT_ASSERT_NO_THROW(
        con2 = dynamic_cast<cStreamConnection *>(hex->connect(""))
    );
    CPPUNIT_ASSERT( 0 != con1 and 0 != con2 );

    con1->events_enabled(false);
    con2->events_enabled(false);
 
    CPPUNIT_ASSERT_NO_THROW( ret_len = con1->write("abc", 3) );
    CPPUNIT_ASSERT_EQUAL((unsigned int)3, ret_len);
    CPPUNIT_ASSERT_NO_THROW( buffer = con2->read(6) );
    CPPUNIT_ASSERT_EQUAL(std::string("616263"), buffer);

    CPPUNIT_ASSERT_NO_THROW( ret_len = con2->write("616263", 6) );
    CPPUNIT_ASSERT_EQUAL( (unsigned int)6, ret_len );
    CPPUNIT_ASSERT_NO_THROW( buffer = con1->read(3) );
    CPPUNIT_ASSERT_EQUAL( std::string("abc"), buffer );

    CPPUNIT_ASSERT_THROW( con2->write("111",3), ModuleError );

    // CLEAN UP:
    delete con1;
    delete con2;
    CPPUNIT_ASSERT_NO_THROW( d_module_loader.unload(hex) );
    CPPUNIT_ASSERT_NO_THROW( d_module_loader.unload(loop) );
}



void CoreModuleTest::test_HexDumpModule( void ){
    cModule             *hex, *loop;
    cStreamConnection   *con1, *con2;
    cSequenceConnection *dump;
    unsigned int        len;
    std::string         buffer;


    CPPUNIT_ASSERT_NO_THROW( 
        loop = d_module_loader.load("../plugins/ppltstdmodules.so",
                                    "LoopbackModuleFactory",
                                    tModuleParameters() )
    );

    CPPUNIT_ASSERT_NO_THROW( 
        hex = d_module_loader.load("../plugins/ppltstdmodules.so",
                                   "HexDumpModuleFactory", loop, "aaa",
                                   tModuleParameters())
    );

    CPPUNIT_ASSERT_NO_THROW( con1 = dynamic_cast<cStreamConnection *>(loop->connect("aaa")));
    CPPUNIT_ASSERT_NO_THROW( con2 = dynamic_cast<cStreamConnection *>(hex->connect("")));
    CPPUNIT_ASSERT_NO_THROW( dump = dynamic_cast<cSequenceConnection *>(hex->connect("dump")));
    CPPUNIT_ASSERT( 0!=con1 and 0!=con2 and 0!=dump);

    con1->events_enabled(false);
    con2->events_enabled(false);
    dump->events_enabled(false);


    CPPUNIT_ASSERT_NO_THROW( len = con2->write("hello world",11) );
    CPPUNIT_ASSERT_EQUAL( (unsigned int)11, len );
    CPPUNIT_ASSERT_NO_THROW( buffer = con1->read(11) );
    CPPUNIT_ASSERT_EQUAL( std::string("hello world"), buffer );

    CPPUNIT_ASSERT_NO_THROW( len = con1->write("hello world",11) );
    CPPUNIT_ASSERT_EQUAL( (unsigned int)11, len );
    CPPUNIT_ASSERT_NO_THROW( buffer = con2->read(11) );
    CPPUNIT_ASSERT_EQUAL( (unsigned int)11, buffer.length() );
    CPPUNIT_ASSERT_EQUAL( std::string("hello world"), buffer );

    //cleanup:
    delete dump;
    delete con1;
    delete con2;
    CPPUNIT_ASSERT_NO_THROW( d_module_loader.unload(hex) );
    CPPUNIT_ASSERT_NO_THROW( d_module_loader.unload(loop) );
}



