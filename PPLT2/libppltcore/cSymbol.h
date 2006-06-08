/***************************************************************************
 *            cSymbol.h
 *
 *  Sun Apr 23 01:12:34 2006
 *  Copyright  2006  Hannes Matuschek
 *  hmatuschek@gmx.net
 ****************************************************************************/

/*
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 */
 
#ifndef PPLT_CSYMBOL_H
#define PPLT_CSYMBOL_H

#include "Logging.h"
#include "Exceptions.h"
#include "cDisposable.h"
#include "cObject.h"
#include "cConnection.h"
#include "cValueConnection.h"
#include "cSequenceConnection.h"

/**\file cSymbol.h
 * This file contains the declaration of the basic Symbol class. 
 */
 
namespace PPLTCore{
    /** Interface for a callback function.
    * A callback handler should inplement this interface. */
    typedef void (*tSymbolCallback)(class cSymbol *);
        
    typedef void *(*tThreadCallback)(void *);
    
    /**Basic class for Symbols.
     * This class defines the methods for the basic class also
     * it provides the generic algorithms to handle callbacks.
     * Therefor there is a interface definition of a callback 
     * handler.	*/
    class cSymbol: public cDisposable, public cObject{
    	private:
        	std::map<int, tSymbolCallback>  d_callbacks;
            int new_callback_id();
        
        protected:
            /** Pointer to the connection.
            * This protected attribute holds the pointer to the connection
            * between the parent module and the symbol. */
            cConnection *d_parent_connection;
        
        public:
            /** Constructor. */
            cSymbol(cModule *parent, std::string addr);
            
            /** Destructor. */
			~cSymbol();

            // may be it is better to hide this function to
            // all but friend classes like modules...
            /** Callback.
            * This callback is used by the connection to the parent module
            * to notify the symbol about new data. This happens for example
            * if the value of the symbol has been changed by the system it 
            * self. */
			void data_notify();

            /** Adds a notify handler.
            * This method adds a handler to the list of functions, that are 
            * called if the symbol received a data_notify. Each handler will
            * be called into a new thread. (This may cange in future.)*/
			int addHandler(void (*function)(cSymbol*));
        
            /** Removes a handler.
            * This method removes the given handler from the list. */
			void remHandler(int );

            
            void reserve();
            void release();
            void autolock(bool al);
            bool autolock(void);
            
            
            /* Followin' methods are used to  define an interface of a "normal"
             * symbol: getting and setting values of different types. 
             * StreamSymbols are extended symbols inherit this class. */
            virtual void set(int value);
            virtual void set(double value);
            virtual void set(std::string value);

            virtual int getInt(void);
            virtual double getFloat(void);
            virtual std::string getSeq(void);
};

}

#endif
