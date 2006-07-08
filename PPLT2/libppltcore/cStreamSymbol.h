/***************************************************************************
 *            cStreamSymbol.h
 *
 *  Sat Apr 22 22:04:15 2006
 *  Copyright  2006  Hannes Matuschek
 *  <hmatuschek@gmx.net>
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


#ifndef PPLT_CSTREAMSYMBOL_H
#define PPLT_CSTREAMSYMBOL_H

#include "cSymbol.h" 
#include "cModule.h"
#include "cStreamConnection.h"
#include "Exceptions.h"

/** \file cStreamSymbol.h
 * \brief Defines the stream connection.
 *
 * This file contains the definition for the stream-symbol.
 * The stream symbol acts like a data-stream. So you can 
 * access the stream provided by a module by this class. */
namespace PPLTCore{
   
    /** Stream-Symbol class.
     * This class provides the basic interface to access a stream of a 
     * module. Therefor there are the methods read() and write(). */
    class cStreamSymbol: public cSymbol{
        private:
            // bool        d_is_autolock;
        
        protected:
            /** Connection to the parent. */
            cStreamConnection   *d_stream_connection;
        
        public:
            /** Constructor.
            * The constructor take 3 arguments. The first is a pointer to the
            * parent module. The second is a string containing the address of 
            * the connection to the parent. */
            cStreamSymbol(cModule *parent, std::string address);
            
            /** Reads len bytes from the parent.
            * This method will read len bytes from the parent and
            * return them as a string.*/
            std::string read(unsigned int len);
        
            /** Writes len bytes from data to the parent module.
            * This method will write len bytes copyed from data to the 
            * parent. \b Note: This method will lock and unlock the parent if 
            * autolock is enabled. */
            unsigned int write(std::string data, unsigned int len);
            

    };
    
}

#endif
