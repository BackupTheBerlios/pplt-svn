/***************************************************************************
 *            cFloatSymbol.h
 *
 *  Fri Apr 28 16:47:52 2006
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
 
#ifndef PPLT_CFLOATSYMBOL_H
#define PPLT_CFLOATSYMBOL_H

#include <iostream>
#include "cSymbol.h"
#include "cFloatConnection.h"

/**\file cFloatSymbol.h
 * This file contains the definition of the cFloatSymbol. **/
namespace PPLTCore{

    /** This class implements a symbol that deals with floating point numbers.
     * This class is a simple wrapper around the cFloatConnection. It extends
     * it interface with some methods inherit from the cSymbol class to manage
     * user defined callback methods. 
     * @see cFloatConnection
     * @see cSymbol*/
    class cFloatSymbol: public cSymbol{
        protected:
            cFloatConnection    *d_float_connection;
        
        public:
            cFloatSymbol(cModule *parent, std::string addr);
        
            double get();
            void set(double value);
    };
    
}

#endif
