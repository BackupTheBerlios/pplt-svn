/***************************************************************************
 *            cObject.cpp
 *
 *  Sun Apr 23 01:26:44 2006
 *  Copyright  2006  Hannes Matuschek
 *  hmatuschek@gmx.net
 ****************************************************************************/

#include "cObject.h"

using namespace PPLTCore;

// define static member initial value...
std::list<std::string> cObject::d_identifier_list = std::list<std::string>();

cObject::cObject(){ d_identifier = NewIdentifier(); }

/* Destructor: will call each registered "destruction"-notifier */
cObject::~cObject(){ 
    std::list<iNotifyDestruction *>::iterator      it;

    //FIXME does it free all IDs if only one object will be destroyed?
    cObject::d_identifier_list.clear();     
    for(it = d_destruction_notifiers.begin(); it != d_destruction_notifiers.end(); ++it)
        (*it)->notify_destruction(Identifier());
}


/* This accessor is used to get the UNIQUE id of the object. */
std::string cObject::Identifier(){ return d_identifier; }


/* This private method generates new identifiers for
   the private cObject::d_identifier attribute. */
std::string cObject::NewIdentifier(){
    std::string     id = random_string(32);
    while(IdExists(id)){
        id = random_string(32);
    }
    d_identifier_list.push_back(id);
    return id;
}


/* Internal used method to generate random (hex) strings. */
std::string cObject::random_string(int length){
    std::string     id;
    char           alph[16] = {'0','1','2','3','4','5','6','7','8','9',
                               'a','b','c','d','e','f'};
    for(register int n = 0; n < length*2; n++)
        id += alph[std::rand()%16];
    return id;
}


/* Internal (private) method to check if a id is allready used. */
bool cObject::IdExists(std::string id){
    for( std::list<std::string>::iterator it = cObject::d_identifier_list.begin();
         cObject::d_identifier_list.end() != it;
         ++it)
        if((*it) == id)
            return true;
    return false;
}

void cObject::addDestructionNotifier(iNotifyDestruction *notifier){
    d_destruction_notifiers.push_back(notifier);
}
