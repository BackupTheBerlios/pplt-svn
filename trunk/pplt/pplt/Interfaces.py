""" This module holds all interfaces specified for the PPLT2 core. """

# ########################################################################## #
# Interfaces.py
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



class IDisposable:
    """ This interface defines what methods have to be inplemented to be 
        "Disposable" meaning to recive events that signal that data may have 
        changed. Ie the CInnerModule class have to implement this interface to
        be able to handle events."""

    def notify_data(self):
        """ This method will be called by the parent to notify that his state
            have changed. Normaly a CInnerModule implementation will have this 
            method. So override it to handle events. """
        raise NotImplemented("The notify_data() method have to be implemented!");





class IStreamModule:
    """ This interface defines the methods have to be implemented to be a 
        StreamModule. This means that the module can provide data streams.
        A StreamConenction instance will check if the parent iherence this
        interface to be sure that the module will provide the proper 
        interface. """

    def read(self, con_id, length):
        """ This method have to be implented by the module implemtation. 
            The parameter con_id specifies the identifier of the connection
            who calls this method. The identifier can be obtained by calling
            the Identifier() method of the connection instance. The parameter
            length specifies the max. number of bytes this method should 
            return. """
        raise NotImplemented("This read() method have to be implemented!");

    def write(self, con_id, data):
        """ This method have to be implented by the module implemtation. 
            The parameter con_id specifies the identifier of the connection. 
            This identifier can be obtained by calling the Identifier() method
            of the connection insztance. data specifies the string send by the
            connection. """
        raise NotImplemented("This read() method have to be implemented!");





class ISequenceModule:
    """ """
    
    def recv(self, con_id):
        raise NotImplemented("This recv() method have to be implemented!");

    
    def send(self, con_id, msg):
        raise NotImplemented("This send() method have to be implemented!");





class IValueModule:
    """ This interface specifies the methods that are needed to be implemented
        for an uniform interface for modules that provide single values.""" 

    def set(self, con_id, value):
        """ This method will be used by other modules or any application to 
            set the value of the connection. This method should be implemented
            by all modules that derive from the IValueModule interface. 

            The first parameter specifies the connection id. This id can be 
            used to determ what value should be set. The second parameter 
            specifies the value set. """
        raise NotImplemented("This set() method have to be implemented by the module!")

    def get(self, con_id):
        """ This method will be used by other modules or any application to get 
            the actual value of a connection. This method should be implented 
            by the module.

            The first parameter specifies the connection id. This id can be 
            used to determ which value is wanted. """
        raise NotImplemented("This method should be implemented by the module!")

