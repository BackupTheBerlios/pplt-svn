#ifndef PPLT_ISEQUENCEMODULE_H
#define PPLT_ISEQUENCEMODULE_H

#include "cModule.h"

/**\file iSequenceModule.h
 * \brief This file contains the iSequenceModule interface definition. */
namespace PPLTCore{

    /** The iStequenceModule interface.
     *
     * The a sequcence module is something a mixture of a stream module
     * (iStreamModule) and a module that proviedes values. A sequcene module
     * provides data like the stream module but not as a buffred stream. It
     * provides the data in a datagram called sequence. This is like a
     * UDP socket under Linux. If a connection calls recv() it will get
     * a newly alloceated string that contains the complete size of the
     * data. */
    class iSequenceModule{
        public:
            virtual ~iSequenceModule();

            virtual std::string recv(std::string con_id) = 0;
            virtual void send(std::string con_id, std::string data) = 0;

    };

}

#endif
