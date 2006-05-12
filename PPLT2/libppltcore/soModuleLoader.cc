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



// constructor with a module list conatining only [path] as element:
soModuleLoader::soModuleLoader(std::string path){
    d_module_paths.push_back(path);
}



// Constructor with the module path list == paths:
soModuleLoader::soModuleLoader(std::list<std::string> paths){
    d_module_paths.merge(paths);
}



std::string soModuleLoader::find_file(std::string filename){
    std::string     so_file_path;
    
    /**\todo if file starts with a "/" than simply return the filename */
    
    for(std::list<std::string>::iterator it = d_module_paths.begin();
        it != d_module_paths.end();
        ++it){
            so_file_path = *it + "/" + filename;
            if(0 == access(so_file_path.c_str(), F_OK|R_OK))
                return (so_file_path);
    }            
    throw ItemNotFound("No \"%s\" file can be found (with read right) "\
                       "in module paths.", filename.c_str());
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
    std::string     so_file_path;
    void            *handle;
    tModuleFactory  mod_factory;
    cModule         *mod;
                                  
    so_file_path = find_file(filename);
    if(0 == (handle = dlopen(so_file_path.c_str(), RTLD_NOW)) ){
        throw CoreError("Unable to load file %s: ",so_file_path.c_str());
    }
    
    CORELOG_DEBUG("Try to load factory " << factory.c_str() <<
                  " from file " << so_file_path.c_str());
    
    if(0 == (mod_factory = reinterpret_cast<tModuleFactory>(dlsym(handle, factory.c_str()))) ){
        dlclose(handle);
        throw ItemNotFound("Unable to find factory function %s() in %s!", 
                           factory.c_str(), so_file_path.c_str());
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
    std::string         so_file_path;
    void                *handle;
    tInnerModuleFactory mod_factory;
    cModule             *mod;
                                  
    so_file_path = find_file(filename);
    if(0 == (handle = dlopen(so_file_path.c_str(), RTLD_NOW)) ){
        throw CoreError("Unable to load file %s: ",so_file_path.c_str());
    }
    
    if(0 == (mod_factory = reinterpret_cast<tInnerModuleFactory>(dlsym(handle, factory.c_str()))) ){
        dlclose(handle);
        throw ItemNotFound("Unable to find factory function %s() in %s!", 
                           factory.c_str(), so_file_path.c_str());
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



void soModuleLoader::addModulePath(std::string path){
    d_module_paths.push_back(path);
}



void soModuleLoader::addModulePath(std::list<std::string> paths){
    d_module_paths.merge(paths);
}



void soModuleLoader::remModulePath(std::string path){
    d_module_paths.remove(path);    
}



void soModuleLoader::remModulePath(std::list<std::string> paths){
    for(std::list<std::string>::iterator it = paths.begin();
        it != paths.end();
        ++it){
            d_module_paths.remove(*it);
    }            
}



void soModuleLoader::clearModulePath(){ 
   d_module_paths.clear();
}



std::list<std::string> soModuleLoader::getModulePaths(){ 
    return d_module_paths;
}

