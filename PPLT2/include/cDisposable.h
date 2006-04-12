#ifndef PPLT_CDISPOSABLE_H
#define PPLT_CDISPOSABLE_H

/**
 * \file cDisposable.h
 * \brief This file contains the interface for all modules that are
 * disposable.
 */
namespace PPLTCore{
    /** Interface for all (inner) Modules and symbols.
     *
     * Modules that wants to be informed about new data have to
     * implement this interface. Meanly this can onyl be inner
     * modules.
     *
     * \b Note: If your module is derived from the
     * cInnerModule class, you don't need to derive you module
     * additional from this class to implement the interface,
     * because the cInnerModule class was allready derived from
     * cDisposable.
     *
     * This interface defines that a module, that wants to be
     * infromed from his parent about new data, have to implement
     * a method called \c data_notify(). This \c void method
     * takes no additional parameters. This method will be called
     * by the parent module if there is new data for your module.
     * You can get this data by calling read() or get() of you
     * d_parent_connection. (Depends on the kind of the connection
     * you've got from the parent.)
     *
     * Of cause: A module, that access the OS or hardware instead
     * of processing data gotten from a parent module will not need
     * to implement this interface. */
    class cDisposable{
        public:
            cDisposable();
            virtual ~cDisposable();

            /** Callback.
            *
            * This method will be called by the parent of a module
            * that implements the cDisposable interface. (Meaning
            * providing this method) In other words: only a module,
            * that implements this interface will be connectable to
            * an other module. Because the parent module must be able
            * to inform the child module about the presents of new
            * data. This will be done by pushing the new data into
            * a buffer at the connection between the two modules and
            * calling this method to inform the child. The child can
            * get the data by calling the get() or read() methods
            * of the d_parent_connection. */
            virtual void    data_notify() = 0;
    };

}

#endif
