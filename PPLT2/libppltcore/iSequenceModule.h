/***************************************************************************
 *            iSequenceModule.h
 *
 *  Sun Apr 23 01:18:13 2006
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
            virtual ~iSequenceModule(){};

            virtual std::string recv(std::string con_id) = 0;
            virtual void send(std::string con_id, std::string data) = 0;

    };

}

#endif
