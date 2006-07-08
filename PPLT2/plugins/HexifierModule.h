/***************************************************************************
 *            HexifierModule.h
 *
 *  2006-06-21
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
 
/** \file HexifierModule.h */

#ifndef PPLT_PLUGIN_HEXIFIER_H
#define PPLT_PLUGIN_HEXIFIER_H

#include <iostream>
#include <streambuf>
#include <string>
#include <iomanip>
#include "../libppltcore/Logging.h"
#include "../libppltcore/Exceptions.h"
#include "../libppltcore/cInnerModule.h"
#include "../libppltcore/iStreamModule.h"
#include "../libppltcore/iSequenceModule.h"
#include "../libppltcore/cStreamConnection.h"
#include "../libppltcore/cSequenceConnection.h"


extern "C"{
    PPLTCore::cModule *HexifierModuleFactory(PPLTCore::cModule *parent, 
                                             std::string addr, 
                                             PPLTCore::tModuleParameters params);
};

namespace PPLTPlugin{

    class HexifierModule: 
        public PPLTCore::cInnerModule, 
        public PPLTCore::iStreamModule,
        public PPLTCore::iSequenceModule
    {
        private:
            std::string hexify(std::string data);
            std::string unhexify(std::string data);

        public:
            HexifierModule(PPLTCore::cModule *parent, std::string addr,
                           PPLTCore::tModuleParameters parameters);
            ~HexifierModule();

            PPLTCore::cConnection *connect(std::string addr, 
                                          PPLTCore::cDisposable *child=0);
            void disconnect(std::string con_id);

            void data_notify();

            std::string read(std::string con_id, unsigned int len);
            unsigned int write(std::string con_id, std::string data, unsigned int len);

            std::string recv(std::string con_id);
            void send(std::string con_id, std::string data);
    };

}

#endif

