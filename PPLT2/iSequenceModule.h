#ifndef PPLT_ISEQUENCEMODULE_H
#define PPLT_ISEQUENCEMODULE_H

#include "cModule.h"

namespace PPLTCore{

    class iSequenceModule{
        public:
            virtual std::string *read(std::string) = 0;
            virtual void write(std::string, std::string) = 0;
    };

}

#endif
