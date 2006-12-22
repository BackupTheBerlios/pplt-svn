#include <python2.4/Python.h>
//#include <apr.h>

typedef struct{
    PyObject    *module;
} ppltModule;


typedef struct{
    PyObject    *_ImpPack;
    PyObject    *_ImpPackDict;
    PyObject    *_ImpClass;
    PyObject    *importer;

    //FIXME methods...
} ppltImporter;


/** This function initialize the python-iterpreter and instance a CImporter 
 *  class from the pplt python-package. */
ppltImporter *ppltImporter_Init( void );

/** This function will destroy the importer and finalize the python 
 *  interpreter. */
int ppltImporter_Destroy(ppltImporter *);



/** This method will load a pplt-module or assembly using the given 
 * importer. */
ppltModule *ppltImporter_Load(ppltImporter *, char *, apr_hash_t *);
/** This method will load a inner module or assembly using the given importer
 *  and attach it to the given module/assembly using the given address. */
ppltModule *ppltImporter_LoadInner(ppltImporter *, char *, apr_hash_t *, ppltModule *, char *);
