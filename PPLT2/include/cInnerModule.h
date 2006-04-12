#ifndef PPLT_CINNERMODULE_H
#define PPLT_CINNERMODULE_H

#include "cModule.h"
#include "cDisposable.h"

/**\file cInnerModule.h
 * \brief This file contains the definition of the cInnerModule class.
 *
 * The cInnerModule class can be used to define a inner module. This
 * are modules, that doesn't access any hardware or the OS but
 * accessing other modules. By this a single layer of an
 * communication path will be implemented by a replaceable module,
 * This incraces the reusability of the modules for an other
 * context.*/
namespace PPLTCore{

    /** Baseclass for all inner modules.
     * A inner module differs from an Module, that it doesn't
     * interact with hardware or better with the OS. It interact
     * with other modules. This can be an Module or even an other
     * InnerModule. To do this it is needed to extend the cModule
     * call for a connection to the parent and to provied a
     * "callback" to be informed about new data at the paren for
     * this module.
     *
     * The connection to the parent is provieded by the
     * d_parent_conenction pointer to a cConenction object. This
     * object will be created by the parent module's connection()
     * method that is called by the constructor. The connection will
     * also be closed by the destructor. So you don't need to care
     * about the connection.
     *
     * This class also "implement" the cDisposable interface. That
     * means that your module have to have a method called
     * data_notify(), that will be called (indirectly) by the parent
     * module to inform your module that there is new data at the
     * parent.
     *
     * NOTE: If you want to write a real module you also have to
     * implement one (or more) of the following interfaces:
     * iStreamModule, iSequenceModule, iIntegerModule, iFloatModule,
     * ...
     */
    class cInnerModule: public cModule, public cDisposable{
        protected:
            cConnection     *d_parent_connection;

        public:
            /** Constructor
            * This constructor will create the conenction to the
            * parent module given by the attribute @param parent
            * with the address given by @param addr. Once done
            * you don't have to care about the handling of this
            * connection. All construction and destruction will be
            * done by the constructor and the destructior of this
            * class.
            */
            cInnerModule(cModule *parent, std::string addr);
            ~cInnerModule();
    };

}

#endif
