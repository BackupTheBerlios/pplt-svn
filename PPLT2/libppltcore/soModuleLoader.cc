/***************************************************************************
 *            soModuleLoader.cc
 *
 *  Fri Apr 28 19:04:58 2006
 *  Copyright  2006  Hannes Matuschek   
 *  hmatuschek@gmx.net
 ****************************************************************************/

#include "soModuleLoader.h"

using namespace PPLTCore;




// constructor with an empty module path list:
soModuleLoader::soModuleLoader(){ }



//destructor:
soModuleLoader::~soModuleLoader(){ 
    //FIXME the destructor should free all modules loaded!
}



void soModuleLoader::unload(cModule *module){
    std::string             id = module->Identifier();
    
    if(d_id_handle_map.end() == d_id_handle_map.find(id))
        throw ItemNotFound("Unable to find id (%s) in list -> this may cause into a memory leak!",id.c_str());
   
    if(module->isBusy())
        throw ItemBusy("Module %s is still used by one or more objects (symbols or other modules)!",module->Identifier().c_str());
    
    CORELOG_DEBUG("Destroy module "<<id);
    delete module;

    dlclose(d_id_handle_map[id]);   
    d_id_handle_map.erase(id);
}



cModule *soModuleLoader::load(std::string filename, std::string factory,
                              tModuleParameters params){
    void            *handle;
    tModuleFactory  mod_factory;
    cModule         *mod;
                                  
    if(0 == (handle = dlopen(filename.c_str(), RTLD_NOW)) ){
        throw ItemNotFound("Unable to load file %s: ",filename.c_str());
    }
    
    CORELOG_DEBUG("Try to load factory " << factory.c_str() <<
                  " from file " << filename.c_str());
    
    if(0 == (mod_factory = reinterpret_cast<tModuleFactory>(dlsym(handle, factory.c_str()))) ){
        dlclose(handle);
        throw ItemNotFound("Unable to find factory function %s() in %s!", 
                           factory.c_str(), filename.c_str());
    }        

    try{ 
        mod = mod_factory(params);
    }catch(...){
        dlclose(handle);
        throw;
    }   
    
    d_id_handle_map[mod->Identifier()] = handle;
    
    return mod;    
}




cModule *soModuleLoader::load(std::string filename, std::string factory,
                              cModule *parent, std::string address,
                              tModuleParameters params){
    void                *handle;
    tInnerModuleFactory mod_factory;
    cModule             *mod;
                                  
    if(0 == (handle = dlopen(filename.c_str(), RTLD_NOW)) ){
        throw ItemNotFound("Unable to load file %s: ", filename.c_str());
    }
    
    if(0 == (mod_factory = reinterpret_cast<tInnerModuleFactory>(dlsym(handle, factory.c_str()))) ){
        dlclose(handle);
        throw ItemNotFound("Unable to find factory function %s() in %s!", 
                           factory.c_str(), filename.c_str());
    }        
    
    try{ 
        mod = mod_factory(parent, address ,params);
    }catch(...){
        dlclose(handle);
        throw;
    }   
    
    d_id_handle_map[mod->Identifier()] = handle;
    
    return mod;    
}

