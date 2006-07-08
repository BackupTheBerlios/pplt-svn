/***************************************************************************
 *            cStreamConnection.h
 *
 *  Sun Apr 23 01:17:38 2006
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
 
#ifndef PPLT_CSTREAMCONNECTION_H
#define PPLT_CSTREAMCONNECTION_H

#include <pthread.h>

#include "cConnection.h"
#include "iStreamModule.h"
#include "Exceptions.h"
#include "Logging.h"

/**\file cStreamConnection.h
 * \brief This file contains the definition of the cStreamConnection
 * class.
 *
 * The cStreamConnection class is used to connect a iStreamModule
 * with an other module or symbol. */
namespace PPLTCore{

    /** The cStreamConnection class.
     *
     * This class implements the connection between a iStreamModule
     * and an other module or symbol. By this connection is is
     * possible to read from the module like to read from a file.
     * C++ style stream is not(yet) provided. */
    class cStreamConnection : public cConnection{
        private:
            std::string     d_buffer;
            pthread_mutex_t d_buffer_lock;

        public:
            /** Constructor.
             *
             * The constructor needs at least one parameter. The parameter
             * \c parent defines the parent module. This module have to
             * implement at least the class cModule and the iStreamModule
             * interface. because this connection espects the methods
             * read()/write(). The second (optional) parameter \c child defines
             * the child module of the connection. \b Note: if there is no child
             * module given, each push() method-call will raise a CoreError
             * exception to indicate that there is no child module to inform.*/
            cStreamConnection(cModule *parent, cDisposable *child=0);
            ~cStreamConnection();

            /** The push() method stores the given data and notify child.
             *
             * This method stores the given data into the internal buffer
             * and informs the child module about the data by calling his
             * data_notify() method. The child will get the data by calling
             * the read() method of this connection.
             *
             * This method is used by the parent module to inform indirect
             * the child module that there is not requested data for it.
             * By this it is possible to implement a asynchron communication.
             * If a moulde needs to inform the child direct and not storing
             * the data it can use the push() method without any parameters. */
            void push(std::string data, unsigned int len);

            /** push() callback
             *
             * Informs the child directly about unespected data without storing
             * the data into the connection buffer. This is mostly usefull if
             * there is only one child and the size of the data is not known
             * but the child may determ the size. */
            void push();


            /** Flushes the internal buffer */
            void flush();


            /** This method returns the number of bytes left in the connection 
             *  buffer.*/
            unsigned int buff_len();

            /** The read() method.
             *
             * This method will be used by the child to read data from the
             * parent. The method will try to read max. len bytes from the
             * parent and return them by the given string. 
             * @param len   Max number of bytes read.*/
            std::string read(unsigned int len);

            /** The write() method.
             *
             * This method is used by the child to write data to the parent. 
             * @param data  The string of data to send.
             * @parma len   Defines the number of bytes send. */
            unsigned int write(std::string data, unsigned int len);
    };

}

#endif
