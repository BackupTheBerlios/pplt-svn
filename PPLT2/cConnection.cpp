#include "cConnection.h"
#include "Exceptions.h"
#include "Logging.h"

using namespace PPLTCore;


cConnection::cConnection(cModule *parent, cDisposable *owner){
    d_owner_module = owner; d_parent_module = parent;
}


cConnection::~cConnection(){
    try{ d_parent_module->disconnect(Identifier()); }
    catch(...){ CORELOG_ERROR("Unable to disconnect from parent!"); }
}



void cConnection::data_notify(){
    if(0 == d_owner_module)
        throw ModuleError("Can't notify owner -> no owner set!");
    d_owner_module->data_notify();
}

