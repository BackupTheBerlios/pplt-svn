#include "PortabilityTest.h"

using namespace PPLTCore;
using namespace PPLTCore::Test;


CPPUNIT_TEST_SUITE_REGISTRATION(PortabilityTest);




void PortabilityTest::setUp( void ){
    cwd = CWD();
}



void PortabilityTest::tearDown( void ){
}



void PortabilityTest::test_NormalizePath( void ){
    // check removal or double slashes:
    CPPUNIT_ASSERT(NormalizePath("//test1/filename.ext") == "/test1/filename.ext");

    // check handleing of single dots:
    CPPUNIT_ASSERT(NormalizePath("/test1/././filename.ext") == "/test1/filename.ext");

    // check handleing of two single dots:
    CPPUNIT_ASSERT(NormalizePath("/test/../test1/filename.ext") == "/test1/filename.ext");

    // check handleing of two dots at the beginning:
    CPPUNIT_ASSERT(NormalizePath("/../test1/filename.ext") == "/test1/filename.ext");

    // check all together:
    CPPUNIT_ASSERT(NormalizePath("//../test/.//..///test1/.//filename.ext") == "/test1/filename.ext");
}


void PortabilityTest::test_ExtendPath( void ){
    // check simple path extention
    CPPUNIT_ASSERT( ExtendPath("/with/test/path/to/file", "/base/path") == "/with/test/path/to/file");
    CPPUNIT_ASSERT( ExtendPath("with/test/path/to/file", "/base/path") == "/base/path/with/test/path/to/file");
    CPPUNIT_ASSERT( ExtendPath("../test/path", "/base/path") == "/base/test/path");
    CPPUNIT_ASSERT( ExtendPath(".") == cwd);
}    
