/***************************************************************************
 *            cSequenceConnection.h
 *
 *  Sun Apr 23 01:17:18 2006
 *  Copyright  2006  Hannes Matuschek
 *  hmatuschek@gmx.net
 ****************************************************************************/

/*
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 */
 
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
            /** The constructor.
            * Takes a pointer to the parent module and optional the
            * the child, that can be notified about data (if present). */
            cSequenceConnection(cModule *parent, cDisposable *child=0);
            /** The destructor. */
            ~cSequenceConnection();
    
            /** Only informs the child about new data.
            * This method can be used if the child should only be infromed
            * that there is new data at the parent. This method will be
            * called by the parent module.*/
            void push();
        
            /** Informs the child about the new data.
            * In opertunity to the other push() call this one pushes data into 
            * the connection own buffer and then informs the child about this
            * data. If the child do the next read() or recv() call this data
            * will be returned. \b Note: This method will normally be called
            * only by the parent module. */
            void push(std::string);
            
            /** Flusches the internal connection buffer.
            * The sequence-connection can emulate a stream. To do this there is
            * an internal buffer. This method fushes (erase) this buffer.*/
            void flush();

            /** Returnes a chunk of data. 
            * This method will return a sequence of data read from the parent.
            * Or if there was data left in the buffer this method will return 
            * all this data. */
            std::string recv();
    
            /** Send a chunk of data to the parent.
            * This method will simply send the given data to the parent. */
            void send(std::string data);
    
            /** Reads len bytes from the connection.
            * This method can be used to access the sequence connection like
            * a cStreamConnection. This is relized by an internal buffer.*/
            int read(char *buffer, int len);
            
            /** Sends len bytes of buffer to the parent. */
            int write(char *buffer, int len);
    };

}

#endif
