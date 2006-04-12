#ifndef PLUGIN_RANDOMMODULE_H
#define PLUGIN_RANDOMMODULE_H

#include "../include/Logging.h"
#include "../include/Exceptions.h"
#include "../include/cModule.h"
#include "../include/iStreamModule.h"
#include "../include/iIntegerModule.h"
#include "../include/cConnection.h"
#include "../include/cIntegerConnection.h"
#include "../include/cStreamConnection.h"






namespace PPLTPlugin{

    class RandomModule: public PPLTCore::cModule,
        public PPLTCore::iStreamModule, public PPLTCore::iIntegerModule
    {
        public:
            RandomModule();

            PPLTCore::cConnection *connect(std::string, PPLTCore::cDisposable *child = 0);

            void disconnect(std::string);

            void enable_events();
            void disable_events();

            int read(std::string, char *, int);
            int write(std::string, char *, int);

            int get(std::string);
            void set(std::string, int);
    };

}

#endif
