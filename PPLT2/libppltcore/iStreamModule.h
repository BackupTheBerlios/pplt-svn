/***************************************************************************
 *            iStreamModule.h
 *
 *  Sun Apr 23 01:18:24 2006
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
 
#ifndef PPLT_ISTREAMMODULE_H
#define PPLT_ISTREAMMODULE_H

#include "cModule.h"

/**\file iStreamModule.h
 * \brief This file contains the iStreamModule interface definition.
 *
 * The iStreamModule interface have to be implemented by any module
 * that wants to provide a data stream. */
namespace PPLTCore{

    /** This class (pure virtual) defines the interface for all modules that 
     *  provides data streams.
     * All modules that want's to provide a data stream have to implement this
     * interface, meaning to provide the methods read and write.*/
    class iStreamModule{
        public:
            /** Destructor. */
            virtual ~iStreamModule(){};

            /** This method should return max length bytes in a string.
             * @param con_id    This string countains the connection id. This 
             *                  id can be used to identify the connection 
             *                  address.
             * @param length    This integer should be the maximum of returned bytes.*/
            virtual std::string read(std::string con_id, unsigned int length) = 0;

            /** This method should process the first [length] bytes from the 
             *  given string.
             * @param con_id    This id can be used to identify the connection.
             * @param data      This string hold the data to process.
             * @param length    This integer defines the count of bytes to be 
             *                  processed from data. */
            virtual unsigned int write(std::string con_id, std::string data, unsigned int length) = 0;
    };
}

#endif
