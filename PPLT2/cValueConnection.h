#ifndef PPLT_VALUECONNECTION_H
#define PPLT_VALUECONNECTION_H

#include "cConnection.h"

namespace PPLTCore{

    class cValueConnection: public cConnection{
        public:
            cValueConnection(cModule *parent, cDisposable *child=0);
            virtual ~cValueConnection();

            virtual int Integer() = 0;
            virtual void Integer(int) = 0;

            virtual std::string String() = 0;
            virtual void String(std::string) = 0;
    };

}


#endif
