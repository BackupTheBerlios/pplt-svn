/***************************************************************************
 *            LoopbackModule.cpp
 *
 *  Sun Apr 23 01:26:00 2006
 *  Copyright  2006  Hannes Matuschek
 *  hmatuschek@gmx.net
 ****************************************************************************/

#include "LoopbackModule.h"

using namespace PPLTCore;
using namespace PPLTPlugin;


cModule *LoopbackModuleFactory(tModuleParameters params){
    return new LoopbackModule(params);
}



LoopbackModule::LoopbackModule(tModuleParameters params):cModule(params){}


cConnection *LoopbackModule::connect(std::string addr, cDisposable *child){
    cConnection *con;
    if("" == addr)
        throw ModuleError("This module needs a usefull addr.");
    if (2 <= d_connections.count(addr))
        throw ModuleError("This address is in use by >= 2 modules.");
    con = new cStreamConnection(this, child);
    d_connections.addConnection(addr, con);
    return con;
}


void LoopbackModule::disconnect(std::string con_id){
    d_connections.remConnection(con_id);
}


cConnection *LoopbackModule::GetTheOtherOne(std::string con_id){
    std::list<cConnection *>    *clist;
    std::string     addr = d_connections.getAddressByID(con_id);
    cConnection     *con;

    if(2 != d_connections.count(addr) )
        return 0;

    clist   = d_connections.getConnectionsByAddress(addr);

    con = clist->front();
    if(con->Identifier() == con_id){
        clist->pop_front();
        con = clist->front();
    }
    delete clist;
    return con;
}


int LoopbackModule::read(std::string con_id, char *buffer, int len){
    MODLOG_DEBUG("LoopbackModule has no internal buffer so I return 0");
    return 0;
}


int LoopbackModule::write(std::string con_id, char *buffer, int len){
    cStreamConnection       *con;
    
    if(0 == (con = dynamic_cast<cStreamConnection *>(GetTheOtherOne(con_id))) )
        throw ModuleError("Can't cast to cStremConnection!");
    con->push(buffer, len);    
    return len;
}