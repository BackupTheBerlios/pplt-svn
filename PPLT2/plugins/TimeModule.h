/***************************************************************************
 *            TimeModule.h
 *
 *  Sun Apr 30 00:16:55 2006
 *  Copyright  2006  User
 *  Email
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
 
#ifndef PLUGIN_TIMEMODULE_H
#define PLUGIN_TIMEMODULE_H

#include "../libppltcore/ppltcore.h"

extern "C"{
    PPLTCore::cModule   *TimeModuleFactory(PPLTCore::tModuleParameters params);
};

namespace PPLTPlugin{
    class TimeModule: public PPLTCore::cModule, 
                      public PPLTCore::iFloatModule{
        public:
            TimeModule(PPLTCore::tModuleParameters params);
    
            PPLTCore::cConnection *connect(std::string addr, 
                                           PPLTCore::cDisposable *child=0);
            
            void disconnect(std::string con_id);
    
            double get(std::string con_id);
            void set(std::string con_id, double value);
    };            
}

#endif
