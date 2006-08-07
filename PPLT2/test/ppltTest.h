/**\file ppltTest.h PPLT Unit Test!
 * This 200 lines-file contains the complete PPLT unit test. */

#ifndef PPLT_TEST_H
#define PPLT_TEST_H

#include <iostream>
#include <streambuf>
#include <sstream>
#include <fstream>
#include <typeinfo>
#include <cxxabi.h>
#include <time.h>


/** This macro starts the declaration of the test routines and sub tests. 
 * This macro indicates, that the test declarations are following. These 
 * declarations have to be closed by a TEST_DECLARATION_END macro. Between 
 * these two macros you can used TEST_ADD(test_method) to declare a test
 * method or TEST_ADD_SUB(class) to declare a sub test. 
 *\code
class mySubTest: public PPLTTest::cTest{
    TEST_DECLARARION
        TEST_ADD(subtest_method);
    TEST_DECLARATION_END
    
    private:
        void setup( void );
        void subtest_method( void );
        void teardown( void );
};

class myTest: public PPLTTest::cTest{
    TEST_DECLARATION
        TEST_ADD(test_method);
        TEST_ADD_SUB(mySubTest);
    TEST_DECLARAION_END

    private:
        void setup( void );
        void teardown( void );
        void test_method( void );
};
\endcode
 * This example shows how to define a test with a sub test. 
 * \note The subtest will only be executed if the previous tests are 
 * succeeded. */
#define TEST_DECLARATION        public: void _run( void ){\
                                    PPLTTest::cTestContext *_ctx = PPLTTest::cTestContext::factory();\
                                    try{ setup(); }\
                                    catch(...){\
                                        std::cout << "ERROR while setup test " << PPLTTest::demangle_symbol(typeid(*this).name()) << std::endl;\
                                        return;\
                                    }


/** This macro defined the end of a test declaration.
 * @see TEST_DECLARATION */
#define TEST_DECLARATION_END        try{ teardown();}\
                                    catch(...){\
                                        std::cout << "Error while teardown() test " << PPLTTest::demangle_symbol(typeid(*this).name()) << std::endl;\
                                    }\
                                }

#define TEST_ADD(fct)           do{\
                                    double _used_time;\
                                    _ctx->addtest();\
                                    try{\
                                        std::cout << "RUN  " << PPLTTest::demangle_symbol(typeid(*this).name()) << "::" << #fct << "() ... ";\
                                        _ctx->startTimer();\
                                        fct();\
                                        _used_time = _ctx->stopTimer();\
                                        std::cout << "OK in " << _used_time << " ms\n";\
                                    }catch(PPLTTest::eFail e){\
                                        _ctx->stopTimer();\
                                        _ctx->addfail();\
                                        std::cout << "FAIL: " << e.getReason() << std::endl;\
                                        this->_d_pplttest_failed = true;\
                                    }catch(PPLTTest::eError e){\
                                        _ctx->stopTimer();\
                                        _ctx->adderror();\
                                        std::cout << "ERROR: " << e.getReason() << std::endl;\
                                        this->_d_pplttest_failed = true;\
                                    } catch(...){\
                                        _ctx->stopTimer();\
                                        _ctx->adderror();\
                                        std::cout << "EXCEPTION in "<< __FILE__ << " line " << __LINE__ << std::endl;\
                                        this->_d_pplttest_failed = true;\
                                    }\
                                }while(0);                                        


#define TEST_ADD_SUB(cls)       if(!_d_pplttest_failed){\
                                    cls *_sub_test = new cls();\
                                    _sub_test->_run();\
                                    delete _sub_test;\
                                }else{\
                                    cls *_sub_test = new cls();\
                                    std::cout << "SKIP subtest " << PPLTTest::demangle_symbol(typeid(*_sub_test).name()) << " because a previous test failed!\n";\
                                    delete _sub_test;\
                                }                                    


#define TEST_FAIL(reason)       do{\
                                    std::ostringstream buff;\
                                    buff << reason << " In " << __PRETTY_FUNCTION__ << " ["<< __FILE__ << "] at line " << __LINE__; \
                                    throw PPLTTest::eFail(buff.str());\
                                }while(0);

#define TEST_ERROR(reason)      do{\
                                    std::ostringstream buff;\
                                    buff << reason << " In " << __PRETTY_FUNCTION__ << " ["<< __FILE__ << "] at line " << __LINE__; \
                                    throw PPLTTest::eError(buff.str());\
                                }while(0);


#define START_TEST(test_cls)    do{\
                                    PPLTTest::cTestContext *_ctx = PPLTTest::cTestContext::factory();\
                                    _ctx->reset_counters();\
                                    std::cout << "----------------------\n";\
                                    test_cls    *_test = new test_cls();\
                                    _test->_run();\
                                    std::cout << "--- Tests finished ---\n";\
                                    std::cout << _ctx->results() << std::endl;\
                                }while(0);                                    


#define ASSUME_TRUE(expr)               try{ if(!(expr)){ TEST_FAIL(#expr); } }catch(PPLTTest::eFail){ throw; }catch(...){ TEST_ERROR("An exception was raised!"); }
#define ASSUME_FALSE(expr)              try{ if(expr){ TEST_FAIL(#expr); } }catch(PPLTTest::eFail){ throw; }catch(...){ TEST_ERROR("An exception was raised!"); }
#define ASSUME_NO_THROW(stuff)          try{ stuff; }catch(...){ TEST_FAIL("An exception was raised by " << #stuff ); }
#define ASSUME_THROW(stuff, exception)  try{ stuff; TEST_FAIL("Assumed exception was not thrown by " << #stuff);}catch(exception){}catch(...){ TEST_FAIL("Assumed exception was not thrown but an other one by "<<#stuff); }




namespace PPLTTest{

    std::string demangle_symbol(const char *name);

    class eFail{
        private: std::string d_reason;
        public: 
            eFail(std::string reason);
            std::string getReason();
    };

    class eError{
        private: std::string d_reason;
        public: 
            eError(std::string reason);
            std::string getReason();
    };


    class cTestContext{
        private:
            int                     d_test_run;
            int                     d_test_failed;
            int                     d_test_error;
            static cTestContext    *d_singleton_instance;
            clock_t                 d_start_time;

        public:
            static cTestContext *factory( void );

        public:           
            cTestContext( void );

            void reset_counters( void );

            std::string results( void );
            void addtest( void );
            void addfail( void );
            void adderror( void );

            void startTimer( void );
            double stopTimer( void );
    };


    class cTest{
        protected:
            bool    _d_pplttest_failed;

        public:
            cTest( void );
            virtual ~cTest();

            virtual void setup( void );
            virtual void teardown( void );
            virtual void _run( void ) = 0;
    };   
}

#endif

