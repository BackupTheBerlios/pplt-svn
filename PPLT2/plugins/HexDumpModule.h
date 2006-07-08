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
 
/** \file HexDumpModule.h */

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
#include "../libppltcore/cSequenceConnection.h"


extern "C"{
    /** Factory function for the HexDumpModule.
     * This function is secessary to create a module class from a shared 
     * library, because the libdl doesn't support the loading of classes. */
    PPLTCore::cModule *HexDumpModuleFactory(PPLTCore::cModule *parent, 
                                            std::string addr, 
                                            PPLTCore::tModuleParameters params);
};



namespace PPLTPlugin{


    /** The hexdump module class.
     * This module can be used to investigate the communication between stream 
     * modules. Simply plug this module between the module to investigate and 
     * read the data exchanged.
     * 
     * Therefor there are two possebilities to read the data. This module will
     * allways dump the trafic into the logging system with the flag DEBUG. 
     * The other way is to connect a to this module with the address "dump".
     * You will get a sequence connection that will inform you each time data
     * is exchanged. You will get lines of the form:
     *      $$direction$$ $$length$$ $$HEXDATA$$ $$printable$$. 
     * direction is one of "up", "down" or "push", length is max 8 bytes, 
     * hexdata is the hex and printable the printable representation of the 
     * data exchanged. */
    class HexDumpModule
    :public PPLTCore::cInnerModule, 
     public PPLTCore::iStreamModule, 
     public PPLTCore::iSequenceModule{
        private:
            std::string hexLine(std::string buff, int offset);
            void        notify_children(std::list<std::string> hexlines, std::string func);

        public:
            HexDumpModule(PPLTCore::cModule *, std::string, 
                          PPLTCore::tModuleParameters);

            PPLTCore::cConnection *connect(std::string addr,
                                           PPLTCore::cDisposable *child=0);

            void disconnect(std::string con_id);
            bool isBusy();

            std::string read(std::string con_id, unsigned int len);
            unsigned int write(std::string con_id, std::string data, unsigned int len);

            std::string recv(std::string con_id);
            void send(std::string con_id, std::string data);

            void data_notify();
    };

}

#endif
