#ifndef PPLT_COBJECT_H
#define PPLT_COBJECT_H

#include <string>
#include <list>
#include <iostream>

/**\file cObject.h
 * \brief This class hols the cObject class definition.*/
namespace PPLTCore{

    /** The class cObject implements the basic needs for a unique
     * object like modules, connections.
     *
     * All objects in the PPLT system needs to have a unique id. For
     * example a cConnection object need to be identified by the
     * cModule the cConnection belongs to. To get this all classes
     * that need to have a unique identifier are derived from the
     * cObject class. This class ensures that an instance of it will
     * have a private attribute d_identifier. You can get this ID
     * by calling the public Identifier() method.
     *
     * This method can be used by the connection() method of a
     * cModule class. Normaly a connection will be crated for a
     * address. To identify a connection later by the address may not
     * unique because more than one connection may created with the
     * same address. So the read()/write() or get()/set() methods
     * take a connection ID instead of a address to find out who
     * wants to read/write. */
    class cObject{
        private:
            std::string     d_identifier;
            static std::list<std::string>   d_identifier_list;
            std::string     random_string(int);
            bool            IdExists(std::string);
            std::string     NewIdentifier();

        public:
            /** Constructor.*/
            cObject();
            ~cObject();
            /** Returns the ID of the cObject instance.
             *
             * You can be sure that the returned id is unique for
             * all instances of the cObject and derived classes. */
            std::string     Identifier();
    };

}
#endif
