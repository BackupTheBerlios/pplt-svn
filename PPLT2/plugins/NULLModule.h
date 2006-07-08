/***************************************************************************
 *            NULLModule.h
 *
 *  Sun Apr 23 01:15:30 2006
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
 
#ifndef PPLT_PLUGIN_NULLMODULE_H
#define PPLT_PLUGIN_NULLMODULE_H

#include <string>

#include "../libppltcore/iStreamModule.h"
#include "../libppltcore/cStreamConnection.h"
#include "../libppltcore/cConnection.h"
#include "../libppltcore/cDisposable.h"


/** This factory function is needed to load a class instance from a shared 
 *  object using the libdl. */
extern "C"{
    PPLTCore::cModule *NULLModuleFactory(PPLTCore::tModuleParameters);
};




namespace PPLTPlugin{

    class NULLModule : public PPLTCore::cModule, public PPLTCore::iStreamModule{
        public:
            NULLModule(PPLTCore::tModuleParameters params);

            PPLTCore::cConnection *connect(std::string);
            PPLTCore::cConnection *connect(std::string, PPLTCore::cDisposable *);
            
            void disconnect(std::string);

            std::string read(std::string con_id, unsigned int len);
            unsigned int write(std::string con_id, std::string data, unsigned int len);
    };

}



#endif
