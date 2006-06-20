#ifndef LIBPPLTCORETEST_H
#define LIBPPLTCORETEST_H

#include "libppltcore/ppltcore.h"

#include <cppunit/TestFixture.h>
#include <cppunit/extensions/HelperMacros.h>
#include <cppunit/ui/text/TestRunner.h>
#include <cppunit/BriefTestProgressListener.h>
#include <cppunit/extensions/TestFactoryRegistry.h>
#include <cppunit/TestResult.h>
#include <cppunit/TestResultCollector.h>
#include <cppunit/TestRunner.h>
#include <cppunit/TextOutputter.h>


namespace PPLTCore{
namespace Test{
    
    class libPPLTCoreTest: public CPPUNIT_NS::TestFixture{ 
        
        CPPUNIT_TEST_SUITE(libPPLTCoreTest);
        CPPUNIT_TEST_SUITE_END();
        
        public:
            void setUp( void );
            void tearDown( void );

    };           

    }
}

#endif
