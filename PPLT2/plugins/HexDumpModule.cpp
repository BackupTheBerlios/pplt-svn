#include "HexDumpModule.h"
#include <iostream>
#include <streambuf>
#include <iomanip>


using namespace PPLTCore;
using namespace PPLTPlugin;


HexDumpModule::HexDumpModule(cModule *parent, std::string addr)
: cInnerModule(parent, addr){ }


void HexDumpModule::disable_events() {}
void HexDumpModule::enable_events() {}
void HexDumpModule::data_notify() {}

cConnection *HexDumpModule::connect(std::string addr, cDisposable *child){
    cStreamConnection *con;

    if(1 < d_connections.count())
        throw ModuleError("HexDump can only handle one connection!");

    con = new cStreamConnection(this, child);
    d_connections.addConnection(addr, con);
    return con;
}

void HexDumpModule::disconnect(std::string con_id){
    d_connections.remConnection(con_id);
}

int HexDumpModule::read(std::string con_id, char *buff, int len){
    int             ret_len;
    int             line_num;
    std::string     line;

    ret_len = dynamic_cast<cStreamConnection *>(d_parent_connection)->read(buff, len);
    line_num = ret_len/8;
    for(register int ln=0;ln<line_num; ln++){
        line = hexLine(buff, ln*8);
        MODLOG_DEBUG("read() (+"<<ln*8<<"b):\t"<<line);
    }

    if(0 < ret_len - (line_num*8) ){
        line = hexLine(buff, line_num*8, ret_len-(line_num*8));
        MODLOG_DEBUG("read() (+"<<line_num*8<<"b):\t"<<line);
    }

    return ret_len;
}

int HexDumpModule::write(std::string con_id, char *buff, int len){
    int         ret_len;
    int         line_num;
    std::string line;
    ret_len = dynamic_cast<cStreamConnection *>(d_parent_connection)->write(buff, len);

    line_num = ret_len/8;
    for(register int ln=0;ln<line_num; ln++){
        line = hexLine(buff, ln*8);
        MODLOG_DEBUG("read() (+"<<ln*8<<"b):\t"<<line);
    }

    if(0 < ret_len - (line_num*8) ){
        line = hexLine(buff, line_num*8, ret_len-(line_num*8));
        MODLOG_DEBUG("read() (+"<<line_num*8<<"b):\t"<<line);
    }

    return ret_len;
}

std::string HexDumpModule::hexLine(char *buffer, int offset, int len){
    std::ostringstream  output("",std::ios::ate);
    unsigned int      val;

    output.setf(std::ios::right, std::ios::adjustfield);

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
