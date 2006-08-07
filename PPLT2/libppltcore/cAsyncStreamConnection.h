/***************************************************************************
 *            cStreamConnection.h
 *
 *  Sun Apr 23 01:17:38 2006
 *  Copyright  2006  Hannes Matuschek
 *  hmatuschek@gmx.net
 ****************************************************************************/

#ifndef PPLTCORE_ASYNCSTREAMCONNETION
#define PPLTCORE_ASYNCSTREAMCONNETION
#include "cStreamConnection.h"

namespace PPLTCore{

    class cAsyncStreamConnection: public cStreamConnection{
        private:
            wxMutex         d_read_cond_mutex;
            wxCondition     d_read_cond;
            unsigned int    d_timeout;
            bool            d_child_reading;

        public:
            
            cAsyncStreamConnection(cModule *parent, cDisposable *child, unsigned int timeout=0);
            virtual ~cAsyncStreamConnection();

            virtual void data_notify(std::string data, unsigned int len);

            virtual std::string read(unsigned int length);

    };

}

#endif

