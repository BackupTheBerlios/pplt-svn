/***************************************************************************
 *            NULLModule.cpp
 *
 *  Sun Apr 23 01:26:06 2006
 *  Copyright  2006  Hannes Matuschek
 *  hmatuschek@gmx.net
 ****************************************************************************/

#include <iostream>
#include "NULLModule.h"

using namespace PPLTCore;

using namespace PPLTPlugin;





cModule *NULLModuleFactory(tModuleParameters params){
    return new NULLModule(params);
}



NULLModule::NULLModule(tModuleParameters params): cModule(params){
    MODLOG_DEBUG("Setup NULLModule");
}



cConnection *NULLModule::connect(std::string addr, cDisposable *child){
    cStreamConnection   *con = 0;
    if(0 == child){
        con = new cStreamConnection(this);
    }else{
        con = new cStreamConnection(this, child);
    }
d_connections.addConnection(addr, con);
return con;
}



cConnection *NULLModule::connect(std::string addr){ return connect(addr, 0); }



void NULLModule::disconnect(std::string id){
    d_connections.remConnection(id);
}



std::string NULLModule::read(std::string addr, int len){
    if(len<0)
        return "";

    std::string buffer;

    for(int n=0;n<len;n++)
        buffer[n] = (char)0;

    return buffer;
}



int NULLModule::write(std::string addr, std::string buffer, int len){ return len; }
