/***************************************************************************
 *            cInnerModule.h
 *
 *  Sun Apr 23 01:16:28 2006
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
 
#ifndef PPLT_CINNERMODULE_H
#define PPLT_CINNERMODULE_H

#include "cModule.h"
#include "cDisposable.h"
#include "Exceptions.h"

/**\file cInnerModule.h
 * \brief This file contains the definition of the cInnerModule class.
 *
 * The cInnerModule class can be used to define a inner module. This
 * are modules, that doesn't access any hardware or the OS but
 * accessing other modules. By this a single layer of an
 * communication path will be implemented by a replaceable module,
 * This incraces the reusability of the modules for an other
 * context.*/
namespace PPLTCore{

    /** Baseclass for all inner modules.
     * A inner module differs from an Module, that it doesn't
     * interact with hardware or better with the OS. It interact
     * with other modules. This can be an Module or even an other
     * InnerModule. To do this it is needed to extend the cModule
     * call for a connection to the parent and to provied a
     * "callback" to be informed about new data at the paren for
     * this module.
     *
     * The connection to the parent is provieded by the
     * d_parent_conenction pointer to a cConenction object. This
     * object will be created by the parent module's connection()
     * method that is called by the constructor. The connection will
     * also be closed by the destructor. So you don't need to care
     * about the connection.
     *
     * This class also "implement" the cDisposable interface. That
     * means that your module have to have a method called
     * data_notify(), that will be called (indirectly) by the parent
     * module to inform your module that there is new data at the
     * parent.
     *
     * NOTE: If you want to write a real module you also have to
     * implement one (or more) of the following interfaces:
     * iStreamModule, iSequenceModule, iIntegerModule, iFloatModule,
     * ...
     */
    class cInnerModule: public cModule, public cDisposable{
        protected:
            /** Connection to the parent. */
            cConnection     *d_parent_connection;

        public:
            /** Constructor
            * This constructor will create the conenction to the
            * parent module given by the attribute parent
            * with the address given by addr.  Once done
            * you don't have to care about the handling of this
            * connection. All construction and destruction will be
            * done by the constructor and the destructior of this
            * class.
            */
            cInnerModule(cModule *parent, std::string addr, 
                         tModuleParameters params);
            ~cInnerModule();
    };

}

#endif
