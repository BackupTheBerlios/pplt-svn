/***************************************************************************
 *            cFloatConnection.cpp
 *
 *  Fri Apr 28 14:13:02 2006
 *  Copyright  2006  Hannes Matuschek
 *  hmatuschek@gmx.net
 ****************************************************************************/
 
#include "cFloatConnection.h"


using namespace PPLTCore;


cFloatConnection::cFloatConnection(cModule *parent, cDisposable *child)
: cValueConnection(parent,child){
    if(0 == dynamic_cast<iFloatModule *>(parent)){
        throw Error("Unable to cast parent module to iFloatModule!"\
                    " Need a FloatModule as parent for a FloatConnection!");
    }    
}

void cFloatConnection::push(double value){
    // save the pushed value into the cache and update value-timestamp:
    d_cached_value = value;
    UpdateTimestamp();
    
    // if events are enabled for this connection -> notify_child()
    if(events_enabled())
        notify_child();
}



// will be called by the parent module to get the last value...
double cFloatConnection::pop( void ){
    return d_cached_value;
}



/* GET method: will be called like: value = connection.get(); */
double cFloatConnection::get(){
    iFloatModule    *mod;
 
    // if the cached value is still up to date -> return it.
    if(!CacheTimeElapsed()){
        CORELOG_DEBUG("Return cached value: "<< d_cached_value);
        return d_cached_value;
    }
    
    // try to cast parent-module to a float-module!
    if(0 == (mod = dynamic_cast<iFloatModule *>(d_parent_module)) ){
        throw CoreError("Unable to cast parent module to iFloatModule! A"\
                        "a cFloatConnection needs a iFloatModule as parent!");
    }
    
    CORELOG_DEBUG("Update iternal cache...");
    // lock parent
    if(autolock())
        d_parent_module->reserve();
    // try to get new value:
    try{
        d_cached_value = mod->get_float(Identifier());
    }catch(...){
        // on error release and rethrow exception.
        if(autolock())
            d_parent_module->release();
        throw;
    }
    // release parent
    if(autolock())
        d_parent_module->release();
    // update timestamp and return value.
    UpdateTimestamp();
    
    return d_cached_value;        
}   



void cFloatConnection::set(double value){
    iFloatModule  *mod;
    
    // check cast to iIntegerModule:
    if(0 == (mod = dynamic_cast<iFloatModule *>(d_parent_module)) )
        throw CoreError("Unable to cast parent module to iFloatModule! "
                        "But a cFloatConnection needs a iFloatModule!");
    
    // lock parent
    if(autolock())
        d_parent_module->reserve();
    
    // try to get new value
    try{ 
        mod->set_float(Identifier(), value);
    }catch(...){
        // on error: unlock parent and rethrow exception.
        if(autolock()){ d_parent_module->release(); }
        throw;
    }
    // unlock parent
    if(autolock()){ d_parent_module->release(); }
    
    // if success -> save new value in cache:
    d_cached_value = value;
    UpdateTimestamp();
}



int cFloatConnection::Integer(){
    return (int)get();
}   

void cFloatConnection::Integer(int value){
    set((double) value);
}


double cFloatConnection::Float(){ 
    return get();
}

void cFloatConnection::Float(double value){
    set(value);
}


std::string cFloatConnection::String(){
    //TODO: Implement!
    throw NotImplementedYet("cFloatConnection::String() is not implemented yet!");
}

void cFloatConnection::String(std::string value){
    throw NotImplementedYet("cFloatConnection::String(value) is not implemented yet!");
}
