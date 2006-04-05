#ifndef PPLT_ISTREAMMODULE_H
#define PPLT_ISTREAMMODULE_H

#include "cModule.h"

namespace PPLTCore{

    class iStreamModule{
        public:
            iStreamModule();
            virtual ~iStreamModule();

            virtual int read(std::string, char *, int) = 0;
            virtual int write(std::string, char *, int) = 0;
    };
}

#endif
