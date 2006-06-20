/***************************************************************************
 *            cPyModule.h
 *
 *  2006-06-16
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

/**\file cPyModule.h
 * This file contains the definition for the wrapper class of python 
 * modules. */

#ifndef PPLTCORE_CPYMODULE_H
#define PPLTCORE_CPYMODUEL_H

#include "cModule.h"
#include "iIntegerModule.h"
#include "iFloatModule.h"
#include "iStreamModule.h"
#include "iSequenceModule.h"


namespace PPLTCore{
    
    /** This is a wrapper class for python modules.
     * This class provides interfaces for all types of data. This is necessary
     * to have only one wrapper class for all python modules. But this can 
     * lead into execptions while accessing a python module that doesn't porvide 
     * such an interface. */
    class cPyModule: public cModule, public iIntegerModule, 
                     public iFloatModule, public iStreamModule, 
                     public iSequenceModule {
        private:
        protected:
        public:
           int          get_integer(std::string con_id);
           double       get_float(std::string con_id);
           void         set_integer(std::string con_id, int value);
           void         set_float(std::string con_id, double value);
           int          read(std::string con_id, char *buff, int max_len);
           int          write(std::string con_id, char *buff, int len);
           std::string  recv(std::string con_id);
           void         send(std::string con_id, std::string data);
    };
    
}

#endif
  
