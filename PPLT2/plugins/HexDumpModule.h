/***************************************************************************
 *            HexDumpModule.h
 *
 *  Sun Apr 23 01:13:55 2006
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
 

#ifndef PPLT_PLUGIN_HEXDUMP_H
#define PPLT_PLUGIN_HEXDUMP_H

#include <iostream>
#include <streambuf>
#include <string>
#include <iomanip>
#include "../libppltcore/Logging.h"
#include "../libppltcore/Exceptions.h"
#include "../libppltcore/cInnerModule.h"
#include "../libppltcore/iStreamModule.h"
#include "../libppltcore/cStreamConnection.h"


extern "C"{
    PPLTCore::cModule *HexDumpModuleFactory(PPLTCore::cModule *parent, 
                                            std::string addr, 
                                            PPLTCore::tModuleParameters params);
};



namespace PPLTPlugin{

    class HexDumpModule
    :public PPLTCore::cInnerModule, public PPLTCore::iStreamModule{
        private:
            PPLTCore::cStreamConnection   *d_my_child;
            std::string                   hexLine(std::string buff, int offset);

        public:
            HexDumpModule(PPLTCore::cModule *, std::string, 
                          PPLTCore::tModuleParameters);

            PPLTCore::cConnection *connect(std::string addr,
                                           PPLTCore::cDisposable *child=0);

            void disconnect(std::string con_id);
            bool isBusy();

            std::string read(std::string con_id, int len);
            int write(std::string con_id, std::string data, int len);

            void data_notify();
    };

}

#endif
