#include <iostream>
#include <typeinfo>

#include "../include/Logging.h"
#include "../include/LoopbackModule.h"
#include "../include/HexDumpModule.h"
#include "../include/cConnection.h"
#include "../include/cStreamConnection.h"
#include "../include/cModule.h"
#include "../include/cStreamSymbol.h"

using namespace PPLTCore;
using namespace PPLTPlugin;


void my_handler(cSymbol *symb){
    char    buff[128];
    int     len;
    
    cStreamSymbol   *my_symb = dynamic_cast<cStreamSymbol *>(symb);
    
    if(0 == my_symb)
        throw Error("Unable to cast to a cStreamSymbol pointer!");
    
    len = my_symb->read(buff, 128);

    std::cout << "HDL: Got " << len << "bytes  ";
    for(int n=0;n<len;n++)
        std::cout << (char)buff[n];
    std::cout << "\n";
}

int main(void){
    initLogging();
    cModule             *loop = new LoopbackModule();
    cModule             *hex = new HexDumpModule(loop, "a");
    cStreamConnection   *con = dynamic_cast<cStreamConnection *>(hex->connect("a"));
    cStreamSymbol       *sym = new cStreamSymbol(loop, "a",true);

    sym->addHandler(my_handler);
    
    con->reserve();
    con->write("test",4);
    con->release();
    
    sym->data_notify();
    sleep(1);
return 0;
}
