/***************************************************************************
 *            cStreamConnection.cpp
 *
 *  Sun Apr 23 01:27:04 2006
 *  Copyright  2006  Hannes Matuschek
 *  hmatuschek@gmx.net
 ****************************************************************************/

#include "../include/cStreamConnection.h"

using namespace PPLTCore;

/* Constructor */
cStreamConnection::cStreamConnection(cModule *parent, cDisposable *child) 
: cConnection(parent, child){
    CORELOG_DEBUG("Init cStreamConnection");
    // check if parent match cStreamModule:
    if(!dynamic_cast<iStreamModule *>(parent) )
            throw Error("Can't create new StreamConnection! Invalid parent module!");
    // init buffer...
    d_buffer = 0;
    d_buffer_size = 0;
    pthread_mutex_init(&d_buffer_lock, 0);
}


/* Destructor: may free the internal buffer. */
cStreamConnection::~cStreamConnection(){
    // if buffer is allocated -> free it
    if(0 != d_buffer)
        free(d_buffer);
}


/* Push method: update buffer and notify() child.*/
void cStreamConnection::push(char * buffer, int len){
    // lock internal buffer:
    if(pthread_mutex_lock(&d_buffer_lock))
        throw CoreError("Unable to lock buffer: Mutex returned error.");

    // if int. buffer not set -> init
    // else -> expand int. buffer and copy buffer into it.
    if(0 == (d_buffer = (char *)realloc(d_buffer, len+d_buffer_size)) ){
        pthread_mutex_unlock(&d_buffer_lock);
        throw CoreError("OutOfMem: Unable to alloc mem for internal buffer!");
    }

    memcpy(d_buffer+d_buffer_size, buffer, len);
    d_buffer_size += len;

    pthread_mutex_unlock(&d_buffer_lock);

    if(events_enabled())
        notify_child();
}


/* Clear the internal buffer */
void cStreamConnection::flush(){
    // try to lock internal buffer:
    if(pthread_mutex_lock(&d_buffer_lock))
        throw CoreError("Unable to lock buffer: Mutex returned error.");

    // reset the buffer!
    if(0 != d_buffer){
        free(d_buffer);
        d_buffer = 0;
        d_buffer_size = 0;
    }
    // unlock buffer:
    pthread_mutex_unlock(&d_buffer_lock);
}


/* Method read():
 * if there is data in the internal buffer -> return it
 * else return the data got from the parent by his read() method. */
int cStreamConnection::read(char *buffer, int len){
    iStreamModule   *mod;
    int             cpy_len;
    int             ret_len;
    
    // if data left in int buffer:
    if(0 != d_buffer){
        if(pthread_mutex_lock(&d_buffer_lock))
            throw CoreError("Unable to lock buffer: Mutex returned error.");
        // check length:
        if (len > d_buffer_size)
            cpy_len = d_buffer_size;
        else
            cpy_len = len;
        // copy data from int. buffer to buffer
        CORELOG_DEBUG("Copy "<<cpy_len<<"b from int buffer to out.");
        memcpy(buffer, d_buffer, cpy_len);
        // if not data left in int buffer -> free it
        if(0 == (d_buffer_size - cpy_len) ){
            CORELOG_DEBUG("Free internal buffer.");
            free(d_buffer);
            d_buffer = 0;
            d_buffer_size = 0;
        }else{
            CORELOG_DEBUG("Try to resize the int. buffer!");
            memmove(d_buffer, d_buffer+cpy_len, d_buffer_size-cpy_len);
            if(0 == (d_buffer = (char *)realloc(d_buffer, d_buffer_size-cpy_len)) ){
                pthread_mutex_unlock(&d_buffer_lock);
                throw CoreError("OutOfMem: Unable to alloc mem for int. buffer!");
            }
            d_buffer_size -= cpy_len;
        }
        pthread_mutex_unlock(&d_buffer_lock);
        return cpy_len;
    }

    //check cast to iStreamModule
    if(0 == (mod = dynamic_cast<iStreamModule *>(d_parent_module)) )
        throw CoreError("Unable to cast to iStreamModule!");
    
    if(autolock())
        d_parent_module->reserve();
    
    try{
        ret_len = mod->read(Identifier(), buffer, len);
    }catch(...){
        if(autolock())
            d_parent_module->release();
        throw;
    }
    
    if(autolock())
        d_parent_module->release();
    return ret_len;
}


/* Method write(): simply writes to the partent */
int cStreamConnection::write(char *buffer, int len){
    int ret_len;
    
    // check cast to iStreamModule:
    if(0 == dynamic_cast<iStreamModule *>(d_parent_module) )
        throw CoreError("Unable to cast to iStreamModule!");
    
    if(autolock())
        d_parent_module->reserve();
    try{
        ret_len = dynamic_cast<iStreamModule *>(d_parent_module)->write(Identifier(), buffer, len);
    }catch(...){
        if(autolock())
            d_parent_module->release();
        throw;
    }
    
    if(autolock())
        d_parent_module->release();
    return ret_len;
}
