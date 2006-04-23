/***************************************************************************
 *            cConnection.cpp
 *
 *  Sun Apr 23 01:26:16 2006
 *  Copyright  2006  Hannes Matuschek
 *  hmatuschek@gmx.net
 ****************************************************************************/

#include "../include/cConnection.h"
#include "../include/Exceptions.h"
#include "../include/Logging.h"

using namespace PPLTCore;


cConnection::cConnection(cModule *parent, cDisposable *owner){
    d_owner_module = owner; d_parent_module = parent;
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
    d_parent_module->reserve();
}


void cConnection::release(){
    if(0 == dynamic_cast<cModule *>(d_parent_module))
        throw CoreError("Unable to cast parent_module to cModule.");
    d_parent_module->release();
}
