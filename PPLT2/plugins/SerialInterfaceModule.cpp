#include "SerialInterfaceModule.h"

using PPLTPlugins;
using PPLTCore;



SerialInterfaceModule::SerialInterfaceModule(tModuleParameters parms){
    pthread_cond_init(&d_cond_var, 0);
    pthread_mutex_init(&d_cond_var_mutex, 0);
    sem_init(&d_read_sync_sem, 0, 2);
    d_child_waiting = false;

    //FIXME init termios by params
}


std::string SerialInterfaceModule::read(std::string con_id, unsigned int len){
    timeval     now;
    timespec    timeout;
    
    pthread_mutex_lock(&d_cond_var_mutex);
    
    gettimeofday(&now);
    timeout.tv_sec = now.tv_sec + DIV(d_timeout,1000000000);
    timeout.tv_sec = now.tv_sec*1000 + (d_timout%1000000000);
    
    d_child_waiting = true;
    if(ETIMEDOUT == pthread_cond_timedwait(&d_cond_var, &d_cond_var_mutex, &timeout) )
        d_child_waiting = false;
        pthread_mutex_unlock(&d_cond_var_mutex);
        throw ModuleError("Timeout while read from serial interface.");
    }
    d_child_waiting = false;
    
    // get data from internal read-buffer -> return this!
    pthread_mutex_unlock(&d_cond_var_mutex);
}

void SerialInterfaceModule::_internal_read_thread(){
    while(d_module_runns){
        //blocking read() from interface
        if(d_child_waiting){
            // notify waiting child that there is data to read:
            pthread_cond_signal(&d_cond_var);

        }   
    }
}
