#ifndef PPLT_CDISPOSABLE_H
#define PPLT_CDISPOSABLE_H

/**
 * \file cDisposable.h
 * \brief This file contains the interface for all modules that are disposable.
 */
namespace PPLTCore{
    /** Interface for all (inner) Modules and symbols. Also
     * connections implement this interface.
     * Modules that can be informed about new data. For this
     * these module have to implement the public method data_notify().
     * This method will be called by the underlaying cConnection object
     * to inform the module about new data.
     */
    class cDisposable{
        public:
            cDisposable();
            virtual ~cDisposable();

            virtual void    data_notify() = 0;
    };

}

#endif
