#include <iostream>
#include <typeinfo>

#include "../include/Logging.h"
#include "../include/LoopbackModule.h"
#include "../include/HexDumpModule.h"
#include "../include/cConnection.h"
#include "../include/cStreamConnection.h"
#include "../include/cModule.h"
#include "../include/cSymbol.h"
using namespace PPLTCore;
using namespace PPLTPlugin;


void my_handler(cSymbol *symb){
    std::cout << "In callback! \n";
}

int main(void){
    initLogging();
    cModule             *loop = new LoopbackModule();
    cModule             *hex = new HexDumpModule(loop, "a");
    cStreamConnection   *con = dynamic_cast<cStreamConnection *>(loop->connect("a"));
    cSymbol             *sym = new cSymbol(loop, "a");

    sym->addHandler(my_handler);

    con->write("test",4);

    sym->data_notify();
return 0;
}
