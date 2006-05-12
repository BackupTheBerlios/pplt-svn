/***************************************************************************
 *            iStreamModule.h
 *
 *  Sun Apr 23 01:18:24 2006
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
 
#ifndef PPLT_ISTREAMMODULE_H
#define PPLT_ISTREAMMODULE_H

#include "cModule.h"

/**\file iStreamModule.h
 * \brief This file contains the iStreamModule interface definition.
 *
 * The iStreamModule interface have to be implemented by any module
 * that wants to provide a data stream. */
namespace PPLTCore{

    class iStreamModule{
        public:
            virtual ~iStreamModule(){};

            virtual int read(std::string, char *, int) = 0;
            virtual int write(std::string, char *, int) = 0;
    };
}

#endif
