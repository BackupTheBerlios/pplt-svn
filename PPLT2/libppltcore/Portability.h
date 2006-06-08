#ifndef PPLT_PORTABILITY_H
#define PPLT_PORTABILITY_H

#include <iostream>
#include <string>
#include <list>
#include <unistd.h>


namespace PPLTCore{
    
    #define PPLT_PATH_SEPERATOR     '/'
   
    /** Retunrs true if the given path is an absolute path. */
    bool isAbsolutePath(std::string path);

    
    /** Retunrs the current working path. */
    std::string CWD();


    /** Split the path. */
    std::list<std::string> SplitPath(std::string path, char path_sep);
    std::list<std::string> SplitPath(std::string path);


    /** Normalize path names.
     * This function normalizes path names like /any//path/../to/ to /any/to. 
     * \note This function treads all pathes as absolute pathes:*/
    std::string NormalizePath(std::string path);

    
    /** Extend path names.
     * This function takes a path name if it is a relative path name then the
     * current pwd is added and the path will be normalized. */
    std::string ExtendPath(std::string path);
    std::string ExtendPath(std::string path, std::string base_path);



    
}

#endif

