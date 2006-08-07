/***************************************************************************
 *            cStreamConnection.cpp
 *
 *  Sun Apr 23 01:27:04 2006
 *  Copyright  2006  Hannes Matuschek
 *  hmatuschek@gmx.net
 ****************************************************************************/

#include "cStreamConnection.h"

using namespace PPLTCore;

/* Constructor */
cStreamConnection::cStreamConnection(cModule *parent, cDisposable *child) 
: cConnection(parent, child){
    CORELOG_DEBUG("Init cStreamConnection to " << parent->Identifier());
    // check if parent match cStreamModule:
    if(!dynamic_cast<iStreamModule *>(parent) )
            throw Error("Can't create new StreamConnection! Parent provides no iStreamModule interface!");
    // init buffer...
}



/* Destructor: may free the internal buffer. */
cStreamConnection::~cStreamConnection(){ }



/* Push method: update buffer and notify() child.*/
void cStreamConnection::push(std::string data, unsigned int len){
    // lock internal buffer:
    d_buffer_lock.Lock();
    
    // ensures that len <= len(data);
    if(len > data.length())
        len = data.length();

    // append substring of data to buffer:
    d_buffer += data.substr(0,len);

    // unlock buffer:
    d_buffer_lock.Unlock();

    // notify child:
    if(events_enabled())
        notify_child();
}



void cStreamConnection::push(){
    if(events_enabled())
        notify_child();
}



/* Clear the internal buffer */
void cStreamConnection::flush(){
    // try to lock internal buffer:
    d_buffer_lock.Lock();
    
    // clear internal buffer:
    d_buffer.erase();

    // unlock buffer:
    d_buffer_lock.Unlock();
}



unsigned int cStreamConnection::buff_len(){
    return d_buffer.length();
}



/* Method read():
 * if there is data in the internal buffer -> return it
 * else return the data got from the parent by his read() method. */
std::string cStreamConnection::read(unsigned int len){
    iStreamModule   *mod;
    std::string     tmp; 
    // if data left in int buffer:
    if(!d_buffer.empty()){
        // lock buffer:
        d_buffer_lock.Lock();

        //ensures that len <= len(buffer):    
        if(len >= d_buffer.length())      
            len = d_buffer.length();
        
        // copy substring and delete it from buffer:
        tmp = d_buffer.substr(0,len);
        d_buffer.erase(0,len);
        
        // unlock buffer:
        d_buffer_lock.Unlock();
        return tmp;
    }

    //check cast to iStreamModule
    if(0 == (mod = dynamic_cast<iStreamModule *>(d_parent_module)) )
        throw CoreError("Unable to cast to iStreamModule!");
    
    if(autolock())
        d_parent_module->reserve();
    
    try{
        tmp = mod->read(Identifier(), len);
    }catch(...){
        if(autolock())
            d_parent_module->release();
        throw;
    }
    
    if(autolock())
        d_parent_module->release();
    return tmp;
}


/* Method write(): simply writes to the partent */
unsigned int cStreamConnection::write(std::string data, unsigned int len){
    unsigned int ret_len;
    
    // check cast to iStreamModule:
    if(0 == dynamic_cast<iStreamModule *>(d_parent_module) )
        throw CoreError("Unable to cast to iStreamModule!");
    
    if(autolock())
        d_parent_module->reserve();
    try{
        ret_len = dynamic_cast<iStreamModule *>(d_parent_module)->write(Identifier(), data, len);
    }catch(...){
        if(autolock())
            d_parent_module->release();
        throw;
    }
    
    if(autolock())
        d_parent_module->release();
    return ret_len;
}
