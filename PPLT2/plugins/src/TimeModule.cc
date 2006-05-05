/***************************************************************************
 *            TimeModule.cc
 *
 *  Sun Apr 30 00:17:43 2006
 *  Copyright  2006  User
 *  Email
 ****************************************************************************/

#include "TimeModule.h"

using namespace PPLTCore;
using namespace PPLTPlugin;


cModule *TimeModuleFactory(tModuleParameters params){
    return new TimeModule(params);
}



TimeModule::TimeModule(tModuleParameters params): cModule(params){ }

cConnection *TimeModule::connect(std::string addr, cDisposable *child){
    cFloatConnection *con;
    
    if(addr == "timestamp"){
        MODLOG_DEBUG("Make connection for \"timestamp\".");            
        con = new cFloatConnection(this, child);
        d_connections.addConnection(addr, con);
        return con;
    }else{
        throw ModuleError("Unknown address \"%s\" for module TimeModule.",
                            addr.c_str());
    }
}

void TimeModule::disconnect(std::string con_id){
    d_connections.remConnection(con_id);
}

double TimeModule::get(std::string con_id){
    struct ntptimeval   t;
    double              val;
    
    if(d_connections.getAddressByID(con_id) == "timestamp"){
        ntp_gettime(&t);
        val = t.time.tv_sec;
        val += (double)(t.time.tv_usec)/1000000;
        return val;
    }
    throw ModuleError("Unknown address \"%s\" of connection (%s)! "\
                      "This should not happend!", 
                      d_connections.getAddressByID(con_id).c_str(),
                      con_id.c_str());
}

void TimeModule::set(std::string con_id, double value){
    throw ModuleError("This module (TimeModule) is read only!!!");
}
