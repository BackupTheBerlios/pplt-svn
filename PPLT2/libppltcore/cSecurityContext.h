/***************************************************************************
 *            cSecurityContext.h
 *
 *  2006-06-23
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

#ifndef PPLTCORE_SECURITY_CONTEXT
#define PPLTCORE_SECURITY_CONTEXT
#include <typeinfo>
#include "Exceptions.h"


namespace PPLTCore{

    class iExecutionContext{ };
    class iACLItem{ }; 
    
    class cSecurityContext{
        private:
            iUserDatabase                       *d_user_db;
            iExecutionContext                   d_exec_ctx;
            std::list<iACLItem>                 d_sec_acl;
            
        public:
            cSecurityContext();
            ~cSecurityContext();
    
            bool isAllowed(unsigned int action, iExecutionContext exec_ctx);

    };

}

#endif
