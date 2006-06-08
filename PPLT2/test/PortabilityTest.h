#ifndef PORTABILITYTEST_H
#define PORTABILITYTEST_H


#include "libPPLTCoreTest.h"
#include "libppltcore/ppltcore.h"


namespace PPLTCore{
    namespace Test{


    class PortabilityTest : public libPPLTCoreTest{ 
        CPPUNIT_TEST_SUB_SUITE(PortabilityTest, libPPLTCoreTest);

        CPPUNIT_TEST(test_NormalizePath);
        CPPUNIT_TEST(test_ExtendPath);

        CPPUNIT_TEST_SUITE_END();

        public:
            void setUp( void );
            void tearDown( void );

        protected:
            void test_NormalizePath();
            void test_ExtendPath();

        private:
            std::string     cwd;
    };


    // END OF NAMESPACES:
    }
}


#endif

