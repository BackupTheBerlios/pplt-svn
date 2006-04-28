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
            bool        d_is_autolock;
        
        protected:
            /** Connection to the parent. */
            cStreamConnection   *d_stream_connection;
        
        public:
            /** Constructor.
            * The constructor take 3 arguments. The first is a pointer to the
            * parent module. The second is a string containing the address of 
            * the connection to the parent. */
            cStreamSymbol(cModule *parent, std::string address);
            
            /** Reads len bytes from the parent into buffer.
            * This method will read len bytes from the parent and
            * copy them into buffer. \b Note: buffer have to be >= len bytes. 
            * \b Note: This method will (un-) lock the parent if autolock is 
            * enabled. */
            int read(char *buffer, int len);
        
            /** Writes len bytes from buffer to the parent module.
            * This method will write len bytes copyed from buffer to the 
            * parent. \b Note: This method will lock and unlock the parent if 
            * autolock is enabled. */
            int write(char *buffer, int len);
            
            /** Reserves (lock) the parent module.
            * \b Note: You only need to use this method if autolock is disabled
            * otherwise this clas takes care about the locking of the parent 
            * module. But sometimes it is secessary to do the locking by hand.
            * To disable the locking please use the autolock() method. But be
            * carefull with the using of this method. It may cause deadlocks!*/
            void reserve();
            
            /** Releases the parent module if it was reserved. */
            void release();
            
            /** Enable or disable autolock.
            * With this method you can set the autolock. Calling autolock(true)
            * to enable the autolock and with false to disable.*/
            void autolock(bool al);

            /** Get autolock state.
            * Returns true if autolock is enabled. */
            bool autolock(void);
    };
    
}

#endif
