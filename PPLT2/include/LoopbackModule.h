#ifndef PPLT_PLUGIN_LOOPBACK_H
#define PPLT_PLUGIN_LOOPBACK_H

#include "../include/cModule.h"
#include "../include/iStreamModule.h"
#include "../include/cConnection.h"
#include "../include/cStreamConnection.h"
#include "../include/cDisposable.h"
#include "../include/Logging.h"
#include "../include/Exceptions.h"


namespace PPLTPlugin{

    class LoopbackModule
    : public PPLTCore::cModule,
      public PPLTCore::iStreamModule
    {
        private:
            PPLTCore::cConnection *GetTheOtherOne(std::string addr);

        public:
            LoopbackModule();

            void enable_events();
            void disable_events();

            PPLTCore::cConnection *connect(std::string addr,
                                           PPLTCore::cDisposable *child=0);
            void disconnect(std::string);

            int read(std::string, char *, int);
            int write(std::string, char *, int);
    };
}


#endif
