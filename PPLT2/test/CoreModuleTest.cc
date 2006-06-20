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

}

