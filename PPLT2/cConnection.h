#ifndef PPLT_CCONNECTION_H
#define PPLT_CCONNECTION_H

#include "cModule.h"
#include "cObject.h"
#include "cDisposable.h"


namespace PPLTCore{
    /** The basic connection class.
     * The cConnection class is the base class for
     * all connections between modules and modules or
     * the external world. From this class the classes
     * @see cStreamConnection, @see cSequenceConnection and
     * @see cValueConnection are derived.
     *
     * Note: if this class will be destroyed, the destructor
     * will call the disconnect() method of the parent module.
     * So the connection will be closed clean. You don't need
     * to care about the closing of the connection. But you
     * need to care about the destruction of the instances of
     * this class unless the instance is used to connect two
     * modules. In this case the child module will destruct
     * the connection if it is destruct.
     *
     * Note: All constructos all called by the connect() method
     * of the module you or an other module want to be
     * connected to. Normaly you need not to create a
     * cConnection object by your self.
     */
    class cConnection: public cObject{
        private:
            cDisposable *d_owner_module;

        protected:
            /** Link to the parent module:
            * This attribute will be used by the derived classes to
            * access the parent module.
            */
            class cModule   *d_parent_module;

            /** Notyfy child about new data in buffer,
            * This method can be called from derived classes to
            * notify the child module (or symbol) about new data
            * in the  buffer.
            */
            virtual void    notify_child();

        public:
            /** Constructor:
            * The constructor take two arbuments, the first is a
            * pointer to the parent module, the second (optional)
            * parameter contains the pointer to the child module.
            * This pointer doesn't need to point to an complete
            * module, but the object have to implement at least the
            * @see cDisposable interface.
            * @param *parent Pointer to the parent.
            * @param *child Optional pointer to child.
            */
            cConnection(cModule *parent, cDisposable *owner=0);
            virtual ~cConnection();
    };

}

#endif
