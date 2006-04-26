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

#include "../include/Logging.h"
#include "../include/Exceptions.h"
#include "../include/cInnerModule.h"
#include "../include/iStreamModule.h"
#include "../include/cStreamConnection.h"

namespace PPLTPlugin{

    class HexDumpModule
    :public PPLTCore::cInnerModule, public PPLTCore::iStreamModule{
        private:
            PPLTCore::cStreamConnection   *d_my_child;
            std::string hexLine(char *buff, int offset, int len=8);

        public:
            HexDumpModule(PPLTCore::cModule *, std::string, 
                          PPLTCore::tModuleParameters);

            PPLTCore::cConnection *connect(std::string addr,
                                           PPLTCore::cDisposable *child=0);
            void disconnect(std::string);

            int read(std::string, char *, int);
            int write(std::string, char *, int);

            void data_notify();
    };

}

#endif
