/***************************************************************************
 *            RandomModule.h
 *
 *  Sun Apr 23 01:15:45 2006
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
 
#ifndef PLUGIN_RANDOMMODULE_H
#define PLUGIN_RANDOMMODULE_H

#include "../include/Logging.h"
#include "../include/Exceptions.h"
#include "../include/cModule.h"
#include "../include/iStreamModule.h"
#include "../include/iIntegerModule.h"
#include "../include/cConnection.h"
#include "../include/cIntegerConnection.h"
#include "../include/cStreamConnection.h"






namespace PPLTPlugin{

    class RandomModule
    :public PPLTCore::cModule,
     public PPLTCore::iStreamModule, 
     public PPLTCore::iIntegerModule {
     
        public:
            RandomModule();

            PPLTCore::cConnection *connect(std::string, PPLTCore::cDisposable *child = 0);

            void disconnect(std::string);

            void enable_events();
            void disable_events();

            int read(std::string, char *, int);
            int write(std::string, char *, int);

            int get(std::string);
            void set(std::string, int);
    };

}

#endif
