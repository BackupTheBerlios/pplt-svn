#ifndef PPLT_IINTEGER_MODULE_H
#define PPLT_IINTEGER_MODULE_H

#include "cModule.h"

namespace PPLTCore{

    class iIntegerModule{
        public:
            iIntegerModule();
            virtual ~iIntegerModule();

            virtual int get(std::string) = 0;
            virtual void set(std::string, int) = 0;
    };

}
#endif
