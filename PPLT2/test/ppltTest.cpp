#include "ppltTest.h"

using namespace PPLTTest;

std::string PPLTTest::demangle_symbol(const char *name){
    std::string ret;
    char        *buffer;
    int         status;
        
    buffer = abi::__cxa_demangle(name, 0, 0, &status);
    ret = buffer;
    free(buffer);
    return ret;
}





eFail::eFail(std::string reason){ d_reason = reason; }
std::string eFail::getReason( void ){ return d_reason; }


eError::eError(std::string reason){ d_reason = reason; }
std::string eError::getReason( void ){ return d_reason; }





cTestContext *cTestContext::d_singleton_instance = 0;
cTestContext *cTestContext::factory( void ){
    if(!cTestContext::d_singleton_instance)
        cTestContext::d_singleton_instance = new cTestContext();
    return cTestContext::d_singleton_instance;
}


cTestContext::cTestContext( void ){
    d_test_run = 0;
    d_test_failed = 0;
    d_test_error = 0;
}


void cTestContext::reset_counters( void ){
    d_test_run = 0; d_test_failed = 0; d_test_error = 0;
}


std::string cTestContext::results( void ){
    std::ostringstream buff;
    buff << "Tests run: "<<d_test_run<<"  failed: "<<d_test_failed<<"  errors: "<<d_test_error<<std::endl; 

    return buff.str();
}


void cTestContext::addtest( void ){ d_test_run++; }
void cTestContext::addfail( void ){ d_test_failed++; }
void cTestContext::adderror( void ){ d_test_error++; }

void cTestContext::startTimer( void ){ d_start_time = clock(); }

double cTestContext::stopTimer( void ){
    return (clock() - d_start_time)*1000.0/((double)CLOCKS_PER_SEC);
}




cTest::cTest( void ){ _d_pplttest_failed; }
cTest::~cTest( void ){ }
void cTest::setup( void ){ }
void cTest::teardown( void ){ }
