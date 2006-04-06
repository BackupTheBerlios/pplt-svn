#include "cIntegerConnection.h"
#include "iIntegerModule.h"
#include "Exceptions.h"
#include "Logging.h"
#include "cModule.h"
#include <iostream>
#include <sstream>

using namespace PPLTCore;

/* Constructor: checks also it the parent is castable to a iIntegerModule */
cIntegerConnection::cIntegerConnection(cModule *parent, cDisposable *child): cValueConnection(parent, child){
    // check if parent is a IntegerModule
    if(0 == dynamic_cast<iIntegerModule *>(parent))
        throw Error("Unable to cast to iIntegerModule -> Connection closed!");
}


/* push() method: Will (may) called by the parent module. Store this given
 * value into the cache and inform the child for new data. */
void cIntegerConnection::push(int value){
    // change cache
    d_cache_value = value;
    // if child is set -> notify
    notify_child();
}


/* get() method: returns the cached value if the cachetime is not elapsed
 * other wise it tryes to get a fresh value from parent. */
int cIntegerConnection::get(){
    iIntegerModule  *mod;

    // if the cache_time is not elapsed -> return cached value.
    if(!CacheTimeElapsed()){
        CORELOG_DEBUG("Return cached value");
        return d_cache_value;
    }
    // else -> check cast to iIntegerModule:
    if(0 == (mod = dynamic_cast<iIntegerModule *>(d_parent_module)) )
        throw Error("Unable to cast to iIntegerModule!");
    // cache the new value and return it:
    CORELOG_DEBUG("Update value-cache.");
    d_cache_value = mod->get(Identifier());
    UpdateTimestamp();
    return d_cache_value;
}


/* set() method: send the new value to the parent and store it into the cache.
 * It alos updates the last_update time. */
void cIntegerConnection::set(int value){
    iIntegerModule  *mod;
    // check cast to iIntegerModule:
    if(0 == (mod = dynamic_cast<iIntegerModule *>(d_parent_module)) )
        mod->set(Identifier(), value);
    // if success -> save new value in cache:
    d_cache_value = value;
    UpdateTimestamp();
}


/* Integer converting: do nothing, just returns the value from get() */
int cIntegerConnection::Integer(){ return get(); }
/* Integer converting: just calls set() */
void cIntegerConnection::Integer(int value){ set(value); }


/* String converting: calls get() and then convert it to a string. */
std::string cIntegerConnection::String(){
    std::ostringstream o("",std::ios::ate);
    o << get();
    return o.str();
}

/* Not implemented yet */
void cIntegerConnection::String(std::string value){
    //FIXME: Implement str -> int convert
    throw NotImplementedYet("Mail author!");
}
