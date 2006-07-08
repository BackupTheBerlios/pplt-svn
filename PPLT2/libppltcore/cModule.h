/***************************************************************************
 *            cModule.h
 *
 *  Sun Apr 23 01:16:52 2006
 *  Copyright  2006  Hannes Matuschek
 *  hmatuschek@gmx.net
 ****************************************************************************/

/*
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 */
 
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

    /** */
    typedef std::map<std::string, std::string>  tModuleParameters;
    
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
            std::list<cConnection *> getConnectionsByAddress(std::string addr);

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
     * to make sure that no other module or symbol can access this module at the
     * same time. It also makes it possible to reserve your parent module for an
     * exclusive access. Normaly each connection to a module will automaticly
     * lock the module. But with a autolock(false) call you can disable the 
     * autolock mechanism. But in this case you have to care about the locking
     * and unlocking. Example:
     * \code
       cConnection connection = module->connect("address");
       connection->reserve();
       try{
            //do IO with connection
            connection->release()
       }catch(...){
            connection->release();
            throw;
       } 
       \endcode
     * \todo Write some examples how to inform a child. */
    class cModule: public cObject{
        private:
            pthread_mutex_t     d_reservation_lock;

        protected:
            /** The connection data base */
            cConnectionDataBase          d_connections;
            tModuleParameters            d_parameters;
        
        public:
            /** Constructor.
            * This is the constructor. It doesn't take any parameters
            * because this class isn't really complex. */
            cModule(tModuleParameters);
            
            /** Destructor. */
            virtual ~cModule();

            /** Reserves (locks) the module.
            * Calling this method the module will be locked. This means that
            * no other thread can access this module at the same time. The 
            * locking will not be done automaticly because by this way it is
            * possible to reserve the module over more then one access. */
            void reserve();
            
            /** Frees (releases) the module. 
            * This method will release the module lock. */
            void release();
            
            /** Creates a new connection to the module.
            * This pure virtual method have to be implemented by a module.
            * This method should return a pointer to a new allocated cConnection
            * object or better to one that was derived from this. (like 
            * cStreamConnection). Please use the available tools to manage the
            * connections. */
            virtual class cConnection *connect(std::string addr="", 
                                               cDisposable *child=0) = 0;
            
            /** Closes a connection.
            * This method should close the connection. The parameter is the 
            * connection id. This method will be calleb by the destructor of
            * the cConnection object or the one derived from this. */
            virtual void disconnect(std::string con_id)   = 0;

            /** Returns false if module is used by an other module or symbol. */
            virtual bool isBusy(void);
   };

}

#endif
