/***************************************************************************
 *            iIntegerModule.h
 *
 *  Sun Apr 23 01:18:02 2006
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
 
#ifndef PPLT_IINTEGER_MODULE_H
#define PPLT_IINTEGER_MODULE_H

#include "cModule.h"

/**\file iIntegerModule.h
 * \brief This file contains the definition of the iIntegerModule
 * interface.
 *
 * The iIntegerModule interface have to be implemented by any module
 * that wants to provide data in the shape of an integer value. */
namespace PPLTCore{

    /**Interface for all modules that can return integer values.
     *
     * If you want to write a module that can return or get integer
     * values. Then you have to implement this interface. Meanig
     * your module have to provide the methods get() and set().
     *
     * By this methods your children (other modules or symbols) are
     * able to read (get()) or write (set()) integer values.  */
    class iIntegerModule{
        public:
            /** Constructor */
            iIntegerModule();
            virtual ~iIntegerModule();

            /** Should return a integer value.
             *
             * This method have to be implemented by modules,
             * that want to return integer values. This method have
             * to be implemented also if your module is "write-only".
             * @param con_id This parameter specifies the ID of the
             * connection to your module. You can retrive the address
             * the connection was etablished with by the
             * cConnectionDataBase in your module. See: cModule */
            virtual int get(std::string con_id) = 0;

            /** This method will be used by the children of the module
             * to set an integer value.
             * @param con_id The connection id of the child that wants
             * to write the value.
             * @param value The value. */
            virtual void set(std::string con_id, int value) = 0;
    };

}
#endif
