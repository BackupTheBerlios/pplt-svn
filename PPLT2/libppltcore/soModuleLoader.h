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

/** This \file soModuleLoader.h contains the definitions of the module loader
 * for shared object files. (.so) */

#ifndef PPLT_SO_MODULE_LOADER_H
#define PPLT_SO_MODULE_LOADER_H

#include <dlfcn.h>
#include <unistd.h>
#include <list>

#include "cModule.h"
#include "Exceptions.h"
#include "cObject.h"
#include "iModuleLoader.h"



namespace PPLTCore{
    /** This type defines the interface for a factory function to generate 
     *  (root) modules.
     * A factory function of a root module should be of this type. It is
     * secessary to write a simple function (of this type) to create a 
     * module because the C libdl can't handle with classes but with 
     * functions. So a factory function for each exported module have to 
     * be written to create a module. This function should take all 
     * paramters a module needs, in this case only the module parameters 
     * and should return a newly created module instance. */
    typedef cModule *(*tModuleFactory)(tModuleParameters);
   
    /** This type defines the interface for a inner module factory function.
     * This type should be used for all factory function of inner module.
     * Additionaly to the tModuleFactory this one takes the pointer to the
     * parent module (all inner modules have one) and the address for the 
     * connection to the parent. 
     * @see tModuleFactory*/
    typedef cModule *(*tInnerModuleFactory)(cModule *, std::string, 
                                            tModuleParameters);
   
    /** This class implements a module loader for shread object files.
     * This class implements the iModuleLoader interface. So it is a common 
     * module loader. This class is able to instance modules from shared 
     * object files (so-files) using factory functions. 
     * @see load */
    class soModuleLoader: public iModuleLoader{
        private:
            /** map of loaded module id to there source .so files */
            std::map<std::string, void *>  d_id_handle_map;    

        protected:

        public:
            /** Constructor. */
            soModuleLoader();
       
            /** Destructor.
             * @todo The destructor have to free all remaining modules! */
            ~soModuleLoader();

            /** This method loads a root module from the given file.
             * This method can be used to load and instance a module from the
             * given file. The factory should be the name of the factory function 
             * that creates the instance of the module. The tModuleParameters are 
             * used to instance the module.
             * @see tModuleFactory 
             * @param filename  The path to the module (package) file.
             * @param factory   The name of the fayctory function.
             * @param params    The parameters the module may need to be 
             *                  instanced.*/
            cModule *load(std::string filename, std::string factory,
                          tModuleParameters params);
       

            /** This method will load a inner module from the given file.  
             * This method can be used to load a inner module from the given
             * file using the given factory function. @see tModuleFactory
             * Aditionaly to the load mathod for root modules, this one takes
             * the parent module and the address used to connect the new module
             * to the parent.
             * @see load
             * @param filename  The file name of the module (package) file.
             * @param factory   The name of the factory function.
             * @param parent    A pointer to the parent module.
             * @param address   The address used to connect the new module to 
             *                  the parent.
             * @param parms     The parameters the module may needs to be instanced. */
            cModule *load(std::string filename, std::string factory,
                          cModule *parent, std::string address,
                          tModuleParameters params);
            
           
           /** This method should be used to destroy and free a module.
             * This method should be used to destroy a module loaded by a 
             * instance of this class. */
            void unload(cModule *mod);
    };        
}

#endif
