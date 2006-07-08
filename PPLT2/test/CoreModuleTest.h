#ifndef COREMODULETEST_H
#define COREMODULETEST_H


#include "libPPLTCoreTest.h"
#include "libppltcore/ppltcore.h"


namespace PPLTCore{
    namespace Test{


    class CoreModuleTest : public libPPLTCoreTest{ 
        CPPUNIT_TEST_SUB_SUITE(CoreModuleTest, libPPLTCoreTest);

        CPPUNIT_TEST(test_RandomModule);
        CPPUNIT_TEST(test_LoopbackModule);
        CPPUNIT_TEST(test_HexifierModule);
        CPPUNIT_TEST(test_HexDumpModule);

        CPPUNIT_TEST_SUITE_END();

        private:
            soModuleLoader       d_module_loader;

        public:
            void setUp( void );
            void tearDown( void );

        protected:
            void test_RandomModule();
            void test_LoopbackModule();
            void test_HexifierModule();
            void test_HexDumpModule();
    };


    }
}


#endif

