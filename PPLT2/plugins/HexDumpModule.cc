/***************************************************************************
 *            HexDumpModule.cc
 *
 *  Sun Apr 23 01:25:47 2006
 *  Copyright  2006  Hannes Matuschek
 *  hmatuschek@gmx.net
 ****************************************************************************/

#include "HexDumpModule.h"


using namespace PPLTCore;
using namespace PPLTPlugin;



cModule *HexDumpModuleFactory(cModule *parent, std::string addr, tModuleParameters params){
    return new HexDumpModule(parent, addr, params);
}



HexDumpModule::HexDumpModule(cModule *parent, std::string addr, 
                             tModuleParameters params)
: cInnerModule(parent, addr, params) { }



void HexDumpModule::notify_children(std::list<std::string> hexlines, std::string func){
    cSequenceConnection         *con;
    std::list<cConnection *>    connections;

    // get all connection with "dump" addr and push the new data:
    connections = d_connections.getConnectionsByAddress("dump");
    for(std::list<cConnection *>::iterator it = connections.begin();
        it != connections.end(); ++it){
            for(std::list<std::string>::iterator line_it = hexlines.begin();
                line_it != hexlines.end(); ++line_it){
                    // FIXME max be a little bit ugly
                    try{
                        if(0 == (con = dynamic_cast<cSequenceConnection *>(*it)) )
                            continue;
                        con->push(func + " " + *line_it); }           
                    catch(...){ }
            }                
    }        
}



void HexDumpModule::data_notify() {
    std::string                 buffer;
    cStreamConnection           *con;
    int                         line_num;
    int                         ret_len=0;
    std::list<std::string>      hexlines;

    // cast connection:
    if(0 == (con = dynamic_cast<cStreamConnection *>(d_parent_connection)) )
        throw ModuleError("Unable to cast parent connection to stream!");
   
    //try to get data from parent:
    do{
        std::string  tmp;
        tmp = con->read(1024);
        ret_len = tmp.length();
        buffer += tmp;
    }while(ret_len == 1024);    
    
    MODLOG_DEBUG("data_notify(): got " << buffer.length() <<" bytes.");
    
    line_num = buffer.length()/8; 
    for(register int ln=0; ln<line_num+1; ln++){
        MODLOG_DEBUG("data_notify() (+" << ln*8<<"b):\t" << hexLine(buffer, ln*8));
        hexlines.push_back(hexLine(buffer, ln*8));
    }
    
    notify_children(hexlines, "push:");

    // check if a child is defined:
    if(d_connections.count("") != 1)
        throw ModuleError("No child defined: Number of children connected with \"\": %i", d_connections.count(""));

    // try to inform the child:
    try{
        std::list<cConnection *>    connections;
        cStreamConnection           *con;
        if(0 == (con = dynamic_cast<cStreamConnection *>(d_connections.getConnectionsByAddress("").front())) )
            throw ModuleError("Unable to cast connection to stream connection!");
        con->push(buffer, buffer.length());
    }catch(...){ 
        throw;
    }
}



cConnection *HexDumpModule::connect(std::string addr, cDisposable *child){
    cConnection *con;

    if(addr == ""){
        if(0 != d_connections.count(""))
            throw ModuleError("This module can handle only one child-connection at addr \"\".");
        MODLOG_DEBUG("Create cStreamConnection for HexDump");
        con = new cStreamConnection(this, child);
        d_connections.addConnection(addr, con);
        return con;
    }
    
    if(addr == "dump"){
        MODLOG_DEBUG("Create dump connection.");
        con = new cSequenceConnection(this, child);
        d_connections.addConnection(addr, con);
        return con;
    }

    throw ModuleError("Can't connect to HexDump with addr \"%s\": Address unknown.",addr.c_str());
    return 0;
}



bool HexDumpModule::isBusy(void){
    if(d_connections.count())
        return true;
    return false;
}    



void HexDumpModule::disconnect(std::string con_id){
    cConnection *con;

    if(d_connections.hasID(con_id)){
        con = d_connections.getConnectionByID(con_id);
        d_connections.remConnection(con_id);
    }
}



std::string HexDumpModule::read(std::string con_id, unsigned int len){
    std::string                 data;
    int                         line_num;
    cConnection                 *con;
    std::list<std::string>      hexlines;

    if(0 == d_connections.count(""))
        throw ItemNotFound("Mad connection id (%s): There is not connection with addr \"\"", con_id.c_str());

    if(!d_connections.hasID(con_id))
        throw ItemNotFound("There is no connection with id \"%s\" to this module!", con_id.c_str());
    
    if("" != d_connections.getAddressByID(con_id))
        throw ModuleError("Only connection with addr \"\" can call read()");     //FIXME should throw AccessDenied instead

    data = dynamic_cast<cStreamConnection *>(d_parent_connection)->read(len);
    
    line_num = data.length()/8;
    for(register int ln=0;ln<line_num+1; ln++){
        std::string line = hexLine(data, ln*8);
        MODLOG_DEBUG("read() (+"<<ln*8<<"b):\t"<<line);
        hexlines.push_back(line);
    }

    notify_children(hexlines,"read:");

    return data;
}



unsigned int HexDumpModule::write(std::string con_id, std::string data, unsigned int len){
    int                     line_num;
    std::list<std::string>  hexlines;

    try{
        len = dynamic_cast<cStreamConnection *>(d_parent_connection)->write(data, len);
    }catch( ... ){
        line_num = len/8;
        for(register int ln=0;ln<line_num+1; ln++){
            std::string line = hexLine(data, ln*8);
            MODLOG_DEBUG("read() (+"<<ln*8<<"b):\t"<<line);
            hexlines.push_back(line);
        }
        notify_children(hexlines, "write:");
        throw;
    }        
    return len;
}



std::string HexDumpModule::recv(std::string con_id){
    throw ModuleError("This method should never be called!");
}



void HexDumpModule::send(std::string con_id, std::string data){
    throw ModuleError("This method should never be called!");
}



std::string HexDumpModule::hexLine(std::string buffer, int offset){
    std::ostringstream  output("",std::ios::ate);
    unsigned int        val;
    int                 len=8;
    std::string         hex_line;
    
    if(0 >= buffer.length()-offset)
        return hex_line;

    output.setf(std::ios::right, std::ios::adjustfield);

    if(len > buffer.length()-offset)
        len = buffer.length()-offset;

    for(register int n=0;n<len;n++){
        val = buffer[offset+n];
        output.setf(std::ios::hex,std::ios::basefield);
        output << std::setw(2) << (int)(val&0xff) << " ";
        output.unsetf(std::ios::hex);
    }

    if(len < 8){
        for(register int n=0; n<8-len;n++)
        output << "   ";
    }
    output << "\t";

    for(register int n=0; n<len; n++){
        val = buffer[offset+n];
        if((val&0xff) < 32 || (val&0xff) > 126)
            output << ".";
        else
            output << (unsigned char)val;
    }

    if(len < 8){
        for(register int n=0; n<8-len;n++)
        output << " ";
    }

    return output.str();
}
