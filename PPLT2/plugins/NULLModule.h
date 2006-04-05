#ifndef PPLT_PLUGIN_NULLMODULE_H
#define PPLT_PLUGIN_NULLMODULE_H

#include <string>

#include "../iStreamModule.h"
#include "../cStreamConnection.h"
#include "../cConnection.h"
#include "../cDisposable.h"

namespace PPLTPlugin{

    class NULLModule : public PPLTCore::cModule, public PPLTCore::iStreamModule{
    public:
        NULLModule();

        PPLTCore::cConnection *connect(std::string);
        PPLTCore::cConnection *connect(std::string, PPLTCore::cDisposable *);
        void disconnect(std::string);

        int read(std::string, char *, int);
        int write(std::string, char *, int);

        void enable_events();
        void disable_events();
    };

}



#endif
