#include "cModule.h"
#include "Exceptions.h"

using namespace PPLTCore;



/* ************************************************************************ *
 * Methods of cModule class:
 * ************************************************************************ */
cModule::cModule(){}
cModule::~cModule(){ }


/* ************************************************************************ *
 * Methods of CModule class:
 * ************************************************************************ */
cConnectionDataBase::cConnectionDataBase(){ }
cConnectionDataBase::~cConnectionDataBase(){ d_id_address_map.clear(); d_id_connection_map.clear(); }

void cConnectionDataBase::addConnection(std::string addr, cConnection *connection){
    std::string     id = connection->Identifier();
    d_id_address_map[id] = addr;
    d_id_connection_map[id] = connection;
}


void cConnectionDataBase::remConnection(std::string id){
    d_id_address_map.erase(id); d_id_connection_map.erase(id);
}


int cConnectionDataBase::count(){ return d_id_address_map.size(); }


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
            my_list->insert(0, d_id_connection_map[it->first]);
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
