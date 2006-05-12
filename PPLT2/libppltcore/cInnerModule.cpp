/***************************************************************************
 *            cInnerModule.cpp
 *
 *  Sun Apr 23 01:26:27 2006
 *  Copyright  2006  Hannes Matuschek
 *  hmatuschek@gmx.net
 ****************************************************************************/

#include "cInnerModule.h"

using namespace PPLTCore;

cInnerModule::cInnerModule(cModule *parent, std::string addr, 
                            tModuleParameters params): cModule(params)
{
    d_parent_connection = parent->connect(addr, this);
}

cInnerModule::~cInnerModule(){
    if(0 == d_parent_connection)
        throw CoreError("Innermodule with no connection to parent!");
    delete d_parent_connection;
}