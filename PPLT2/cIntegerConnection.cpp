#include "cIntegerConnection.h"
#include "iIntegerModule.h"
#include "Exceptions.h"
#include "cModule.h"

using namespace PPLTCore;

cIntegerConnection::cIntegerConnection(cModule *parent, cDisposable *child): cValueConnection(parent, child){
    if(0 == dynamic_cast<iIntegerModule *>(parent))
        throw Error("Unable to cast to iIntegerModule -> Connection closed!");
}

int cIntegerConnection::get(){
    iIntegerModule  *mod;

    if(0 == (mod = dynamic_cast<iIntegerModule *>(d_parent_module)) )
        throw Error("Unable to cast to iIntegerModule!");
    return mod->get(Identifier());
}

void cIntegerConnection::set(int value){
    dynamic_cast<iIntegerModule *>(d_parent_module)->set(Identifier(), value);
}

int cIntegerConnection::Integer(){ return get(); }
void cIntegerConnection::Integer(int value){ set(value); }

std::string cIntegerConnection::String(){
    //FIXME: Implement str -> int convert
    throw NotImplementedYet("Mail author!");
}

void cIntegerConnection::String(std::string value){
    //FIXME: Implement str -> int convert
    throw NotImplementedYet("Mail author!");
}
