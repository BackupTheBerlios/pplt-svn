#ifndef PPLT_CSTREAMCONNECTION_H
#define PPLT_CSTREAMCONNECTION_H

#include "cConnection.h"

namespace PPLTCore{

    class cStreamConnection : public cConnection{
        private:
            char    *d_buffer;
            int     d_buffer_size;

        public:
            cStreamConnection(cModule *parent, cDisposable *child=0);
            ~cStreamConnection();

            void push(char *buffer, int len);
            void flush();

            int read(char *, int);
            int write(char *, int);
    };

}

#endif
