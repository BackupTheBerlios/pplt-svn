/***************************************************************************
 *            cFloatConnection.c
 *
 *  Thu Apr 27 14:01:07 2006
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
 
#include "../include/cFloatConnection.h"
#include "../include/cValueConnection.h"


using namespace PPLTCore;


cFloatConnection::cFloatConnection(cModule parent, cDisposable *child)
: cValueConnection(parent,child){
    if(0 == dynamic_cast<iFloatModule *>(parent)){
        throw Error("Unable to cast parent module to iFloatModule!"\
                    " Need a FloatModule as parent for a FloatConnection!");
    }    
}


cFloatConnection::push(double value){
    d_cached_value = value;
    UpdateTimestamp();
    
    if(events_enabled())
        notify_child();
}

//FIXME:
cFloatConnection::get();
cFloatConnection::set();

cFloatConnection::Integer();
cFloatConnection::Integer();

cFloatConnection::Float();
cFloatConnection::Float();

cFloatConnection::String();
cFloatConnection::String();
