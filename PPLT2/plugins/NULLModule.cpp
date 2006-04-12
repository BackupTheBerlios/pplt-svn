#include <iostream>
#include "NULLModule.h"

using namespace PPLTCore;

using namespace PPLTPlugin;

NULLModule::NULLModule(): cModule(){
    std::cout << "Setup NULLModule\n";
}

cConnection *NULLModule::connect(std::string addr, cDisposable *child){
    cStreamConnection   *con = 0;
    if(0 == child){
        con = new cStreamConnection(this);
    }else{
        con = new cStreamConnection(this, child);
    }
d_connections.addConnection(addr, con);
return con;
}
cConnection *NULLModule::connect(std::string addr){ return connect(addr, 0); }


void NULLModule::disconnect(std::string id){
    d_connections.remConnection(id);
}

int NULLModule::read(std::string addr, char *buffer, int len){
    for(int n=0;n<len;n++)
        buffer[n] = (char)0;
return len;
}

int NULLModule::write(std::string addr, char *buffer, int len){ return len; }

void NULLModule::enable_events(){ }
void NULLModule::disable_events(){ }


