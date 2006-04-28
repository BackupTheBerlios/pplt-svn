/***************************************************************************
 *            cFloatConnection.h
 *
 *  Thu Apr 27 13:48:52 2006
 *  Copyright  2006  User
 *  Email
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
 
#include "iFloatModule.h"
#include "cValueConnection.h"
#include "cDisposable.h"

namespace PPLTCore{
    
    class cFloatConnection: public cValueConnection{
        private:
            double d_cached_value;            
        
        public:
            cFloatConnection(cModule *parent, cDisposable *child=0);
            
            void push(double value);
            
            double get();
            void set(double value);
        
            int Integer();
            void Integer(int value);
        
            double Float();
            void  Float(double value);
        
            std::string String();
            void String(std::string value);
        
    };
}
