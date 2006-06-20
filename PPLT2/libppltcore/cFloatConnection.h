/***************************************************************************
 *            cFloatConnection.h
 *
 *  Thu Apr 27 13:48:52 2006
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
 
#ifndef PPLT_CFLOATCONNECTION_H 
#define PPLT_CFLOATCONNECTION_H

#include "iFloatModule.h"
#include "cValueConnection.h"
#include "cDisposable.h"
#include "cModule.h"
#include "Exceptions.h"

/**\file cFloatConnection.h
 * This file contains the cFloatConnection class definition. */

namespace PPLTCore{
    
    /** Connection class for connections dealing with floatingpoint numbers.*/
    class cFloatConnection: public cValueConnection{
        private:
            double d_cached_value;            
        
        public:
            /** Constructor.
             * The contructor takes the pointer to the parent module of the
             * connection. Normaly this is the module that creates the 
             * connection. The second parameter is the child module. Normaly
             * this is the module that will own the connection. This parameter
             * is optional. If missed, no events will be send to the child. */
            cFloatConnection(cModule *parent, cDisposable *child=0);
            
            /** Pushes the given value into the cache and notify the child
             * that there is one. */
            void push(double value);
           
            /** Request the last cached value.
             * \b Note: This method is a hack to write some strange modules 
             * that doesn't fit into the definitions of the PPLT2. */
            double pop();

            /** Returns the actual value. 
             * This method will return the cached value if it is up to date.
             * Other wise it will try to get it from the parent, store it into
             * the cache and update the timestamp. */
            double get();
        
            /** Sets the value of this connection. */
            void set(double value);
        
            /** Works like get() but returns an integer. */
            int Integer();
            /** Works like set() but takes an integer. */
            void Integer(int value);
        
            /** Simlpy calles get(). */
            double Float();
            /** Simply calles set(). */
            void  Float(double value);
            
            /**\todo implement! */
            std::string String();
            /**\todo implement! */
            void String(std::string value);
        
    };
}


#endif
