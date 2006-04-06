#ifndef PPLT_VALUECONNECTION_H
#define PPLT_VALUECONNECTION_H

#include "cConnection.h"
#include "Logging.h"
#include <sys/timex.h>

namespace PPLTCore{

    class cValueConnection: public cConnection{
        private:
            struct timeval  d_last_update;
            struct timeval  d_cache_time;

        protected:
            /**Updates the timestamp of the last cache update to now.*/
            void UpdateTimestamp();
            /**Retuns true if last_update-now < cache_time */
            bool CacheTimeElapsed();

        public:
            cValueConnection(cModule *parent, cDisposable *child=0);
            virtual ~cValueConnection();

            /**Returns the current caching time in seconds.*/
            double CacheTime();
            /**Sets the caching time in seconds.*/
            void CacheTime(double time);

            virtual int Integer() = 0;
            virtual void Integer(int) = 0;

            virtual std::string String() = 0;
            virtual void String(std::string) = 0;
    };

}


#endif
