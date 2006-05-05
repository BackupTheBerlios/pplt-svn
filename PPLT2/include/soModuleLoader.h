/***************************************************************************
 *            soModuleLoader.h
 *
 *  Fri Apr 28 18:54:18 2006
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
 
#ifndef PPLT_SO_MODULE_LOADER_H
#define PPLT_SO_MODULE_LOADER_H

#include <dlfcn.h>
#include <unistd.h>
#include <list>
#include "cModule.h"
#include "Exceptions.h"


namespace PPLTCore{
    typedef cModule *(*tModuleFactory)(tModuleParameters);
    
    typedef cModule *(*tInnerModuleFactory)(cModule *, std::string, 
                                            tModuleParameters);
    
    class soModuleLoader{
        private:
            std::list<std::string>  d_module_paths;
        
        protected:
            std::string             find_file(std::string filename);
        
        public:
            soModuleLoader();
            soModuleLoader(std::string path);
            soModuleLoader(std::list<std::string> paths);
        
            cModule *load(std::string filename, std::string factory,
                          tModuleParameters params);
        
            cModule *load(std::string filename, std::string factory,
                          cModule *parent, std::string address,
                          tModuleParameters params);
        
            void addModulePath(std::string path);
            void addModulePath(std::list<std::string> paths);
            void remModulePath(std::string path);
            void remModulePath(std::list<std::string> paths);
            void clearModulePath();
            std::list<std::string> getModulePaths();        
    };        
}

#endif
