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

#include "../include/cModule.h"
#include "../include/iStreamModule.h"
#include "../include/cConnection.h"
#include "../include/cStreamConnection.h"
#include "../include/cDisposable.h"
#include "../include/Logging.h"
#include "../include/Exceptions.h"


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

            int read(std::string, char *, int);
            int write(std::string, char *, int);
    };
}


#endif
