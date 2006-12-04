# ########################################################################## #
# Module.py
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


from Object import CObject
from ConnectionDatabase import CConnectionDatabase
import threading
import logging
from Tools import _fmtid



class CModule (CObject):
    """ This is the baseclass for all Mmodule classes. This class imeplements
        the basic needs for a module. Ie Locking. This locking is used to 
        ensure that only child accesses a module simultaneously. The methods
        reserve() and release() where never be called directly by the child
        insteat they call the reserve and release methods of the connection
        instance. Note: A module have to implement the connect() and 
        disconnect() methods."""

    _d_module_lock = None
    _d_module_parameters = None
    _d_connections = None


    def __init__(self, parameters = None):
        """ This is the constructor. The parameter "parameters" specifies the
            parameter for the sprcific module. These can be used to setup the
            module correctly. This class contains a CConnectionDatabase 
            instance as the _d_conenctions attribute. Please use it to manage
            your conenctions! Else if you don't want to use it or if you can't
            please override the is_busy() method also! This method returns 
            True if there are connections to the specific module. """
        CObject.__init__(self)
        
        if None == parameters:
            parameters = {}

        self._d_module_lock = threading.Lock()
        self._d_module_parameters = parameters
        self._d_connections = CConnectionDatabase()

        self._d_logger = logging.getLogger("PPLT.core")


    
    def __del__(self):
        if self.is_busy():
            self._d_logger.warning("Destruction of module %s but is_busy() == True"%_fmtid(self.identifier()))
        CObject.__del__(self)



    def reserve(self):
        """ This method will be used by the connection objects to reserve 
            (lock) this module. Normaly this method doesn't need to be 
            overridden, a module doesn't need to know if it is reserved or 
            not.""" 
        self._d_module_lock.acquire()



    def release(self):
        """ This method releases the module. This method will be called by the
            connection object retuned from the connect() method of the module
            implementation. """
        self._d_module_lock.release()



    def connect(self, address, child=None):
        """ This method have to be overridden by the module implementation. 
            This method tooks the address and the optional child module and
            should return a connection instance of the proper type. 
            For example a CStreamConnection instance if the connection handles
            streams. """
        raise NotImplemented("The method connect() have to be implemented!");



    def disconnect(self, con_id):
        """ This method have to be overridden to implement the diconnect 
            method. The parameter conid specifies the identifier of the 
            connection instance. This one can be obtained by calling the
            Indentifier() method of the connection instance (all connections
            have one). """
        raise NotImplemented("The method disconnect() have to be implemented!");



    def is_busy(self):
        """ This method returns True if there are connections left to the module.
            This method uses the module internal ConnectionDatabase insatance
            to determ if there are connection left. If a module implementation
            doesn't use this db to strore and manage the connection this method
            have to be overridden! """
        return 0 != self._d_connections.count();



