/***************************************************************************
 *            cSymbol.cpp
 *
 *  Sun Apr 23 01:13:08 2006
 *  Copyright  2006  Hannes Matuschek
 *  hmatuschek@gmx.net
 ****************************************************************************/


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
    pthread_t       thread;
    
    for(std::list<tSymbolCallback>::iterator it = d_callbacks.begin();
        it != d_callbacks.end();
        ++it){
        pthread_create(&thread, 0, reinterpret_cast<tThreadCallback>(*it), this);
        pthread_detach(thread);
    }
}

int cSymbol::addHandler(tSymbolCallback cb){
    d_callbacks.push_back(cb);
    return(0);  //FIXME: handle this with IDs
}

void cSymbol::remHandler(int ID){ }
