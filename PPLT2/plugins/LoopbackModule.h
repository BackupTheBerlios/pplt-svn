/***************************************************************************
 *            LoopbackModule.h
 *
 *  Sun Apr 23 01:15:16 2006
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
 
#ifndef PPLT_PLUGIN_LOOPBACK_H
#define PPLT_PLUGIN_LOOPBACK_H

#include "../libppltcore/cModule.h"
#include "../libppltcore/iStreamModule.h"
#include "../libppltcore/cConnection.h"
#include "../libppltcore/cStreamConnection.h"
#include "../libppltcore/cDisposable.h"
#include "../libppltcore/Logging.h"
#include "../libppltcore/Exceptions.h"

extern "C"{
    PPLTCore::cModule   *LoopbackModuleFactory(PPLTCore::tModuleParameters);   
};    


namespace PPLTPlugin{

    class LoopbackModule
    : public PPLTCore::cModule,
      public PPLTCore::iStreamModule
    {
        private:
            PPLTCore::cConnection *GetTheOtherOne(std::string addr);
            void *notify_child(void *data);
        
        public:
            LoopbackModule(PPLTCore::tModuleParameters);

            PPLTCore::cConnection *connect(std::string addr,
                                           PPLTCore::cDisposable *child=0);
            void disconnect(std::string);

            std::string read(std::string con_id, int len);
            int write(std::string, std::string data, int len);
    };
}


#endif
