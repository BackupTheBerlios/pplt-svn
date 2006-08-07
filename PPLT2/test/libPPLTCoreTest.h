#ifndef LIBPPLTCORETEST_H
#define LIBPPLTCORETEST_H

#include "libppltcore/ppltcore.h"
#include "ppltTest.h"
#include "CoreModuleTest.h"

namespace PPLTCore{
namespace Test{
    
    class libPPLTCoreTest: public PPLTTest::cTest{ 
        
        TEST_DECLARATION
            TEST_ADD(test_ModuleFinding);
            TEST_ADD(test_ModuleLoading);
            TEST_ADD_SUB(CoreModuleTest);
        TEST_DECLARATION_END
 
        private:
            void setup();
            
            void test_ModuleFinding( void );
            void test_ModuleLoading( void );
            
            void teardown();
            
        private:
            PPLTCore::soModuleLoader    *module_loader;
    };           

}}

#endif
