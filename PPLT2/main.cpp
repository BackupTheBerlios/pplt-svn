#include <iostream>


#include "Logging.h"
#include "plugins/RandomModule.h"
#include "plugins/HexDumpModule.h"

using namespace PPLTCore;




int main(void){
    initLogging();

    cModule     *mod1 = new PPLTPlugin::RandomModule();
    cModule     *mod2 = new PPLTPlugin::HexDumpModule(mod1, "");
    cConnection *con  = mod2->connect("");

    char        buff[32];
    for(int n=0; n<32; n++)
        buff[n] = 0;

    dynamic_cast<cStreamConnection *>(con)->read(buff, 23);
    for(int n=0; n<32; n++)
        std::cout << (int)buff[n] << " ";
    std::cout << std::endl;


return 0;
}
