/***************************************************************************
 *            cStreamSymbol.cpp
 *
 *  Sat Apr 22 22:09:44 2006
 *  Copyright  2006  Hannes Matuschek
 *  <hmatuschek@gmx.net>
 ****************************************************************************/

#include "cStreamSymbol.h"

using namespace PPLTCore;


cStreamSymbol::cStreamSymbol(cModule * parent, std::string address)
: cSymbol(parent,address){
    if (0 == (d_stream_connection = dynamic_cast<cStreamConnection *>(d_parent_connection))){
        throw CoreError("Unable to cast to a cStreamConnection. I need a" \
                        "stream connection to act like a stream symbol!");
    }
}


std::string cStreamSymbol::read(unsigned int len){
    return d_stream_connection->read(len);
}


unsigned int cStreamSymbol::write(std::string data, unsigned int len){
    return d_stream_connection->write(data, len);
}
