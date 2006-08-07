#include "SerialInterfaceModule.h"

using PPLTPlugins;
using PPLTCore;



/* Constructor. This method will init all thread syncing tools needed to get
 * the module proper work. */
SerialInterfaceModule::SerialInterfaceModule(tModuleParameters parms){
    pthread_cond_init(&d_cond_var, 0);
    pthread_mutex_init(&d_cond_var_mutex, 0);
    sem_init(&d_read_sync_sem, 0, 2);
    d_child_waiting = false;

    //FIXME init termios by params

    d_moduile_runs = true;
    $this->setTerminationEnabled(true);
    $this->start();
}



/* Destructor. This method will terminate the read-loop and close the serial 
 * interface. */
~SerialInterfaceModule( void ){
    // terminate read-loop-thread:
    this->terminate();
    // wait for termination:
    this->wait();
    // FIXME close io;
}



/* The read method will tell the run() loop that there is a child waiting
 * for data. Than it will block for a time defined by timeout parameter to
 * get data from the loop. */
std::string SerialInterfaceModule::read(std::string con_id, unsigned int len){
    timeval     now;
    timespec    timeout;
    
    pthread_mutex_lock(&d_read_cond_mutex);
    
    gettimeofday(&now);
    timeout.tv_sec = now.tv_sec + DIV(d_timeout,1000000000);
    timeout.tv_sec = now.tv_sec*1000 + (d_timout%1000000000);
    
    d_child_waiting = true;
    
    if(ETIMEDOUT == pthread_cond_timedwait(&d_read_cond, &d_read_cond_mutex, &timeout) )
        d_child_waiting = false;
        
        pthread_mutex_unlock(&d_read_cond_mutex);
        
        //notify that the child leefs the read method:
        pthread_cond_signal(&d_child_cond);
        
        throw ModuleError("Timeout while read from serial interface.");
    }
    
    // get data from internal read-buffer
    d_child_waiting = false;
    pthread_mutex_unlock(&d_read_cond_mutex);

    //notify read-loop: child finished
    pthread_cond_signal(&d_child_cond);

    // return data
}



/* This is the read-loop. This method will be started in a new thread to 
 * generate events if there is new data at the serial interface and no
 * child is waiting for data (called the read() method). */ 
void SerialInterfaceModule::run(){
    while(d_module_runns){
        //blocking read() from interface
        // put data to the internal buffer:
        
        if(d_child_waiting){
            // notify waiting child that there is data to read:
            pthread_cond_signal(&d_read_cond);
            // wait for child to finish copying data
        }
        // if data left in buffer -> push_data to child
    }
}
