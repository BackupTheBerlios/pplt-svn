#ifndef PPLT_COBJECT_H
#define PPLT_COBJECT_H

#include <string>
#include <list>
#include <iostream>

namespace PPLTCore{

    /* The class \c cObject implements the basic needs for a unique object like
      modules, connections, symbols.

      \p All objects in the PPLT system needs to have a unique id. For
      example a \c cConnection object need to be identified by the \c cModule
      the cConnection belongs to. */
    class cObject{
        private:
            std::string     d_identifier;
            static std::list<std::string>   d_identifier_list;
            std::string     random_string(int);
            bool            IdExists(std::string);

        protected:
            std::string     NewIdentifier();

        public:
            cObject();
            ~cObject();

            std::string     Identifier();
    };

}
#endif
