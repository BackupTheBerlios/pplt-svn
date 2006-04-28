/***************************************************************************
 *            cStreamSymbol.cpp
 *
 *  Sat Apr 22 22:09:44 2006
 *  Copyright  2006  Hannes Matuschek
 *  <hmatuschek@gmx.net>
 ****************************************************************************/

#include "../include/cStreamSymbol.h"

using namespace PPLTCore;


cStreamSymbol::cStreamSymbol(cModule * parent, std::string address)
: cSymbol(parent,address){
    if (0 == (d_stream_connection = dynamic_cast<cStreamConnection *>(d_parent_connection))){
        throw CoreError("Unable to cast to a cStreamConnection. I need a" \
                        "stream connection to act like a stream symbol!");
    }
}


int cStreamSymbol::read(char *buffer, int len){
    return d_stream_connection->read(buffer, len);
}


int cStreamSymbol::write(char *buffer, int len){
    return d_stream_connection->write(buffer, len);
}



void cStreamSymbol::reserve(){ 
    d_parent_connection->reserve(); 
}


void cStreamSymbol::release(){ 
    d_parent_connection->release(); 
}


void cStreamSymbol::autolock(bool al){ 
    d_parent_connection->autolock(al);
}

bool cStreamSymbol::autolock(){ 
    return d_parent_connection->autolock(); 
}
