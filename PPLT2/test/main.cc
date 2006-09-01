#include "libPPLTCoreTest.h"
#include <wx/log.h>

using namespace PPLTTest;
using namespace PPLTCore::Test;


class myThread: public wxThreadHelper{
    public:
        myThread( void ): wxThreadHelper() { 
            Create(); 
            GetThread()->Run();
        }

        ~myThread( void ){ 
            std::cout << "Wait for thread to exit...";
            GetThread()->Wait(); 
        }

        void *Entry()
        { std::cout << "In Thread...\n"; sleep(2); return  NULL; }
};


int main(){
   
    myThread    t;
   
    std::cout << "Ok, thread should running...\n";
    std::cout << "Now we quit the program and the main() should wait for the thread to exit...\n";

return 0;
}

