/***************************************************************************
 *            RandomModule.cpp
 *
 *  Sun Apr 23 01:26:11 2006
 *  Copyright  2006  Hannes Matuschek
 *  hmatuschek@gmx.net
 ****************************************************************************/

#include "../include/RandomModule.h"


using namespace PPLTCore;
using namespace PPLTPlugin;



RandomModule::RandomModule(): cModule(){
    //init random generator:
    std::srand(std::time(0));
}

cConnection *RandomModule::connect(std::string addr, cDisposable *child){
    cConnection *con = 0;

    MODLOG_DEBUG("Connection request for \""+addr+"\"");

    if(addr == ""){
        con = new cStreamConnection(this, child);
    }else if(addr == "int"){
        con = new cIntegerConnection(this, child);
    }else
        throw Error("Unknown address for module RandomModule");

    d_connections.addConnection(addr, con);
    return con;
}



void RandomModule::disconnect(std::string con_id){
    d_connections.remConnection(con_id);
}


void RandomModule::enable_events(){}
void RandomModule::disable_events(){}


int RandomModule::read(std::string con_id, char *buff, int len){
    if("" != d_connections.getAddressByID(con_id))
        throw Error("Wrong interface...");
    for(register int n=0;n<len;n++)
        buff[n] = (char)(std::rand()%256);
    return len;
}

int RandomModule::write(std::string con_id, char *buff, int len){
    throw Error("This module is read only!");
}


int RandomModule::get(std::string con_id){
    MODLOG_DEBUG("get() request from connection :"+con_id);
    if("int" != d_connections.getAddressByID(con_id))
        throw Error("Wrong interface...");
    return std::rand();
}

void RandomModule::set(std::string con_id, int value){
    throw Error("This module is read only!");
}
