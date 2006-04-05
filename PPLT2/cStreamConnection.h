#ifndef PPLT_CSTREAMCONNECTION_H
#define PPLT_CSTREAMCONNECTION_H

#include "cConnection.h"

namespace PPLTCore{

    class cStreamConnection : public cConnection{
        public:
            cStreamConnection(cModule *parent, cDisposable *child=0);
            ~cStreamConnection();

            int read(char *, int);
            int write(char *, int);
    };

}

#endif
