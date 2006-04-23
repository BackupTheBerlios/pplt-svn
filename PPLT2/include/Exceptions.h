/***************************************************************************
 *            Exceptions.h
 *
 *  Sun Apr 23 01:13:30 2006
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
 

#ifndef PPLT_EXCEPTIONS_H
#define PPLT_EXCEPTIONS_H

#include <string>

/** \file Exceptions.h
 * \brief In this file all exception-classes are listed.
 *
 * \b PLEASE use allways one of the classes listed to throw an
 * exception. If you want to define you own exceptions, please derive
 * it at least from the class \c Error. Because the methods of all
 * PPLT classes will allways catch this exceptions. All other
 * exceptions are not handled and will genegrate an abort of the
 * program.
 */

namespace PPLTCore{
    /** \brief Error is the base class for all PPLT exceptions.
     *
     * Pleas derive your exceptions at least from this class to
     * prevent program aborts.
     */
    class Error{
    protected:
        std::string     d_message;

    public:
        /** Constructor.
         * The constructor takes a string parameter that contains the
         * message for the exception. All derived exceptions will also
         * need this message.
         * The parameter \c msg takes the message for the exceptions.
         * May be the reason for the exception. */
        Error(std::string);

        ~Error();

        /** Get/set the message of the exception.
         * Calling this method without a string param will return the
         * current message of the exception. If this method is called
         * with a parameter, the messeg will be reset to the one given
         * by the parameter.
         * @param msg The new message of the exception. */
        std::string Message();
        void Message(std::string);
    };



    /** Basic exception class for internal errors.
     * This exceptions ore one derived from this should be used to
     * indicated an internal error. I.e. a bad useage like
     * FileNotFound or something like that.
     */
    class CoreError: public Error{
        public:
            /** Constructor
             * This constructor takes a string \c message, that
             * defined the message of the exception. This can be the
             * reason for the exception. */
            CoreError(std::string msg);
    };


    /** Base class for all errors in modules.
     * This exception or one derived from this should be used be
     * modules to indicate an error.*/
     class ModuleError: public Error{
         public:
            /** Constructor:
             * @see Error */
            ModuleError(std::string);
     };


    /** Class to indicate incomplete development.
     * This exception will mainly be used by the developer(s) to
     * indicate that a feature is not coimplete. */
    class NotImplementedYet: public CoreError{
        public:
            /** Constructor:
             * @see Error */
            NotImplementedYet(std::string);
    };


    /** Class to indicate an setup-error for modules.
     * This exception can be used by module-developers to
     * indicate an bas setup of a module. I.e. a missing parameter.*/
    class ModuleSetupError: public ModuleError{
    public:
        /** Constructor:
         * @see Error */
        ModuleSetupError(std::string);
        ~ModuleSetupError();
    };

}
#endif
