# ########################################################################### #
# This is part of the PPLT project. PPLT is a framework for master-slave      #
# based communication.                                                        #
# Copyright (C) 2003-2006 Hannes Matuschek <hmatuschek@gmx.net>               #
#                                                                             #
# This library is free software; you can redistribute it and/or               #
# modify it under the terms of the GNU Lesser General Public                  #
# License as published by the Free Software Foundation; either                #
# version 2.1 of the License, or (at your option) any later version.          #
#                                                                             #
# This library is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU            #
# Lesser General Public License for more details.                             #
#                                                                             #
# You should have received a copy of the GNU Lesser General Public            #
# License along with this library; if not, write to the Free Software         #
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA   #
# ########################################################################### #
# This file contains the module-classes for the inside.



class baseModule:
    def __init__(self, Parent):
        self._ModuleParent
        self._ModuleChildTable = [];


    def addressMap(self, Address):
        """ This method has to be overwirtten! """
        return Address;


    def dispatchEvent(self, Event, From):
        """ This method should be overwritten. """
        pass;


    def _unregister(self, Module):
        """ In general this method has not to be overwitten """
        pass;


    def _register(self, Module, Address=None):
        """ In general this method has not to be overwitten """
        intAddr = self.addressMap(Address);
        self._ModuleChildTable.append( (Address, Module) );


    def _queryEvent(self, Event):
        """ This method queries the messages for this module. So please don't 
 overwrite this method. (Only if you know what you're doing.) """
        # wenn keine Nachricht verarbeitet wird -> durchreichen, 
        # an sonsten im stack einsortieren!
        # Sortiert wird nach priorität und nach timeElapsed()-Werten
        # je 1/8 der Zeit -> eine Stufe
        pass;


    def _emitEvent(self, Event, To=None):
        """ This method should be not overwritten """;
        # Holt das modul aus der Tabelle nach (To) oder all wenn Richtung=Oben
        # ruft Module._queryEvent(Event) auf:
        pass;






class baseInterfaceModule(baseModule):
    def __init__(self, Parent, Parameters):
        # init attributes:
        baseModule.__init__(self, Parent);
        self._LoadParameters = Parameters;
        #done!


    def start(self):
        # start if-thread:
        self._IFThread = thread.start_new_thread(self.run, (self,));
        

    def run(self): pass;


    def addressMap(self, Address):
        """ This method has to be overwirtten! """
        return Address;


    def dispatchEvent(self, Event, From):
        """ This method should be overwritten. """
        pass;
    
