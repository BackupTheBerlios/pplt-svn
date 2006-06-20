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
: cInnerModule(parent, addr, params) { d_my_child = 0; }



void HexDumpModule::data_notify() {
    std::string         buffer;
    cStreamConnection   *con;
    int                 line_num;
    int                 ret_len=0;

    MODLOG_DEBUG("In HexDump::data_notify()");

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
    
    line_num = buffer.length()/8; 
    for(register int ln=0; ln<line_num+1; ln++){
        MODLOG_DEBUG("data_notify() (+" << ln*8<<"b):\t" << hexLine(buffer, ln*8));
    }
    
    // check if a child is defined:
    if(0 == d_my_child)
        throw ModuleError("No child defined");

    // try to inform the child:
    try{
        d_my_child->push(buffer, buffer.length());
    }catch(...){ 
        throw;
    }
}


cConnection *HexDumpModule::connect(std::string addr, cDisposable *child){
    if(0 != d_my_child)
        throw ModuleError("This module can handle only one child-connection.");
    MODLOG_DEBUG("Create cStreamConnection for HexDump");
    d_my_child = new cStreamConnection(this, child);
    return d_my_child;
}



bool HexDumpModule::isBusy(void){
    if(0 != d_my_child)
        return true;
    return false;
}    



void HexDumpModule::disconnect(std::string con_id){
    if(0 == d_my_child)
        throw ItemNotFound("Connection %s is not to me!", con_id.c_str());
    if(con_id != d_my_child->Identifier())    
        throw ItemNotFound("Connection %s is not to me!", con_id.c_str());
    d_my_child = 0;
}



std::string HexDumpModule::read(std::string con_id, int len){
    std::string     data;
    int             line_num;

    if(0 == d_my_child)
        throw ItemNotFound("Connection %s is not to me!", con_id.c_str());
    if(con_id != d_my_child->Identifier())    
        throw ItemNotFound("Connection %s is not to me!", con_id.c_str());
    
    data = dynamic_cast<cStreamConnection *>(d_parent_connection)->read(len);
    
    line_num = data.length()/8;
    for(register int ln=0;ln<line_num+1; ln++){
        std::string line = hexLine(data, ln*8);
        MODLOG_DEBUG("read() (+"<<ln*8<<"b):\t"<<line);
    }

    return data;
}

int HexDumpModule::write(std::string con_id, std::string data, int len){
    int         line_num;
    len = dynamic_cast<cStreamConnection *>(d_parent_connection)->write(data, len);

    line_num = len/8;
    for(register int ln=0;ln<line_num+1; ln++){
        std::string line = hexLine(data, ln*8);
        MODLOG_DEBUG("read() (+"<<ln*8<<"b):\t"<<line);
    }

    return len;
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
