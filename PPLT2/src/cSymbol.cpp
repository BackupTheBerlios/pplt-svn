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
    
    for(std::map<int, tSymbolCallback>::iterator it = d_callbacks.begin();
        it != d_callbacks.end();
        ++it){
        pthread_create(&thread, 0, 
                       reinterpret_cast<tThreadCallback>(*it->second), this);
        pthread_detach(thread);
    }
}



int cSymbol::addHandler(tSymbolCallback cb){
    int id = new_callback_id();
    
    d_callbacks[id] = cb;
    return(id);
}



// private function to generate unique ids for the callbacks:
int cSymbol::new_callback_id(void){ 
    srand(time(0));
    int id = random();
    
    while(d_callbacks.count(id))
        id = random();
    return id;
}



void cSymbol::remHandler(int ID){
    if(0==d_callbacks.count(ID)){
        throw ItemNotFound("Unable to remove callback handler with ID %i"\
                           ". No such ID found in map!", ID);
    }
    d_callbacks.erase(ID);
}


void cSymbol::reserve(void){
    d_parent_connection->reserve();
}

void cSymbol::release(void){
    d_parent_connection->release();
}

bool cSymbol::autolock(void){
    return d_parent_connection->autolock();
}

void cSymbol::autolock(bool al){
    d_parent_connection->autolock(al);
}

void cSymbol::set(int value){ 
    cValueConnection    *con;
    if(0 == (con = dynamic_cast<cValueConnection *>(d_parent_connection)) ){
        throw CoreError("Incompatible connection type: The connection does not"\
                         " provide a value.");
    }
    con->Integer(value);
}

void cSymbol::set(double value){
    cValueConnection    *con;
    if(0 == (con = dynamic_cast<cValueConnection *>(d_parent_connection)) ){
        throw CoreError("Incompatible connection type: The connection does"\
                         " not provide a value.");
    }
    con->Float(value);
}

int cSymbol::getInt(void){
    cValueConnection    *con;
    if(0 == (con = dynamic_cast<cValueConnection *>(d_parent_connection)) ){
        throw CoreError("Incompatible connection type: The connection does"\
                         " not provide a value.");
    }    
    return con->Integer();
}

double cSymbol::getFloat(void){
    cValueConnection    *con;
    if(0 == (con = dynamic_cast<cValueConnection *>(d_parent_connection)) ){
        throw CoreError("Incompatible connection type: The connection does"\
                         " not provide a value.");
    }    
    return con->Float();
}

    
