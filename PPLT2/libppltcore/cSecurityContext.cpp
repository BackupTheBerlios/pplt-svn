/***************************************************************************
 *            cSecurityContext.cpp
 *
 *  2006-06-23
 *  Copyright  2006  Hannes Matuschek
 *  hmatuschek@gmx.net
 ****************************************************************************/

#include "cSecurityContext.h"

using namespace PPLTCore;


cSecurityContext::cSecurityContext(){ }



cSecurityContext::~cSecurityContext(){ }



std::list<iSecurityContextItem> cSecurityContext::getItems(std::type_info kind){
    std::list<iSecurityContextItem> list;

    for(std::list<iSecurityContextItem>::iterator it = d_sec_items.begin();
        it != d_sec_items.end(); ++it){
            if(typeid(*it) == kind)
                list.push_back(*it);
    }     

    return list;
}



void cSecurityContext::addItems(iSecurityContextItem item){
    d_sec_items.push_back(item);
}



void cSecurityContext::addItems(std::list<iSecurityContextItem> items){
    for(std::list<iSecurityContextItem>::iterator it = d_sec_items.begin();
        it != d_sec_items.end(); ++it){
            d_sec_items.push_back(*it);
    }            
}


void cSecurityContext::remItems(iSecurityContextItem item){
    //FIXME should raise an exception if item doesn't exists in list
    d_sec_items.remove(item);
}



void cSecurityContext::remItems(std::list<iSecurityContextItem> items){
    for(std::list<iSecurityContextItem>::iterator it = items.begin();
        it != items.end(); ++it){
            d_sec_items.remove(*it);
    }            
}



void cSecurityContext::remItems(std::type_info kind){
    std::list<iSecurityContextItem> new_list;
    iSecurityContextItem            item;

    while(d_sec_items.size()){
        item = d_sec_items.front();
        d_sec_items.pop_front();
    
        if(typeid(item) != kind)
            new_list.push_back(item);
    }        
    
    d_sec_items = new_list;
}

