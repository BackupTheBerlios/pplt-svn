#ifndef PPLT_ISTREAMMODULE_H
#define PPLT_ISTREAMMODULE_H

#include "cModule.h"

/**\file iStreamModule.h
 * \brief This file contains the iStreamModule interface definition.
 *
 * The iStreamModule interface have to be implemented by any module
 * that wants to provide a data stream. */
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
