/***************************************************************************
 *            cIntegerSymbol.h
 *
 *  Fri Apr 28 16:23:21 2006
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
 
#ifndef PPLT_CINTEGERSYMBOL_H 
#define PPLT_CINTEGERSYMBOL_H

#include <iostream>
#include "cSymbol.h"
#include "cIntegerConnection.h"

/**\file cIntegerSymbol.h
 * This file contains the definition of the cIntegerSymbol class. */
namespace PPLTCore{
    
    /** This call implements a symbol that can handle integer values.
     * This class is a simple wrapper around the cIntegerConnection class.
     * It extends this class with some methods inherit from the cSymbol class.
     * There methods can be used to handle several user defined callback 
     * functions. 
     * @see cSymbol
     * @see cIntegerConnection */
    class cIntegerSymbol: public cSymbol{
        protected:
            cIntegerConnection  *d_int_connection;
        
        public:
            cIntegerSymbol(cModule *parent, std::string addr);
        
            int get();
            void set(int value);
        
    };        
    
}
#endif
