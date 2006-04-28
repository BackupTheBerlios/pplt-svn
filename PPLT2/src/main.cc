#include "../include/Exceptions.h"
#include "../include/LoopbackModule.h"
#include "../include/HexDumpModule.h"
#include "../include/cStreamConnection.h"
#include "../include/cModule.h"
#include "../include/iSequenceModule.h"
#include "../include/cSequenceConnection.h"
using namespace PPLTCore;
using namespace PPLTPlugin;

class StaticHDLC: public cInnerModule, public iSequenceModule{
    private:
        int d_my_address;
    
    public:
        StaticHDLC(cModule *parent, std::string addr, tModuleParameters params)
        : cInnerModule(parent, addr, params){
            // check if parameter "address" is present:
            if(!params.count("address"))
                throw ModuleSetupError("Module StaticHDLC needs a pramaeter addr!");
            // check if parentconnection is a stream!
            if(0 == dynamic_cast<cStreamConnection *>(d_parent_connection))
                throw ModuleSetupError("Module StaticHDCL needs a streaming parent!");
            // save addr as number!
            d_my_address = atoi(params["address"].c_str());
        }
        
        
        cConnection *connect(std::string addr, cDisposable *child){
            return new cSequenceConnection(this, child);
        }
        
        void disconnect(std::string id){ }        
        
        
        std::string recv(std::string id){ return ""; }
        void send(std::string id, std::string data){ }
        
        void data_notify(){ }
};    

int main(void){
    PPLTCore::initLogging();
    
    char                buff[32];
    
    cModule             *loop = new LoopbackModule(tModuleParameters());
    cModule             *hex  = new HexDumpModule(loop, "a", tModuleParameters());
    cStreamConnection   *con1 = dynamic_cast<cStreamConnection *>(loop->connect("a"));
    cModule             *hdlc = new StaticHDLC(hex, "", tModuleParameters());
    
    // stop emmiting events
    con1->events_enabled(false);
    
    
return(0);    
}
