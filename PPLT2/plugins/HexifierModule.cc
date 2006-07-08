/***************************************************************************
 *            HexifierModule.cc
 *
 *  2006-06-21
 *  Copyright  2006  Hannes Matuschek
 *  hmatuschek@gmx.net
 ****************************************************************************/


#include "HexifierModule.h"

using namespace PPLTCore;
using namespace PPLTPlugin;



cModule *HexifierModuleFactory(cModule *parent, std::string addr, tModuleParameters params){
    return new HexifierModule(parent, addr, params);
}



HexifierModule::HexifierModule(cModule *parent, std::string addr, tModuleParameters params)
    : cInnerModule(parent, addr, params){
    if(0 == dynamic_cast<cStreamConnection *>(d_parent_connection) and
       0 == dynamic_cast<cSequenceConnection *>(d_parent_connection))
            throw ModuleError("This module needs a stream or sequence connection to the parent!");
}



HexifierModule::~HexifierModule(){ }



cConnection *HexifierModule::connect(std::string addr, cDisposable *child){
    cConnection   *con;
    
    if(addr != "")
        throw ModuleError("Unable to connect: Connections to this module needs no address!");

    if(d_connections.count() != 0)
        throw ModuleError("Only one child can be connected to this module at one time!");

    if(0 != dynamic_cast<cStreamConnection *>(d_parent_connection)){
        con = new cStreamConnection(this, child);
        d_connections.addConnection(addr, con);
    }else{
        con = new cSequenceConnection(this, child);
        d_connections.addConnection(addr, con);
    }

    return con;
}



void HexifierModule::disconnect(std::string con_id){
    if(!d_connections.hasID(con_id))
        throw ItemNotFound("No connection with id (%s) exists to this module!", con_id.c_str());
    d_connections.remConnection(con_id);
}


std::string HexifierModule::hexify(std::string data){
    std::ostringstream      buff;
    char                    val;

    buff.setf(std::ios::right, std::ios::adjustfield);
    for(register int n=0; n<data.length(); n++){
        val = data[n];
        buff.setf(std::ios::hex,std::ios::basefield);
        buff << std::setw(2) << (int)(val&0xff);
        buff.unsetf(std::ios::hex);
    }
    return buff.str();
}



std::string HexifierModule::unhexify(std::string data){
    std::string         buffer;
    unsigned char       c;

    if(data.length()%2)
        throw ModuleError("Unable to unhexify \"%s\" -> length must be a multible of 2!",data.c_str());

    for(register int i=0; i < data.length(); i+=2){ 
        sscanf(data.substr(i,2).c_str(), "%2x", &c);
        buffer+=c;
    }
    return buffer;
}



void HexifierModule::data_notify( void ){
    cStreamConnection   *st_con;
    cSequenceConnection *se_con;
    std::string         buffer;
    unsigned int        len;

    if(0 != (st_con = dynamic_cast<cStreamConnection *>(d_parent_connection)) ){
        len = st_con->buff_len();
        buffer = st_con->read(len);    
        
        if(0 == d_connections.count(""))
            throw ModuleError("No children connected to this module!");
        
        st_con = dynamic_cast<cStreamConnection *>(d_connections.getConnectionsByAddress("").front());
        st_con->push(hexify(buffer), len*2);
        return;
    }          

    if(0 != (se_con = dynamic_cast<cSequenceConnection *>(d_parent_connection)) ){
        buffer = se_con->recv();

        if(0 == d_connections.count(""))
            throw ModuleError("No children are connected to this module!");

        se_con = dynamic_cast<cSequenceConnection *>(d_connections.getConnectionsByAddress("").front());
        se_con->push(hexify(buffer));
        return;
    }
    
    throw ModuleError("Invalid connection type! This module need a sequence or a stream connection to parent!");
}


std::string HexifierModule::read(std::string con_id, unsigned int len){
    std::string         buffer;
    cStreamConnection   *con;

    if(0 == d_connections.count(""))
        throw ItemNotFound("No child connected with addr \"\" to this module!");

    if(!d_connections.hasID(con_id))
        throw ModuleError("Mad connection (%s): This one is not connected to this module!", con_id.c_str());

    if(0 == (con = dynamic_cast<cStreamConnection *>(d_parent_connection)) )
        throw ModuleError("Mad interface: The parent connection is not a stream!");

    if(len%2)
        throw ModuleError("The length must be a multible of 2!");

    buffer = hexify(con->read(len));
    return buffer;
}



std::string HexifierModule::recv(std::string con_id){
    std::string         buffer;
    cSequenceConnection *con;

    if(0 == d_connections.count(""))
        throw ItemNotFound("No child connected with addr \"\" to this module!");
    if(!d_connections.hasID(con_id))
        throw ModuleError("Mad connection (%s): This one is not connected to this module!", con_id.c_str());
    
    if(0 == (con = dynamic_cast<cSequenceConnection *>(d_parent_connection)))
        throw ModuleError("Mad interface: The parent module is not a sequence module!");

    buffer = hexify(con->recv());
    return buffer;
}



unsigned int HexifierModule::write(std::string con_id, std::string data, unsigned int len){
    cStreamConnection   *con;

    if(0 == d_connections.count(""))
        throw ItemNotFound("No child connected with addr \"\" to this module!");
    
    if(!d_connections.hasID(con_id))
        throw ModuleError("Mad connection (%s): This one is not connected to this module!", con_id.c_str());

    if(0 != len%2)
        throw ModuleError("Format error: The length of the given data is not a multible of 2!");

    if( 0 == (con = dynamic_cast<cStreamConnection *>(d_parent_connection)) )
        throw ModuleError("Interface error: The parent-connection is not a stream connection!");
            
    data = unhexify(data);
    return con->write(data, data.length())*2;
}



void HexifierModule::send(std::string con_id, std::string data){
    cSequenceConnection *con;

    if(0 == d_connections.count(""))
        throw ItemNotFound("No child connected with addr \"\" to this module!");
    
    if(!d_connections.hasID(con_id))
        throw ModuleError("Mad connection (%s): This one is not connected to this module!", con_id.c_str());

    if(0 != data.length()%2)
        throw ModuleError("Format error: The length of the given data is not a multible of 2!");

    if( 0 == (con = dynamic_cast<cSequenceConnection *>(d_parent_connection)) )
        throw ModuleError("Interface error: The parent-connection is not a sequence connection!");

    con->send(unhexify(data));        
}

