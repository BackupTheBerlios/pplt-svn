#ifndef PPLT_IVALUEMODULE_H
#define PPLT_IVALUEMODULE_H

#include "cModule.h"

namespace PPLTCore{

    class iValueModule{
        public:
            virtual TT get(std::string) = 0;
            virtual void set(std::string, TT) = 0;
    };


}

#endif
