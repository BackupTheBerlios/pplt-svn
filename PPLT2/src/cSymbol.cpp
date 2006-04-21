#include "../include/cSymbol.h"

using namespace PPLTCore;

cSymbol::cSymbol(cModule *parent, std::string addr){
    d_parent_connection = parent->connect(addr, this);
}

cSymbol::~cSymbol(){
    // close connection to parent:
    delete d_parent_connection;
}


void cSymbol::data_notify(){
    for(std::list<tSymbolCallback>::iterator it = d_callbacks.begin();
        it != d_callbacks.end();
        ++it){
        (*it)(this);
    }
}

int cSymbol::addHandler(tSymbolCallback cb){
    d_callbacks.push_back(cb);
    return(0);  //FIXME: handle this with IDs
}

void cSymbol::remHandler(int ID){ }

