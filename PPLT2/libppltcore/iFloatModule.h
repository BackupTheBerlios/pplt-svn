/***************************************************************************
 *            iFloatModule.h
 *
 *  Thu Apr 27 13:40:55 2006
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
 
/** \file iFloatModule.h 
 * This file contains the definition of the iFloatModule interface. */
#ifndef PPLT_IFLOATMODULE_H
#define PPLT_IFLOATMODULE_H

#include <iostream>

namespace PPLTCore{ 

    /** Interface for a module that provides floating point values.
     * This interface defines what, methods a module that wants to provide 
     * floatingpoint number have to implement. This are the methods get() and
     * set(). */
    class iFloatModule{
        public:
            virtual ~iFloatModule(){}
    
            /** Sets the value of the given connetor. 
             * Thsi method will be used by the connection or
             * Symbol to set the value of the given connection. */
            virtual void set(std::string con_id, double value) = 0;
            /** Returns the value of the given connection. */
            virtual double get(std::string con_id)=0;
    
    };

}

#endif
