#ifndef LIBPPLTCORETEST_H
#define LIBPPLTCORETEST_H

#include "libppltcore/ppltcore.h"
#include <QtTest/QtTest>

#define QASSERT_THROW( statement, exception)    try{ statement; }catch(exception){}catch(...){ QFAIL("Exception was throwed!"); }
#define QASSERT_NOTHROW( statement)             try{ statement; }catch(...){ QFAIL("A unexpacted exception was throwed!"); }

namespace PPLTCore{
namespace Test{
    
    class libPPLTCoreTest: public QObject{ 
        Q_OBJECT;
        
        private slots:
            void initTestCase( void );
            
            void test_ModuleFinding( void );
            void test_ModuleLoading( void );
            
            void test_RandomModule();
            void test_LoopbackModule();
            void test_HexifierModule();
            void test_HexDumpModule();

            void cleanupTestCase( void );

        private:
            PPLTCore::soModuleLoader    *module_loader;
    };           

}}

#endif
