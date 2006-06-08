#ifndef SOMODULELOADERTEST_H
#define SOMODULELOADERTEST_H

#include "libPPLTCoreTest.h"
#include "libppltcore/ppltcore.h"

namespace PPLTCore{
    namespace Test{

    class  soModuleLoaderTest: public libPPLTCoreTest{ 
        CPPUNIT_TEST_SUB_SUITE(soModuleLoaderTest, libPPLTCoreTest);
        
        CPPUNIT_TEST(test_ModuleFinding);
        CPPUNIT_TEST(test_ModuleLoading);
        CPPUNIT_TEST_SUITE_END();
    
        public:
            void setUp( void );
            void tearDown( void );
    
        protected:
            void test_ModuleFinding(void);
            void test_ModuleLoading(void);

        private:
            PPLTCore::soModuleLoader      *module_loader;
    };


    }
}

#endif

