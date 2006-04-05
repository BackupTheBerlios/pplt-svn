#include "cStreamConnection.h"
#include "iStreamModule.h"
#include "Exceptions.h"

using namespace PPLTCore;

cStreamConnection::cStreamConnection(cModule *parent, cDisposable *child) : cConnection(parent, child){
    // check if parent match cStreamModule:
    if(!dynamic_cast<iStreamModule *>(parent) )
            throw Error("Can't create new StreamConnection! Invalid parent module!");
}

cStreamConnection::~cStreamConnection(){
}

int cStreamConnection::read(char *buffer, int len){
    return dynamic_cast<iStreamModule *>(d_parent_module)->read(Identifier(), buffer, len);
}

int cStreamConnection::write(char *buffer, int len){
    return dynamic_cast<iStreamModule *>(d_parent_module)->write(Identifier(), buffer, len);
}
