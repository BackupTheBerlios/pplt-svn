#ifndef PPLT_CSEQUENCECONNECTION_H
#define PPLT_CSEQUENCECONNECTION_H

#include <pthread.h>

#include "cConnection.h"
#include "iSequenceModule.h"
#include "cModule.h"
#include "cDisposable.h"
#include "Logging.h"
#include "Exceptions.h"

/** \file cSequenceConnection.h
 * \brief This file contains the definition of the cSequenceConnection class.
 *
 * The sequecne connection is like the stream connection a connection that
 * links two modules (a iStreamModule and any other that can handle this
 * connection type) or a iStreamModule and a symbol.*/

namespace PPLTCore{
    /**Implementation of a sequencial connection (like UDP) between modules
     * and or symbols.
     *
     * This class implements a sequencial connection between a iSequenceModule
     * and a other module that can handle sequence connection or a symbol.
     *
     * A sequence connection basicly proviedes an interface that returns or
     * accepts a string that should contain a chunk of data. But an
     * additional interface identical to the one of the cStreamConnection is
     * provided that makes it possible to access the sequence connection like
     * a data stream. This enpowers modules that needs a stream connection to
     * use sequcence connections. The stream interface is implemented by a
     * an internal buffer. If the bufffer is empty it is filled up with a new
     * chunk of data than the read() function retunes max (len) bytes from this
     * buffer. If data is left in the buffer, you can access this data by
     * an other read() call or get the complete buffer by calling
     * recv(). The write() method is a simple wrapper for the send() method, it
     * converts the char * into a string and call send() with this string. */
    class cSequenceConnection: public cConnection{
        private:
            std::list<std::string>    d_data_cache;
            // Following attr. are used by the read()/write() methods
            // to simulate a data stream.
            char            *d_internal_buffer;
            int             d_buffer_len;
            pthread_mutex_t d_cache_lock;

        public:
            cSequenceConnection(cModule *parent, cDisposable *child=0);
            ~cSequenceConnection();

            void push();
            void push(std::string);
            void flush();

            std::string recv();
            void send(std::string data);

            int read(char *buffer, int len);
            int write(char *buffer, int len);
    };

}

#endif
