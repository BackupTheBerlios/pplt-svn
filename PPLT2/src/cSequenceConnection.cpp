/***************************************************************************
 *            cSequenceConnection.cpp
 *
 *  Sun Apr 23 01:27:00 2006
 *  Copyright  2006  Hannes Matuschek
 *  hmatuschek@gmx.net
 ****************************************************************************/

#include "../include/cSequenceConnection.h"

using namespace PPLTCore;


cSequenceConnection::cSequenceConnection(cModule *parent, cDisposable *child)
: cConnection(parent, child){
    // checks  the type of the parent module:
    if(0 == dynamic_cast<iSequenceModule *>(parent))
        throw CoreError("Unable to cast the parent to an iSequenceModule");

    pthread_mutex_init(&d_cache_lock, 0);
    d_buffer_len = 0; d_internal_buffer = 0;
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
    if(0 != d_internal_buffer){
        d_buffer_len = 0;
        free(d_internal_buffer);
        d_internal_buffer = 0;
    }
    // unlock cache:
    pthread_mutex_unlock(&d_cache_lock);
}


std::string cSequenceConnection::recv(){
    iSequenceModule     *mod;
    std::string         ret;

    // check parent-module-type:
    if(0 == (mod = dynamic_cast<iSequenceModule *>(d_parent_module)))
        throw CoreError("Unable to cast parent to iSequenceModule.");


    // if there is data left in the stream_cache:
    if(d_buffer_len > 0){
        // lock internal cache:
        if(pthread_mutex_lock(&d_cache_lock))
            throw CoreError("Unable to lock cache: Mutex returned error.");
        // append this data to the return string:
        ret.append(d_internal_buffer, d_buffer_len);
        // free and reset the internal_buffer:
        free(d_internal_buffer);
        d_internal_buffer = 0;
        d_buffer_len = 0;
        // unlock cache:
        pthread_mutex_unlock(&d_cache_lock);
        return(ret);
    }

    // if there are sequences in the cache:
    if(d_data_cache.size() > 0){
        // lock internal cache:
        if(pthread_mutex_lock(&d_cache_lock))
            throw CoreError("Unable to lock cache: Mutex returned error.");
        // fetch first element from cache:
        std::string ret = d_data_cache.front();
        d_data_cache.pop_front();
        // unloc cache:
        pthread_mutex_unlock(&d_cache_lock);
        return ret;
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



int cSequenceConnection::read(char *buffer, int len){
    int     cpy_len;

    // lock internal buffer:
    if(pthread_mutex_lock(&d_cache_lock))
        throw CoreError("Unable to lock my cache: Mutex returned error.");

    // if buffer empty -> fill up
    if(0 == d_buffer_len){
        char        *int_buff;
        int         int_len;
        // try to recieve a new sequence:
        try{
            // i need not to lock parent: this is done by the recv() method.
            std::string tmp = recv();
            int_buff = (char *)tmp.data();
            int_len  = tmp.size();
        }catch(...){
            // if exception -> unlock && rethrow exception
            pthread_mutex_unlock(&d_cache_lock);
            throw;
        }

        // try to alloc mem for the internal buffer:
        if(0 == (d_internal_buffer = (char *)malloc(int_len)) ){
            // if fails: reset buffer length:
            d_buffer_len = 0;
            // unlock cache and throw an exception:
            pthread_mutex_unlock(&d_cache_lock);
            throw CoreError("OutOfMem: Unable to alloc mem for internal buffer!");
        }
        // copy the data of the sequence into the internal buffer:
        memcpy(d_internal_buffer, int_buff, int_len);
        // and set length:
        d_buffer_len = int_len;
    }

    // if there is more data in buffer than requested:
    //  -> copy_length = requested length:
    // else:    -> copy_length = length of internal buffer.
    if(len < d_buffer_len)
        cpy_len = len;
    else
        cpy_len = d_buffer_len;

    // copy copy_length bytes from internal buffer into output buffer:
    memcpy(buffer, d_internal_buffer, cpy_len);

    // if there is no data ledt in the internal buffer:
    if(cpy_len == d_buffer_len){
        // free && reset buffer:
        d_buffer_len = 0;
        free(d_internal_buffer);
        d_internal_buffer = 0;
        // unlock cache and return copy_length:
        pthread_mutex_unlock(&d_cache_lock);
        return(cpy_len);
    }

    // if there war data left in the buffer:
    //  -> resize internal buffer by:
    // - move rest of data to the beginning of the internal_buffer:
    memmove(d_internal_buffer, d_internal_buffer+cpy_len, d_buffer_len-cpy_len);
    // try to resize the buffer:
    if(0 == (d_internal_buffer = (char *)realloc(d_internal_buffer, d_buffer_len-cpy_len)) ){
        // if unable to resize buffer: reset buffer, unlock cache,
        // and finally throw an exception
        d_buffer_len = 0;
        pthread_mutex_unlock(&d_cache_lock);
        throw CoreError("OutOfMem: Unable to realloc mem for internal buffer.");
    }
    // recalc new internal buffer size:
    d_buffer_len -= cpy_len;
    // unloc cache and return number of copied bytes:
    pthread_mutex_unlock(&d_cache_lock);
    return cpy_len;
}


int cSequenceConnection::write(char *buffer, int len){
    std::string tmp;
    // simply convert (len) bytes from (buffer) into a string and
    // call send() -> return (len) because (len) bytes are send.
    tmp.append(buffer, len);
    //there is no locking needed because it is done by the send() method
    send(tmp);      
    return len;
}
