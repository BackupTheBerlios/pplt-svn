# ########################################################################## #
# Object.py
#
# 2006-09-01
# Copyright 2006 Hannes Matuschek
# hmatuschek@gmx.net
# ########################################################################## #
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# ########################################################################## #

import logging;
import random;
from Tools import _fmtid;


class CObject:
    """ This is the base class for all classes used to have unique instances.
        All classes derived from this will have a method called Identifier()
        that retunrs a unique ID for that instance. This will be used to 
        identify module, connection and symbol-instances. """ 
    _d_identifiers = [];
    _d_identifier  = None;

    
    def __init__(self):
        log = logging.getLogger("PPLT.core");
        self._d_identifier = self._make_id();
        while self._d_identifier in CObject._d_identifiers:
            self._d_identifier = self._make_id();
        CObject._d_identifiers.append(self._d_identifier);                    
        log.debug("Object (%s) created with ID %s"%(str(self), _fmtid(self._d_identifier)) );



    def __del__(self): 
        try: CObject._d_identifiers.remove(self._d_identifier);
        except Exception, e:
            log = logging.getLogger("PPLT.core");
            log.error("Unable to remove ID %s from list: [%s]"%(_fmtid(self._d_identifier), self._d_identifiers));
            raise e; 
   


    def Identifier(self):
        """ This method will return the unique identifier for the instance. 
            """
        return self._d_identifier;

    
    
    def _make_id(self):
        obj_id = '';
        for n in range(64): obj_id += random.choice('0123456789abcdef');
        return obj_id;
        
