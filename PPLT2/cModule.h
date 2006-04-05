#ifndef PPLT_CMODULE_H
#define PPLT_CMODULE_H

#include <string>
#include <list>
#include <map>

#include "cConnection.h"
#include "cDisposable.h"
#include "cObject.h"

namespace PPLTCore{

    /*
     * simple database used by the CModule classes to handle
     * all connections to children.
     */
    class cConnectionDataBase{
        private:
            std::map<std::string, std::string>   d_id_address_map;
            std::map<std::string, class cConnection *>  d_id_connection_map;

        public:
            cConnectionDataBase();
            ~cConnectionDataBase();

            void    addConnection(std::string, cConnection *);
            void    remConnection(std::string);

            int     count();

            cConnection  *getConnectionByID(std::string);
            std::string getAddressByID(std::string);
            std::list<cConnection *>    *getConnectionsByAddress(std::string);

            bool    hasAddress(std::string);
            bool    hasID(std::string);
    };



    /*
     * Base class for ALL modules:
     */
    class cModule: public cObject{
        protected:
            cConnectionDataBase          d_connections;

        public:
            cModule();
            virtual ~cModule();

            virtual void disable_events() = 0;
            virtual void enable_events()  = 0;

            virtual class cConnection *connect(std::string addr, cDisposable *child=0) = 0;
            virtual void disconnect(std::string)   = 0;

    };




}
#endif
