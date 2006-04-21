#ifndef PPLT_CMODULE_H
#define PPLT_CMODULE_H

#include <pthread.h>
#include <string>
#include <list>
#include <map>

#include "cConnection.h"
#include "Logging.h"
#include "cDisposable.h"
#include "cObject.h"


/**\file cModule.h
 * \brief This file contains the definition of the cModule class.
 *
 * The cModule class implements the basic needs to a module. It also
 * defines an interface that all module have to inplement. As an
 * "tool", it contains a instance of the cConnectionDataBase class,
 * that can manage connetions to a module for you.
 * @see cConnectionDataBase
 * @see cModule */
namespace PPLTCore{

    /** Simple database used by the CModule classes to handle
     * all connections to children.
     *
     * \b NOTE: You don't need to use this class in your module
     * implementations.
     *
     * Normaly a connection will be created by calling the method connect()
     * of the cModule class instance. This method returns a pointer to a
     * new allocated instace of a class derived from cConnection. The connect()
     * method takes a address parameter. To identify the connection later, the
     * address given at the connect() call is unusable because more than one
     * connection can be etablisht at the same time to the same address. So
     * a unique connection id is needed. Each instance of the cConnection class
     * will have such a unique ID. (This is be done by the parent class
     * cObject)  A module can get this id by calling the Identifier() method
     * of the cConnection instance. To handle all connections, there IDs and
     * addresses a cConnectionDataBase will be present as the d_connections
     * attribute in all instances of the cModule class. Simply add a new
     * connection with the addConnection() method to the database and you can
     * ask later for a address and for a pointer to the connection for a
     * specific connection ID. To remove a connection from database call
     * the remConnection() method. */
    class cConnectionDataBase{
        private:
            std::map<std::string, std::string>   d_id_address_map;
            std::map<std::string, class cConnection *>  d_id_connection_map;

        public:
            /** Constructor.
             *
             * Normaly you don't need to create you own cConnectionDataBase
             * instance if you want to use this in a Module. Because ther is
             * allready an instance at the protected d_connections attribute.*/
            cConnectionDataBase();
            ~cConnectionDataBase();

            /** Adds a new connection to the database. */
            void    addConnection(std::string addr, cConnection *con);
            /** Removes a connection from database. */
            void    remConnection(std::string con_id);

            /** Counts the connections in database */
            int     count();
            /** Counts the connections in database with a specific address. */
            int     count(std::string addr);

            /** Returns the connection with the given ID */
            cConnection  *getConnectionByID(std::string con_id);
            /** Returns the address of the connection with the given ID. */
            std::string getAddressByID(std::string addr);
            /** Returns all connections with the given address. */
            std::list<cConnection *> *getConnectionsByAddress(std::string addr);

            /** Returns true if there is a connection in DB with given
             * address. */
            bool    hasAddress(std::string addr);
            /** Returns true if there is a connection with the given ID. */
            bool    hasID(std::string con_id);
    };



    /** Base class for ALL modules.
     *
     * Any module needs to implement this class. There are some pure virtual
     * methods. These methods have to be present in the module to be compiled.
     * These methods implement some of the functionality of the module.
     *
     * This class also provides some methods to lock this module. Locking means
     * to make sure that no other module or symbo can access this module at the
     * same time. It also makes it possible to reserve your parent module for an
     * exclusive access. To do this, you have to put an 
     * d_parent_connection->reserve() call for each access to the parent module.
     * But you have to care, that the parent will be unlocked. Also there was 
     * thrown an exception while accessing the parent. 
     * Example:
     *
     * d_parent_connection->reserve();
     * try{
     *      //access your parent
     * }catch(...){
     *      d_parent_connection->release();
     * } 
     * \todo Write some examples how to inform a child. */
    class cModule: public cObject{
        private:
            pthread_mutex_t     d_reservation_lock;

        protected:
            /** The connection data base */
            cConnectionDataBase          d_connections;

        public:
            cModule();
            virtual ~cModule();

            void reserve();
            void release();

            virtual void disable_events() = 0;
            virtual void enable_events()  = 0;

            virtual class cConnection *connect(std::string addr, cDisposable *child=0) = 0;
            virtual void disconnect(std::string)   = 0;
   };

}

#endif
