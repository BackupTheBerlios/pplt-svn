#include "cStreamConnection.h"
#include "iStreamModule.h"
#include "Exceptions.h"
#include "Logging.h"

using namespace PPLTCore;

/* Constructor */
cStreamConnection::cStreamConnection(cModule *parent, cDisposable *child) : cConnection(parent, child){
    CORELOG_DEBUG("Init cStreamConnection");
    // check if parent match cStreamModule:
    if(!dynamic_cast<iStreamModule *>(parent) )
            throw Error("Can't create new StreamConnection! Invalid parent module!");
    // init buffer...
    d_buffer = 0;
    d_buffer_size = 0;
}
/* Destructor: may free the internal buffer. */
cStreamConnection::~cStreamConnection(){
    // if buffer is allocated -> free it
    if(0 != d_buffer)
        free(d_buffer);
}


/* Push method: update buffer and notify() child.*/
void cStreamConnection::push(char * buffer, int len){
    // if int. buffer not set -> init
    // else -> expand int. buffer and copy buffer into it.
    if(0 == (d_buffer = (char *)realloc(d_buffer, len+d_buffer_size)) )
        throw CoreError("OutOfMem: Unable to alloc mem for internal buffer!");

    memcpy(d_buffer+d_buffer_size, buffer, len);
    d_buffer_size += len;
    notify_child();
}


/* Clear the internal buffer */
void cStreamConnection::flush(){
    // reset the buffer!
    if(0 != d_buffer){
        free(d_buffer);
        d_buffer = 0;
        d_buffer_size = 0;
    }
}


/* Method read():
 * if there is data in the internal buffer -> return it
 * else return the data got from the parent by his read() method. */
int cStreamConnection::read(char *buffer, int len){
    iStreamModule   *mod;
    int             cpy_len;

    // if data left in int buffer:
    if(0 != d_buffer){
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
            if(0 == (d_buffer = (char *)realloc(d_buffer, d_buffer_size-cpy_len)) )
                throw CoreError("OutOfMem: Unable to alloc mem for int. buffer!");
            d_buffer_size -= cpy_len;
        }
        return cpy_len;
    }

    //check cast to iStreamModule
    if(0 == (mod = dynamic_cast<iStreamModule *>(d_parent_module)) )
        throw CoreError("Unable to cast to iStreamModule!");
    // call read() method of the parent
    return mod->read(Identifier(), buffer, len);
}


/* Method write(): simply writes to the partent */
int cStreamConnection::write(char *buffer, int len){
    // check cast to iStreamModule:
    if(0 == dynamic_cast<iStreamModule *>(d_parent_module) )
        throw CoreError("Unable to cast to iStreamModule!");
    // call write() method of the parent:
    return dynamic_cast<iStreamModule *>(d_parent_module)->write(Identifier(), buffer, len);
}
