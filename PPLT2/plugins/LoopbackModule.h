#ifndef PPLT_PLUGIN_LOOPBACKMODULE_H
#define PPLT_PLUGIN_LOOPBACKMODULE_H

#include <iostream>
#include "../CModule.h"

namespace PPLTPlugin{

    class LoopbackBuffer{
        private:
            std::string     d_buffer;

        public:
            int write(char *, int);
            int read(char *, int);
    };

    class LoopbackModule: public PPLTCore::CRootModule{
        private:
            LoopbackBuffer  d_buffer;
            bool            d_events_enabled;

        public:
            LoopbackModule(std::string);

            int connect(std::string, PPLTCore::CInnerModule *);
            int disconnect(std::string);

            int read(std::string, char *, int);
            int write(std::string, char *, int);

            int enable_events();
            int disable_events();
    };

}

#endif
