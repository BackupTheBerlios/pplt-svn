#include "libPPLTCoreTest.h"

namespace PPLTCore{
namespace Test{

    class CoreModuleTest: public PPLTTest::cTest{
        
        TEST_DECLARATION
            TEST_ADD(test_RandomModule);
            TEST_ADD(test_LoopbackModule);
            TEST_ADD(test_HexifierModule);
            TEST_ADD(test_HexDumpModule);
        TEST_DECLARATION_END


        private:
            soModuleLoader      *module_loader;
            
            void test_RandomModule();
            void test_LoopbackModule();
            void test_HexifierModule();
            void test_HexDumpModule();
        
        public:
            void setup( void );
            void teardown( void );

    };

}
}

