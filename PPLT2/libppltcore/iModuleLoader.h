/***************************************************************************
 *            iModuleLoader.h
 *
 *  2006-06-15
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

/** \file iModuleLoader.
 * This file contians the definition of the interface of a module loader. */

#ifndef PPLTCORE_IMODULE_LOADER
#define PPLTCORE_IMODULE_LOADER

#include "cModule.h"

namespace PPLTCore{
   
    /** This class defines the interface for all module loaders. */
    class iModuleLoader{
        public:
            /** Pure virtual destructor. */
            virtual ~iModuleLoader(){ };


            /** Loads a root module.
             * This method have to be implemented by any module loader! This 
             * method should load and instance a new (root-)module. A root 
             * module is a module with no parent module! 
             * 
             * @param filename   This is the path to the file containing the 
             *      module.
             * @param factory    This is the name of the factory fuction or
             *      the class name of the module.
             * @param parameters This is the map of the parameters the the
             *      module may need to be instanced.
             */  
            virtual cModule *load(std::string filename, std::string factory,
                                  tModuleParameters params) = 0;


            /** Loads a module.
             * This method have to be implemented by any module loader! This 
             * method should load and instance a new inner module. A inner 
             * module is a module with a parent module.Parameters are 
             * the file where the module definitions are strored, the name 
             * of the factory for the module class or the name of the 
             * module class, the parent of the loaded module, the address used
             * to connect the new module with the parent and the parameters 
             * the module my need to be instanced. 
             * 
             * @param filename   Path and name to the file that contains the 
             *      module.
             * @param factory    Name of the factory function or of the class 
             *      that have to be instanced.
             * @param parent     Parent module of the new module.
             * @param address    The address used to conenct the new module to
             *      the parent.
             * @param parameters The Parameter map my used to init the module. */ 
            virtual cModule *load(std::string filename, std::string factory,
                                  cModule *parent, std::string address,
                                  tModuleParameters params) = 0;


            /** Unloads a module.
             * This method have to be implemented by any module loader. This 
             * method should unload the given module and cleanup the module 
             * contex ie close the file that contains the module. */
            virtual void unload(cModule *module) = 0;                                  
    };                                  
}

#endif

