#include <iostream>
#include <typeinfo>

#include "../include/Logging.h"
#include "plugins/LoopbackModule.h"
#include "plugins/HexDumpModule.h"
#include "../include/cConnection.h"
#include "../include/cStreamConnection.h"
#include "../include/cModule.h"

using namespace PPLTCore;
using namespace PPLTPlugin;


int main(void){
    initLogging();
    cModule             *loop = new LoopbackModule();
    cModule             *hex = new HexDumpModule(loop, "a");
    cStreamConnection   *con = dynamic_cast<cStreamConnection *>(loop->connect("a"));

    std::cout << "Type of connection: " << typeid(hex).name() << std::endl;

    con->write("test",4);



return 0;
}
