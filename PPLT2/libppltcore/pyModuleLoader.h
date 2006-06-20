/***************************************************************************
 *            pyModuleLoader.h
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
 
/** This \file pyModuleLoader.h contains the definition of the python module 
 *  loader. */

#ifndef PPLTCORE_PYTHON_MODULE_LOADER
#define PPLTCORE_PYTHON_MODULE_LOADER

#include "python/Python.h"
#include "iModuleLoader.h"
#include "cModule.h"

namespace PPLTCore{

    /** This class implements the module loader for python modules. */
    class pyModuleLoader: public iModuleLoader{
        protected:
            /** Static counter of pyModuleLoaders.
             * This counter is used to init the python interpreter if the
             * first module loader is initialized and to stop the 
             * interpreter if the last is destroyed. */
            static int      d_python_init_count;


        public:
            /** Constructor.
             * This constuctor will init the python interpreter if the first
             * instance of this class will be created. */
            pyModuleLoader();

            /** Destructor.
             * This destructor will stop the python interpreter if the last 
             * instance of this class will be destroyed. */
            ~pyModuleLoader();

            /** This method will load and instance a new python (root-) module.
             * This class will look at the given file and try to create a new 
             * instance of the given class using the given parameters. */ 
            cModule     *load(std::string filename, std::string classname,
                              tModuleParameters params);

            /** This method will load and instance a new python (inner-) 
             *  module.                             
             * This method does quite the same but additionaly it connects
             * the new module to the given parent module using the given 
             * address.*/
            cModule     *load(std::string filename, std::string classname,
                              cModule *parent, std::string address,
                              tModuleParameters params);
    
            /** This method will destroy a loaded module. */
            void        unload(cModule *module);
    };    

}

#endif

