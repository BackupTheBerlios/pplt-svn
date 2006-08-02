/***************************************************************************
 *            SerialInterfaceModule.h
 *
 *  2006-07-08
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
 

#ifndef PPLTPLUGIN_SERIALINTERFACE
#define PPLTPLUGIN_SERIALINTERFACE

#include "../libppltcore/ppltcore.h"
#include "pthread.h"

extern "C"{
    PPLTCore::cModule *SerialInterfaceModuleFactory(PPLTCore::tModuleParameter params);
}

namespace PPLTPlugin{

    class SerialInterfaceModule: public cModule, public iStreamModule{
        private:
            pthread_cond_t      d_cond_var;
            pthread_mutex_t     d_cond_var_mutex;
            sem_t               d_read_sync_sem;
            bool                d_child_waiting;
            unsigned int        d_timeout;      //Timeout in nsec

        public:
            SerialInterfaceModule(PPLTCore::tModuleParameters params);

            PPLTCore::cConnection connect(std::string addr, PPLTCore::cDisposable *child = 0);

            void disconnect(std::string con_id);

            std::string read(std::string con_id, unsigned int len);
            void write(std::string con_id, std::string data, unsigned int len);
    };
}

#endif

