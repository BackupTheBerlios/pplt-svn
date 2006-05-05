/***************************************************************************
 *            cModule.cpp
 *
 *  Sun Apr 23 01:26:36 2006
 *  Copyright  2006  Hannes Matuschek
 *  hmatuschek@gmx.net
 ****************************************************************************/

#include "../include/cModule.h"
#include "../include/Exceptions.h"

using namespace PPLTCore;



/* ************************************************************************ *
 * Methods of cModule class:
 * ************************************************************************ */
cModule::cModule(tModuleParameters params){
    // init mutexes:
    pthread_mutex_init(&d_reservation_lock, 0);
    d_parameters = params;
}

cModule::~cModule(){ }


void cModule::reserve(){
    if(pthread_mutex_lock(&d_reservation_lock))
        throw CoreError("Unable to reserver module! Error returned from mutex.");
    MODLOG_DEBUG("Module ("<<Identifier().substr(0,12)<<"...) reserved.");
}

void cModule::release(){
    MODLOG_DEBUG("Release module ("<<Identifier().substr(0,12)<<"...).");
    pthread_mutex_unlock(&d_reservation_lock);
}




/* ************************************************************************ *
 * Methods of CModule class:
 * ************************************************************************ */
cConnectionDataBase::cConnectionDataBase(){ }

cConnectionDataBase::~cConnectionDataBase(){
    d_id_address_map.clear(); d_id_connection_map.clear();
}


void cConnectionDataBase::addConnection(std::string addr, cConnection *connection){
    std::string     id = connection->Identifier();
    d_id_address_map[id] = addr;
    d_id_connection_map[id] = connection;
}


void cConnectionDataBase::remConnection(std::string id){
    d_id_address_map.erase(id); d_id_connection_map.erase(id);
}


int cConnectionDataBase::count(){ return d_id_address_map.size(); }
int cConnectionDataBase::count(std::string addr){
    int         con_count = 0;

    for( std::map<std::string, std::string>::iterator it = d_id_address_map.begin();
            it != d_id_address_map.end(); ++it){
        con_count++;
    }
    return con_count;
}


cConnection *cConnectionDataBase::getConnectionByID(std::string id){
    return d_id_connection_map[id];
}


std::string cConnectionDataBase::getAddressByID(std::string id){
    return d_id_address_map[id];
}


std::list<cConnection *> *cConnectionDataBase::getConnectionsByAddress(std::string addr){
    std::list<cConnection *>  *my_list = new std::list<cConnection *>;

    for( std::map<std::string, std::string>::iterator it = d_id_address_map.begin();
            it != d_id_address_map.end(); ++it){
        if(addr == it->second)
            my_list->push_back(d_id_connection_map[it->first]);
    }

    return my_list;
}

bool cConnectionDataBase::hasAddress(std::string addr){
    for( std::map<std::string, std::string>::iterator it = d_id_address_map.begin();
            it != d_id_address_map.end(); ++it){
        if(addr == it->second)
            return true;
    }
    return false;
}

bool cConnectionDataBase::hasID(std::string id){
    if(d_id_address_map.end() == d_id_address_map.find(id))
        return false;
    return true;
}
