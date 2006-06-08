#include "Portability.h"

using namespace PPLTCore;





bool PPLTCore::isAbsolutePath(std::string path){
    //FIXME Not portable:
    return path[0] == PPLT_PATH_SEPERATOR;
}



std::string PPLTCore::CWD( void ){
    //FIXME The function cwd() may not avaliable at all platforms:
    char            *cwd = getcwd(NULL, 0);
    std::string     cwd_s(cwd);
    free(cwd);
    return cwd_s;
}



std::string PPLTCore::ExtendPath(std::string path){
    return PPLTCore::ExtendPath(path, PPLTCore::CWD());
}



std::string PPLTCore::ExtendPath(std::string path, std::string base_path){
    if (PPLTCore::isAbsolutePath(path))
        return PPLTCore::NormalizePath(path);

    return NormalizePath(base_path + "/" + path);
}    



std::string PPLTCore::NormalizePath(std::string path){
    std::list<std::string>  path_list;
    std::string             new_path;
    std::list<std::string>  new_path_list;

    path_list   = SplitPath(path);

    for(std::list<std::string>::iterator it = path_list.begin();
        it != path_list.end(); ++it){
            if((*it) == ".")
                continue;
            if((*it) == ".."){
                if(!new_path_list.empty())
                    new_path_list.pop_back();
                continue;
            }
            new_path_list.push_back((*it));
    }   

    for(std::list<std::string>::iterator it = new_path_list.begin();
        it != new_path_list.end(); ++it){
            new_path += PPLT_PATH_SEPERATOR + (*it);
    }    
    
    return new_path;    
}



std::list<std::string> PPLTCore::SplitPath(std::string path){
    return SplitPath(path, PPLT_PATH_SEPERATOR);
}



std::list<std::string> PPLTCore::SplitPath(std::string path, char path_sep){
    std::list<std::string>      path_list;
    std::string                 tmp;
    
    for(std::string::iterator it = path.begin();
        it != path.end(); ++it){
            if((*it) == path_sep){
                if(!tmp.empty())
                    path_list.push_back(tmp);
                tmp = "";
            }else{
                tmp += *it;
            }    
    }
    if(!tmp.empty())
        path_list.push_back(tmp);

    return(path_list);
}
