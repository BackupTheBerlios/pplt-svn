from EventManager import EventManager
import logging



class BaseOutput:
    _d_inputs           = None # List of inputs connected to this output
    _d_event_manager    = None
    _d_logger           = None


    def __init__(self):
        """ Constructor of an output pin. This constructor takes a referece to
            the event-manager. """
        self._d_inputs = dict()
        self._d_event_manager = EventManager.factory()
        self._d_logger = logging.getLogger("PPLT.core")


    def __call__(self, value):
        """ This method will be used to set the value of this output. Simply
            call o_out(value) to set the value """
        self.set_value(value)


    def __rshift__(self, inp):
        """ This operatior is used to add this putput as an event-source to 
            the other input. The usage is ModA.o_out >> ModB.i_in
            inp should be a callable."""
        self.add_input(inp)


    def __iadd__(self, inp):
        """ Does the same like __rshift__() but can be used otherwise:
            ModA.o_out += ModB.i_in """
        self.add_input(inp)
        return self

    
    def __isub__(self, inp):
        """ Removes the given input from this output.
            Usage: ModA.o_out -= ModB.i_in """
        self.rem_input(inp)
        return self


    def __contains__(self, inp):
        """ This method should return true if the give input is connected to 
            this output.
            
            Usage: if ModB.i_in in ModB.o_out: pass
            
            inp should be a callable. """
        return self.has_input(inp)


    def set_value(self, value):
        self._d_logger.debug("Set output %s to %s"%(id(self),value))

        for inp in self._d_inputs.values():
            self._d_event_manager.add_event(inp, value)


    def add_input(self, callback):
        if not id(callback) in self._d_inputs.keys():
            self._d_inputs[id(callback)] = callback


    def rem_input(self, callback):
        del self._d_inputs[id(callback)]


    def has_input(self, callback):
        return id(callback) in self._d_inputs.keys()




class ValueOutput(BaseOutput):
    _d_last_value = None

    def __init__(self, init_value=None):
        BaseOutput.__init__(self)
        self._d_last_value = init_value


    def __call__(self, value):
        if self._d_last_value == value:
            return
        
        self._d_last_value = value
        BaseOutput.__call__(self, value)

    
    def add_input(self, callback):
        if self.has_input(callback):
            return

        BaseOutput.add_input(self, callback)
        self._d_event_manager.add_event(callback, self._d_last_value)


    def last_value(self):
        return self._d_last_value




class StreamOutput(BaseOutput):
    pass


class FrameOutput(BaseOutput):
    pass


