#include "libppltcore/ppltcore.h"

#include "libPPLTCoreTest.h"
#include "soModuleLoaderTest.h"


using namespace PPLTCore;
using namespace PPLTCore::Test;


int main(void){
    initLogging();

    CPPUNIT_NS::BriefTestProgressListener   testlistener;
    CPPUNIT_NS::TextTestRunner              testrunner;

    testrunner.addTest(CPPUNIT_NS::TestFactoryRegistry::getRegistry().makeTest());
    testrunner.eventManager().addListener(&testlistener);
    
    testrunner.setOutputter( dynamic_cast<CPPUNIT_NS::Outputter *>(new CPPUNIT_NS::TextOutputter(&testrunner.result(), std::cout)) );
    
    testrunner.run("");
    
    return 0;
}



