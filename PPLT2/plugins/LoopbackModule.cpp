#include <ios>
#include "LoopbackModule.h"
#include "../Exceptions.h"

using namespace PPLTPlugin;
using namespace PPLTCore;

LoopbackModule::LoopbackModule(std::string id)
: CRootModule(id){
    d_events_enabled = true;
}


int LoopbackModule::connect(std::string address, CInnerModule *module){
    CRootModule::connect(address, module);
    return 0;
}

int LoopbackModule::disconnect(std::string id){
    CRootModule::disconnect(id);
    return 0;
}


int LoopbackModule::read(std::string addr, char *buff, int len){
    d_buffer.read(buff, len);

return 0;
}

int LoopbackModule::write(std::string addr, char *buff, int len){
    std::list<CModule *> *c_list = d_children.getChildrenByAddress(addr);
    d_buffer.write(buff, len);
    for(std::list<CModule *>::iterator it = c_list->begin(); it != c_list->end(); ++it){
        reinterpret_cast<CInnerModule *>(*it)->data_present_callback();
    }
return 0;
}


int LoopbackModule::disable_events(){
    if(true == d_events_enabled)
        d_events_enabled = false;
    return 0;
}

int LoopbackModule::enable_events(){
    if(false == d_events_enabled)
        d_events_enabled = true;
    return 0;
}


/* ************************************************************************
 * Methods of LoopbackBuffer class
 * ************************************************************************ */
int LoopbackBuffer::write(char *buff, int len){
    d_buffer.append(reinterpret_cast<char const *>(buff), len);
    return len;
}

int LoopbackBuffer::read(char *buff, int len){
    std::string     tmp;

    if((unsigned int)len > d_buffer.size())
        len = d_buffer.size();
    tmp = d_buffer.substr(0, len);
    d_buffer.erase(0,len);
    for(int n=0; n<len; n++)
        buff[n] = tmp.data()[n];
    return len;
}
