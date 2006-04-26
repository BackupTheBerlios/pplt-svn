/***************************************************************************
 *            cConnection.h
 *
 *  Sun Apr 23 01:16:07 2006
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
 
#ifndef PPLT_CCONNECTION_H
#define PPLT_CCONNECTION_H

#include "cModule.h"
#include "cObject.h"
#include "cDisposable.h"


/**\file cConnection.h
 * \brief This file contains the definition of the basic
 * connection class. This class is used by any other connection
 * objects.
*/
namespace PPLTCore{
    /** The basic connection class.
     * The cConnection class is the base class for
     * all connections between modules and modules or
     * the external world.
     *
     * \b Note: if this class will be destroyed, the destructor
     * will call the disconnect() method of the parent module.
     * So the connection will be closed clean. You don't need
     * to care about the closing of the connection. But you
     * need to care about the destruction of the instances of
     * this class unless the instance is used to connect two
     * modules. In this case the child module will destruct
     * the connection if it is destruct.
     *
     * \b Note: All constructos all called by the connect() method
     * of the module you or an other module want to be
     * connected to. Normaly you need not to create a
     * cConnection object by your self
     * @see cStreamConnection @see cSequenceConnection
     * @see cValueConnection */
    class cConnection: public cObject{
        private:
            cDisposable     *d_owner_module;    // child module
            bool            d_is_autolock;      // autolock true by default
            bool            d_events_enabled;   // events enabled by default
        
        protected:
            /** Link to the parent module:
            * This attribute will be used by the derived classes to
            * access the parent module.
            */
            class cModule   *d_parent_module;

            /** Notyfy child about new data in buffer,
            * This method can be called from derived classes to
            * notify the child module (or symbol) about new data
            * in the  buffer.
            */
            virtual void    notify_child();
            
        public:
            /** Constructor:
            * The constructor take two arbuments, the first is a
            * pointer to the parent module, the second (optional)
            * parameter contains the pointer to the child module.
            * This pointer doesn't need to point to an complete
            * module, but the object have to implement at least the
            * cDisposable interface.
            * @param parent Pointer to the parent.
            * @param owner Optional pointer to child.
            */
            cConnection(cModule *parent, cDisposable *owner=0);
            virtual ~cConnection();

            /** Reserve the module of this connection.
            * This method reserves the module, this connection
            * is attached to. This reservation can be resetted by calling
            * release(). \b Note: Normaly a connection will automaticly
            * reserve his parent if a get(), set(), read() or write() 
            * method is called. This behavior can be disabled by calling
            * autolock(false). But in this case the programmer has to care
            * about the locking of the connection using this and the 
            * relaese() method. If it is missed it may happen, that two or more
            * tharead accesses the parent at the same time. */
            virtual void reserve();
            
            /** Release the reservation. */
            virtual void release();
            

            /** Disables or enables events events. */
            virtual void events_enabled(bool stat);
            /** Returns true if events are enabled. */
            virtual bool events_enabled(void);
            
            /** Set the autolock.
            * The autolock mechanism ensures that only one thread accesses a 
            * module at the same time. To do this each connection object have 
            * to autolock the parent at each call of get(), set(), read() or
            * write() call. But sometimes it is secessary to do the locking
            * by hand. So it is possible to disable the autolock by calling
            * this method [autolock(false)].*/
            void autolock(bool al);
            /** Returns true if autolock is enabled. */
            bool autolock();
    };

}

#endif
