/***************************************************************************
 *            cIntegerSymbol.cpp
 *
 *  Fri Apr 28 16:29:46 2006
 *  Copyright  2006  Hannes Matuschek
 *  hmatuschek@gmx.net
 ****************************************************************************/

#include "../include/cIntegerSymbol.h"

using namespace PPLTCore;

cIntegerSymbol::cIntegerSymbol(cModule *parent, std::string addr)
: cSymbol(parent, addr){
    if(0 == (d_int_connection = dynamic_cast<cIntegerConnection *>(d_parent_connection)) ){
        throw CoreError("Unable to cast parent connection to cIntegerConnection! "
                        "But a IntegerConnection is needed!");
    }
}

int cIntegerSymbol::get(void){
    return d_int_connection->get();
}

void cIntegerSymbol::set(int value){
    d_int_connection->set(value);
}
