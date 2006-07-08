#include "pyModuleLoader.h"

using namespace PPLTCore;


// init static member pyModuleLoader::d_python_initcount;
int pyModuleLoader::d_python_init_count = 0;


pyModuleLoader::pyModuleLoader(){
    if(0 >= d_python_init_count)
        Py_Initialize();
    d_python_init_count++;
}



pyModuleLoader::~pyModuleLoader(){ 
    if(--d_python_init_count <= 0){
        Py_Finalize();
        d_python_init_count = 0;
    }
}


cModule *pyModuleLoader::load(std::string filename, std::string factory, tModuleParameters params){
    PyObject    *pName, *pModule;

    pName = PyString_FromString(filename.c_str());
    pModule = PyImport_Import(pName);
    Py_DECREF(pName);

    if(0 == pModule)
        throw ItemNotFound("Unable to find (python) file \"%s\"", filename.c_str());

    //FIXME write it!    
    return 0;            
}



cModule *pyModuleLoader::load(std::string filename, std::string factory, cModule *parent, std::string address, tModuleParameters params){
    // FIXME write it
    return 0;
}



void pyModuleLoader::unload(cModule *mod){
}


