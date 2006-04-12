#include "../include/cValueConnection.h"

using namespace PPLTCore;

/* Constructor: set last_update and cache_time to 0 */
cValueConnection::cValueConnection(cModule *parent, cDisposable *child): cConnection(parent, child){
    d_cache_time.tv_sec = 0; d_cache_time.tv_usec = 0;
    d_last_update.tv_sec = 0; d_last_update.tv_usec = 0;
}

/* Destructor */
cValueConnection::~cValueConnection(){ }


/* Set the timestamp of the last update to now. */
void cValueConnection::UpdateTimestamp(){
    struct ntptimeval   now;
    // get current time:
    ntp_gettime(&now);
    // store it in d_last_update:
    d_last_update.tv_sec = now.time.tv_sec;
    d_last_update.tv_usec = now.time.tv_usec;
}


/* Checks if now - last_update < cache_time */
bool cValueConnection::CacheTimeElapsed(){
    struct ntptimeval   now;
    // get current time:
    ntp_gettime(&now);
    // decides if the cache-time is elapsed
    if( (now.time.tv_sec - d_last_update.tv_sec) < d_cache_time.tv_sec)
        return false;
    if( now.time.tv_sec - d_last_update.tv_sec == d_cache_time.tv_sec &&
        now.time.tv_usec - d_last_update.tv_usec  <= d_cache_time.tv_usec)
        return false;
    return true;
}


/* Returns the current cacheing time in seconds. */
double cValueConnection::CacheTime(){
    return (double)d_cache_time.tv_sec + ((double)(d_cache_time.tv_usec)/1000000);
}

/* Sets the cachetime in seconds */
void cValueConnection::CacheTime(double t){
    d_cache_time.tv_sec = (int)t;
    t -= (int)t;
    d_cache_time.tv_usec = (int)(t*100000);
    CORELOG_DEBUG("Set cachetime to "<< d_cache_time.tv_sec << "s and "<< d_cache_time.tv_usec << "µs");
}
