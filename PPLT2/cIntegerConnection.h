#ifndef PPLT_CINTEGER_CONNECTION
#define PPLT_CINTEGER_CONNECTION

#include "iIntegerModule.h"
#include "cValueConnection.h"

namespace PPLTCore{

    /** A conection to a module that implements IntegerModule.
     * This class extend the cValueConnection class to implement
     * a connection to a module that provies integer values.
     * This class can also (like other connection classes) connect
     * two
     */
     // FIXME : complete!
    class cIntegerConnection : public cValueConnection{
        private:
            int d_cache_value;

        public:
            cIntegerConnection(cModule *parent, cDisposable *child=0);

            int get();
            void set(int);

            int Integer();
            void Integer(int);

            std::string String();
            void String(std::string);
    };

}

#endif
