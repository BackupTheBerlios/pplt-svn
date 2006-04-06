#ifndef PPLT_CINTEGER_CONNECTION
#define PPLT_CINTEGER_CONNECTION

#include "iIntegerModule.h"
#include "cValueConnection.h"

namespace PPLTCore{

    /** A conection to a module that implements IntegerModule.
     * This class extend the cValueConnection class to implement
     * a connection to a module that provies integer values.
     * This class can also (like other connection classes) connect
     * two modules. The child module have to know how to handle
     * integer connections. A module can check on construction what
     * kind of connection it got.
     */
    class cIntegerConnection : public cValueConnection{
        private:
            int d_cache_value;

        public:
            /** Constructor
            * This constructor has one needed and one optional
            * parameter. The parameter parent defined the parent
            * module the connection will be etablished to. The
            * optional parameter child defines the child module.*/
            cIntegerConnection(cModule *parent, cDisposable *child=0);

            /** Push() callback.
            * This callback can be used by the parent module to
            * notify the child about ney data in the conenction
            * buffer. The data of the parameter value will be stored
            * into a buffer and the next get() request will be
            * satisfied by this value instead of reading from the
            * parent. Also this method call the data_notify() method
            * of the child. */
            void push(int value);

            /** Returns the cached value or one obtained from parent. */
            int get();
            /** Sends the value to the parent and update cache. */
            void set(int);

            /** Get the value as an integer.
            * This method calls get() and tryes to convert the value
            * into an integer. In this case it does quiet nothing.  */
            int Integer();
            /** Set the value from an integer.
            * This method tryes to convert the given value to an
            * integer and then set the value by calling the set()
            * method. In this case it only calles set() */
            void Integer(int);

            /** Get the value as an string.
            * This method calls get() and tryes to convert the value
            * into a string. */
            std::string String();
            /** Set the value from a string.
            * This method tryes to convert the string into a integer
            * and then call set() to set this value. */
            void String(std::string);
    };

}

#endif
