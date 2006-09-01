/***************************************************************************
 *            cConnection.cpp
 *
 *  Sun Apr 23 01:26:16 2006
 *  Copyright  2006  Hannes Matuschek
 *  hmatuschek@gmx.net
 ****************************************************************************/

#include "cConnection.h"

using namespace PPLTCore;


cConnection::cConnection(cModule *parent, cDisposable *owner){
    d_owner_module = owner; d_parent_module = parent;
    d_is_autolock = true;
    d_events_enabled = true;
}


cConnection::~cConnection(){
    try{ d_parent_module->disconnect(Identifier()); }
    catch(...){ CORELOG_ERROR("Unable to disconnect from parent!"); }
}


void cConnection::notify_child(){
    if(0 == d_owner_module)
        throw ModuleError("Can't notify owner -> no owner set!");
    d_owner_module->data_notify();
}


void cConnection::reserve(){
    if(0 == dynamic_cast<cModule *>(d_parent_module))
        throw CoreError("Unable to cast parent_module to cModule.");
    
    // Store status of events and disable them. This will cause the connection
    // to buffer all incomming events unlit release() will be called!
    d_event_status = events_enabled();
    events_enabled(false);

    // lock the parent module!
    d_parent_module->reserve();
}



void cConnection::release(){
    if(0 == dynamic_cast<cModule *>(d_parent_module))
        throw CoreError("Unable to cast parent_module to cModule.");
    
    d_parent_module->release();
    events_enabled(d_event_status);
}


void cConnection::events_enabled(bool stat){
    d_events_enabled = stat;
}

bool cConnection::events_enabled(void){
    return d_events_enabled;
}


void cConnection::autolock(bool al){ d_is_autolock = al; }
bool cConnection::autolock(void){ return d_is_autolock; }
