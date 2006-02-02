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


    def unregister(self, Module):
        """ In general this method has not to be overwitten """
        pass;


    def register(self, Module, Address=None):
        """ In general this method has not to be overwitten """
        intAddr = self.addressMap(Address);
        self._ModuleChildTable.append( (Address, Module) );


    def queryEvent(self, Event):
        """ In general this method has not to be overwritten! """
        pass;


    def emitEvent(self, Event, To=None):
        """ This method should be not overwritten """;
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
    
