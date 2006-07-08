/***************************************************************************
 *            cSequenceConnection.cpp
 *
 *  Sun Apr 23 01:27:00 2006
 *  Copyright  2006  Hannes Matuschek
 *  hmatuschek@gmx.net
 ****************************************************************************/

#include "cSequenceConnection.h"

using namespace PPLTCore;


cSequenceConnection::cSequenceConnection(cModule *parent, cDisposable *child)
: cConnection(parent, child){
    // checks  the type of the parent module:
    if(0 == dynamic_cast<iSequenceModule *>(parent))
        throw CoreError("Unable to cast the parent to an iSequenceModule");

    pthread_mutex_init(&d_cache_lock, 0);
}

cSequenceConnection::~cSequenceConnection(){
    flush();
}


void cSequenceConnection::push(){
    notify_child();
}


void cSequenceConnection::push(std::string data){
    // ensure that only one thread accesses the cache:
    if(pthread_mutex_lock(&d_cache_lock))
        throw CoreError("Unable to lock cache: Mutex returned error!");
    // append data-string to cache:
    d_data_cache.push_back( std::string(data) );
    // unlock cache:
    pthread_mutex_unlock(&d_cache_lock);
    
    // inform child module (if events are enabled).
    if(events_enabled())
        notify_child();
}


void cSequenceConnection::flush(){
    //FIXME: does this delete all strings in list?
    // ensure that only one thread accesses the cache:
    if(pthread_mutex_lock(&d_cache_lock))
        throw CoreError("Unable to lock cache. Mutex returned error.");
    // clear cache...
    d_data_cache.clear();
    // free stream_buffer:
    if(!d_internal_buffer.empty())
        d_internal_buffer.erase();
    // unlock cache:
    pthread_mutex_unlock(&d_cache_lock);
}


std::string cSequenceConnection::recv(){
    iSequenceModule     *mod;
    std::string         ret;

    // check parent-module-type:
    if(0 == (mod = dynamic_cast<iSequenceModule *>(d_parent_module)))
        throw CoreError("Unable to cast parent to iSequenceModule.");

    // If there is data left in the internal buffer:
    if(!d_internal_buffer.empty()){
        if(pthread_mutex_lock(&d_cache_lock))
            throw CoreError("Unable to lock cache. Mutex returned error.");
        
        std::string tmp = d_internal_buffer;
        d_internal_buffer.erase();
        
        pthread_mutex_unlock(&d_cache_lock);
        return tmp;
    }

    // if there is data left in the cache.
    if(!d_data_cache.empty()){
        if(pthread_mutex_lock(&d_cache_lock))
            throw CoreError("Unable to lock cache. Mutex returned error.");
        
        std::string tmp = d_data_cache.front();
        d_data_cache.pop_front();

        pthread_mutex_unlock(&d_cache_lock);
        return(tmp);
    }

    // if autolock is enabled -> lock parent
    if(autolock())
        d_parent_module->reserve();
    
    // try to get new seq.
    try{
        ret = mod->recv(Identifier());
    }catch(...){
        // on error -> unlock and rethrow exception
        if(autolock())
            d_parent_module->release();
        throw;
    }
    
    // unlock and return
    if(autolock())
        d_parent_module->release();
    return ret;
}



void cSequenceConnection::send(std::string data){
    if(0 == dynamic_cast<iSequenceModule *>(d_parent_module))
        throw CoreError("Unable to cast parent to iSequenceModule.");
    if(autolock())
        d_parent_module->reserve();
    try{
        dynamic_cast<iSequenceModule *>(d_parent_module)->send(Identifier(), data);
    }catch(...){
        if(autolock())
            d_parent_module->release();
        throw;
    }
    if(autolock())
        d_parent_module->release();
}



std::string cSequenceConnection::read(unsigned int len){
    unsigned int     cpy_len;

    if(d_internal_buffer.empty() and d_data_cache.empty()){
        // DO NOT LOCK HERE!
        d_internal_buffer = recv();
    }
    
    // lock internal buffer:
    if(pthread_mutex_lock(&d_cache_lock))
        throw CoreError("Unable to lock my cache: Mutex returned error.");
    
    if(d_internal_buffer.empty()){
        d_internal_buffer = d_data_cache.front();
        d_data_cache.pop_front();
    }        

    unsigned int bufflen = d_internal_buffer.length();
    if(len <= bufflen)
        cpy_len = len;
    if(len > bufflen)
        cpy_len = bufflen;

    std::string tmp = d_internal_buffer.substr(0,cpy_len);
    d_internal_buffer.erase(0,cpy_len);

    //unlock cache:
    pthread_mutex_unlock(&d_cache_lock);
    
    return tmp;
}


unsigned int cSequenceConnection::write(std::string data, unsigned int len){
    // make sure that len is <= len(data)
    if(len > data.length())
        len = data.length();
    // send substring:        
    send(data.substr(0,len));
    //return number of bytes send:
    return len;
}
