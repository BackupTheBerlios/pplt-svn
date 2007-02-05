""" 
    Outputs manage connections to inputs and interface the L{EventManager}.
    So they are an important part of the I{edef} system. 
   
    There are differen output types for different cases. For example there is
    an output for simple values (L{ValueOutput}) for data streams 
    (L{StreamOutput)) and for sequences of values (L{FrameOutput}). 

    An simple example how to use the L{ValueOutput} in any context may be:
        import edef
        import time

        def cb_one(value):
            print "Callback one, new value: %s"%value
        def cb_two(value):
            print "Callback two, new value: %s"%value
        
        out1 = edef.ValueOutput(False)
        out2 = edef.ValueOutput(False)

        # add cb_one and cb_two to out1:
        out1 += cb_one
        out1 >> cb_two

        # add cb_one to out2:
        out2 += cb_one

        # set some values:
        out1(True)
        out2(True)

        # let eventhandler time to work:
        time.sleep(0.1)

        # remove cb_one from out1:
        out1 -= cb_one
    
        # test if successfull:
        assert not cb_one in out1

        # reset some values:
        out1(False)
        out2(False)

        # let eventhandler work
        time.sleep(0.1)
        # Stop eventhandler
        edef.EventHandler().stop()

    This example defines two functions, as inputs and instances two 
    ValueOutputs. Then the inputs are connected to the outputs and the values
    of the outputs are updated. The line C{time.sleep(0.1)} ensures, that the
    eventhandler has enough time to handle the emitted events of the outputs.
    Then one input (C{cb_one}) is removed from the input C{out1} and the value
    of the outpus is reseted. Finally we let the eventhandler work and stop it. 

    """

# ########################################################################## #
# Output.py
#
# 2007-01-24
# Copyright 2007 Hannes Matuschek
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



from EventManager import EventManager
import logging



class BaseOutput:
    """ This is the base class for all output types. Please do not use this
        output directly. Use one of L{ValueOutput}, L{StreamOutput} or
        L{FrameOutput} instead. 
        
        All other types are subclassed from this one. But they provide some 
        additional functions or other behavior like this."""
    _d_inputs           = None # List of inputs connected to this output
    _d_event_manager    = None
    _d_logger           = None


    def __init__(self):
        """ Constructor of an output pin. This constructor takes a referece to
            the event-manager. """
        self._d_inputs = dict()
        self._d_event_manager = EventManager()
        self._d_logger = logging.getLogger("edef.core")


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
        """ This method will be called by the __call__ special method to set 
            the value of the output. Please use the __call__ method instead of
            calling this method directly. Also the __call__method will provide
            some eye-candy for you. Simple do C{output(new_value)} to set the 
            new value to the output. """
        self._d_logger.debug("Set output %s => %s"%(getattr(self,"__name__",self),value))

        for inp in self._d_inputs.values():
            self._d_event_manager.add_event(inp, value)


    def add_input(self, callback):
        """ This method will add an input to the output. This input will be
            called if the value of the output changes. Please use the 
            overwritten operator C{+=} or C{>>} to add new inputs to an 
            output instead of calling this method direct. Example:
            C{output += new_input} or C{output >> another_input}. The imput 
            should be a I{callable} that takes only one argument, may be a 
            function or a method of a class. """
        if not id(callback) in self._d_inputs.keys():
            self._d_inputs[id(callback)] = callback


    def rem_input(self, callback):
        """ This method will remove the given input from this output. But 
            PLEASE do not call this method direct! Use the overwritten 
            operator C{-=} instead. 
            Example: C{output -= any_input_added_first}
            If the given input was not added to the output first, this method
            will raise an exception. """
        del self._d_inputs[id(callback)]


    def has_input(self, callback):
        """ This method will return True if the given input was added to this 
            output and False otherwise. Please do not use this method direct. 
            Use the overwritten operator C{in} instead: 
            C{if any_input in output: do_somethin()} """
        return id(callback) in self._d_inputs.keys()




class ValueOutput(BaseOutput):
    """ The ValueOutput is specialized version of L{BaseOutput} for dealing 
        with values like boolean, integer, floats, complex or strings. The 
        main difference is, that you can obtain the last value of this output
        by calling C{last_value()}. Additionaly there will be an event emmited
        to an input that was just added to the output. The output will only 
        emmit events, if its value changes not if a value was set!"""
    _d_last_value = None

    def __init__(self, init_value=None):
        """ This constructor can optional take the initial value of the 
            output. """
        BaseOutput.__init__(self)
        self._d_last_value = init_value


    def __call__(self, value):
        """ This method will set the internal value to C{value} and emmit 
            events to all connected inputs. Usage: output(value)"""
        if self._d_last_value == value: return
        self._d_last_value = value
        BaseOutput.__call__(self, value)

    
    def add_input(self, callback):
        """ This method will add the given imput to the input list. Please do
            not use this method directly. Use the overwritten operators 
            C{output += an_input} or C{output >> another_input} instead. """
        # if input was allready added:
        if self.has_input(callback): return
        # check if it is no stream- or frame-input:
        if not getattr(callback, "dec_type_name", None):
            self._d_logger.warning("No Type-Decorator was set to the input.")
        elif not callback.dec_type_name in ["bool", "int", "float", "complex", "str"]:
            # FIXME An exception may be to mutch...
            raise TypeError("The callback should be value-typed");
            self._d_logger.exception("Bad callback-type")

        BaseOutput.add_input(self, callback)
        if not self._d_last_value is None:
            self._d_event_manager.add_event(callback, self._d_last_value)


    def last_value(self):
        """ This method will return the last value or inital value of the 
            output. """
        return self._d_last_value




class StreamOutput(BaseOutput):
    def add_input(self, callback):
        """ This method adds the given input to this output. Pleas do not use
            this method directly. Use the overwritten operators C{+=} or C{>>}
            instead. """
        if not getattr(callback, "dec_type_name", None):
            self._d_logger.warning("No Type-Decorator was set to the input.")
        if not callback.dec_type_name == "stream":
            raise TypeError("This output needs a StreamDecorated input! (got %s)"%type(callback))
            self._d_logger.exception("Wrong inputtype!")
        BaseOutput.add_input(self, callback)




class FrameOutput(BaseOutput):
    def add_input(self, callback):
        """ This method adds the given input to this output. Pleas do not use
            this method directly. Use the overwritten operators C{+=} or C{>>}
            instead. """
        # FIXME: add type-check!
        BaseOutput.add_input(self, callback)

        



class BoolOutput(ValueOutput): pass #FIXME override add_input() and check type
class IntegerOutput(ValueOutput): pass #FIXME override add_input() and check type
class FloatOutput(ValueOutput): pass #FIXME override add_input() and check type
class ComplexOutput(ValueOutput): pass #FIXME override add_input() and check type
class StringOutput(ValueOutput): pass #FIXME override add_input() and check type

class BoolSeqOutput(FrameOutput): pass #FIXME override add_input() and check type
class IntegerSeqOutput(FrameOutput): pass #FIXME override add_input() and check type
class FloatSeqOutput(FrameOutput): pass #FIXME override add_input() and check type
class ComplexSeqOutput(FrameOutput): pass #FIXME override add_input() and check type
    
