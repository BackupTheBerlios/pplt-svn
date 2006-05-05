/***************************************************************************
 *            cFloatSymbol.cpp
 *
 *  Fri Apr 28 16:56:08 2006
 *  Copyright  2006  Hannes Matuschek
 *  hmatuschek@gmx.net
 ****************************************************************************/

#include "../include/cFloatSymbol.h"

using namespace PPLTCore;

cFloatSymbol::cFloatSymbol(cModule *parent, std::string addr)
: cSymbol(parent, addr){
    if(0 == (d_float_connection = dynamic_cast<cFloatConnection *>(d_parent_connection)) ){
        throw CoreError("Unable to cast connection to cFloatConnection!");
    }        
}


double cFloatSymbol::get(void){
    return d_float_connection->get();
}

void cFloatSymbol::set(double value){
    d_float_connection->set(value);
}
