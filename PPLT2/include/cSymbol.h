#ifndef PPLT_CSYMBOL_H
#define PPLT_CSYMBOL_H

#include "Logging.h"
#include "Exceptions.h"
#include "cDisposable.h"
#include "cObject.h"
#include "cConnection.h"

/**\file cSymbol.h
 * This file contains the declaration of the basic Symbol class. 
 * CHANGELOG: */
namespace PPLTCore{

    typedef void (*tSymbolCallback)(class cSymbol *);

    /**Basic class for Symbols.
     * This class defines the methods for the basic class also
     * it provides the generic algorithms to handle callbacks.
     * Therefor there is a interface definition of a callback 
     * handler.	*/
    class cSymbol: public cDisposable, public cObject{
    	private:
        	std::list<tSymbolCallback>  d_callbacks;

        protected:
            cConnection     *d_parent_connection;

        public:
            cSymbol(cModule *parent, std::string addr);
			~cSymbol();

            // may be it is better to hide this function to
            // all but friend classes
			void data_notify();

			int addHandler(void (*function)(cSymbol*));
			void remHandler(int );
    };

}

#endif
