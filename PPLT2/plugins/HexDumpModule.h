#ifndef PPLT_PLUGIN_HEXDUMP_H
#define PPLT_PLUGIN_HEXDUMP_H

#include "../Logging.h"
#include "../Exceptions.h"
#include "../cInnerModule.h"
#include "../iStreamModule.h"
#include "../cStreamConnection.h"

namespace PPLTPlugin{

    class HexDumpModule
    :public PPLTCore::cInnerModule,
     public PPLTCore::iStreamModule{
        private:
            std::string hexLine(char *buff, int offset, int len=8);

        public:
            HexDumpModule(PPLTCore::cModule *, std::string);

            void enable_events();
            void disable_events();

            PPLTCore::cConnection *connect(std::string addr,
                                           PPLTCore::cDisposable *child=0);
            void disconnect(std::string);

            int read(std::string, char *, int);
            int write(std::string, char *, int);

            void data_notify();
    };

}

#endif

