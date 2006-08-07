#include "cAsyncStreamConnection.h"

using namespace PPLTCore;


cAsyncStreamConnection::cAsyncStreamConnection(cModule *parent, cDisposable *child, unsigned int timeout)
    : cStreamConnection(parent, child), d_read_cond(d_read_cond_mutex) {   
    d_timeout = timeout; 
    d_child_reading = false;
}

std::string cAsyncStreamConnection::read(unsigned int length){
    std::string     ret_buffer;

    d_read_cond_mutex.Lock();
    d_child_reading = true;

    // if there is data left in the buffer:
    if(d_buffer.length() > 0){
        if(d_buffer.length()<=length)
            length = d_buffer.length();
        
        d_buffer_lock.Lock();
        
        ret_buffer = d_buffer.substr(0,length);
        d_buffer.erase(0, length);
        
        // UNLOCK(s)
        d_buffer_lock.Unlock();
        d_read_cond_mutex.Unlock();
        d_child_reading = false;
        return(ret_buffer);
    }       

    //FIXME if d_timeout == 0 -> call Wait();
    switch(d_read_cond.WaitTimeout((unsigned long) d_timeout)){
        case wxCOND_TIMEOUT:
            d_child_reading = false;
            throw Error("Can't read: Timeout!");
            break;

        case wxCOND_NO_ERROR:
            if(d_buffer.length() <= length)
                length = d_buffer.length();
            ret_buffer = d_buffer.substr(0, length);
            d_buffer.erase(0,length);
            d_child_reading = false;
            return ret_buffer;
            break;

        default:
            d_child_reading = false;
            throw Error("Unkown behavior of the wxCondition.Wait() method!");
    }
    return "";
}

void cAsyncStreamConnection::data_notify(std::string data, unsigned int len){
    d_buffer_lock.Lock();
    
    if(len >= data.length())
        len = data.length();
    d_buffer += data.substr(0,len);
    
    d_buffer_lock.Unlock();
    
    if(d_buffer.length() == 0)
        return;

    if(d_child_reading){
        d_read_cond.Signal();
    }else{
        if(events_enabled())
            notify_child();
    }
}
