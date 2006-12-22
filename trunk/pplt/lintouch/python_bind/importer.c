#include "importer.h"

ppltImporter *ppltImporter_Init( void ){
    ppltImporter    *imp;
    
    // Init Python interpreter:
    Py_Initialize();

    //alloc memory for importer
    imp = calloc(1, sizeof(ppltImporter));

    //Get python-module "pplt.Importer"
    imp->_ImpPack = PyImport_Import(PyString_FromString("pplt.Importer"));
    if(NULL == imp->_ImpPack){
        free(imp);
        Py_Finalize();
        return NULL;
    }
    
    // get the CImporter class from pplt.Importer module
    imp->_ImpPackDict = PyModule_GetDict(imp->_ImpPack);
    imp->_ImpClass    = PyDict_GetItemString(imp->_ImpPackDict, "CImporter");
    if (NULL == imp->_ImpClass || !PyCallable_Check(imp->_ImpClass) ){
        Py_DECREF(imp->_ImpPackDict);
        Py_DECREF(imp->_ImpPack);
        free(imp);
        Py_Finalize();
        return NULL;
    }

    // Instance the CImporter
    imp->importer = PyObject_CallObject(imp->_ImpClass, PyTuple_New(0));
    if(NULL == imp->importer){
        Py_DECREF(imp->_ImpPackDict);
        Py_DECREF(imp->_ImpPack);
        free(imp);
        Py_Finalize();
        return NULL;
    }

    //FIXME add methods to importer!
    return imp;
}


int ppltImporter_Destroy(ppltImporter *imp){
    if (NULL == imp)
        return -1;
    
    Py_DECREF(imp->importer);
    Py_DECREF(imp->_ImpClass);
    Py_DECREF(imp->_ImpPackDict);
    Py_DECREF(imp->_ImpPack);
    free(imp);
    Py_Finalize();
}



int main(void){
    ppltImporter    *imp;
    PyObject    *rand_mod, *con_obj, *value;

    if(NULL == (imp = ppltImporter_Init()) ){
        PyErr_Print();
        fprintf(stderr, "Unable to init importer!");
    }

    rand_mod = PyObject_CallMethod(imp->importer, "load", "(s)","random_module");
    if(NULL == rand_mod){
        PyErr_Print();
        fprintf(stderr, "Unable to load: random_module\n");
        return 1;
    }        
   
    con_obj = PyObject_CallMethod(rand_mod, "connect", "(s)","integer");
    if(NULL == con_obj){
        PyErr_Print();
        fprintf(stderr,"oops...\n");
        return 1;
    }

    value = PyObject_CallMethod(con_obj, "get", NULL);
    printf("Value of get(): %i\n",PyInt_AsLong(value));
    
    
    ppltImporter_Destroy(imp);
return 0;
}
