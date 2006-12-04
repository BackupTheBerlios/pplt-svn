""" This module contains the definitions of the L{CInnerModule} and 
    L{CDisposableModule} classes. You have to derive a module from one of this
    classes if you want to write a module that is able to be set on the top of
    an other module. The main difference between a simple inner module and the 
    disposable one, is that the disposable is able to handle events. Therefore
    you have to implement a notify_data() method. This method will be called 
    if an event reaches the module. """

# ########################################################################## #
# InnerModule.py
#
# 2006-11-21
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



from Module import CModule
from Interfaces import IDisposable

class CInnerModule (CModule):
    """ The CInnerModule class extends the interface of a module to be able to
        be connected to an other module. Therefore ther have to be passed a 
        patenmodule and a address to the constructor. The constructor will 
        create the connection to the parent. This connection will be closed if
        the module will be destroyed. So you don't need to care about it. 
        
        The parent_connection will be stored into the _d_parent_connection 
        attribute all CInnerModules inhert. You may want to check if the 
        parent-module provide the correct interface so your module can send 
        any messages to it."""
    _d_parent_connection = None


    def __init__(self, parent, address=None, parameters=None):
        """ The constructor of this class. If you derive your module from this
            class you should call this constructor, beacuse it will  create 
            the connection to the parent module in a proper way. Maybe you 
            want to check if the parent module provied to correct interface 
            for your module before you call the constructor. May be in this 
            way:

            >>> class MyModule (CInnerModule, IStreamModule):
            >>>     # This module will be an inner-module providing a data 
            >>>     # stream. Maybe it needs a Stream or Sequence module as 
            >>>     # parent!
            >>>     def __init__(self, parent, address, params):
            >>>         # check interface of parent:
            >>>         if not isinstance(parent, (ISequenceModule,IStreamModule)):
            >>>             raise PPLTError("Invalid parent module!!! ...")
            >>>         # call now the constructor of the super-class:
            >>>         CInnerModule.__init__(self, parent, address, params)
            """
        # init super-class
        CModule.__init__(self, parameters)

        self._d_logger.debug("Create connection to parent with addr %s"%address)
        self._d_parent_connection = parent.connect(address)





class CDisposableModule (CModule, IDisposable):
    """ This class extends the L{CInnerModule} interface by the data_notify 
        method. This method will be called by the parent to notify the child 
        about an event. These events are like "there is new data" or 
        "value have changed". The semantic of the event will be determed by 
        the module that recives the event. Therefore it may be possible that a
        module can not understand the event emitted by the parent. """
    _d_parent_connection = None;

    def __init__(self, parent, address=None, parameters=None):
        """ The constructor of this class. If you derive your module from this
            class you should call this constructor, beacuse it will  create 
            the connection to the parent module in a proper way. Maybe you 
            want to check if the parent module provied to correct interface 
            for your module before you call the constructor. May be in this 
            way:

            >>> class MyModule (CDisposableModule, IStreamModule):
            >>>     # This module will be an disposable-module providing a
            >>>     # data stream. Maybe it needs a Stream or Sequence module 
            >>>     # as parent!
            >>>     def __init__(self, parent, address, params):
            >>>         # check interface of parent:
            >>>         if not isinstance(parent, (ISequenceModule,IStreamModule)):
            >>>             raise PPLTError("Invalid parent module!!! ...")
            >>>         # call now the constructor of the super-class:
            >>>         CDisposableModule.__init__(self, parent, address, params)
            """
        # init superclass
        CModule.__init__(self, parameters)

        self._d_logger.debug("Create connection to parent with addr %s"%address)
        self._d_parent_connection = parent.connect(address, self)


