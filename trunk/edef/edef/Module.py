""" This file contains definitions for all module-types. There is a DynamicModule 
    class which sould be used as a super-class for all modules that have a
    dyamic count of input or outputs. Look at the documentation of the 
    L{DynamicModule} class for more information.

    Additionally there is a L{InputWrapper} class that can be used to 
    implement inputs as attributes instead of methods.

    There is no superclass for "simple" modules. Because ther is no need for.
    To build a simple module with a static count of inputs and outputs, you 
    have to write a class whith some methods called like C{i_*()} and with 
    some attributes called C{o_*}. The o_* attributes represent the outputs 
    and should be instances of L{ValueOutput}, L{StreamOutput} or 
    L{FrameOutput}. The inputs are relized by simple methods taking one 
    argument, the value. this method should process the new value and update
    all outputs by calling something like C{self.o_OUTPUTNAME(new_value)}. 
    
    A simple AND module example. This module has two inputs C{a},C{b} and one 
    output C{out}. If C{a} and C{b} is true the output will also be true. A 
    simple AND-gate. block::
        import edef
        import time 

        class AND:  
            def __init__(self):
                # define internal values:
                self._in_a = False
                self._in_b = False
                # define output (with initial value False):
                self.o_out = edef.ValueOutput(False)

            # Input "a":
            def i_a(self, value):
                self._in_a = value
                if self._in_a and self._in_b:
                    self.o_out(True)
                else:
                    self.o_out(False)

            # Input "b":
            def i_b(self, value):
                self._in_b = value
                if self._in_a and self._in_b:
                    self.o_out(True)
                else:
                    self.o_out(False)

    
        #                    
        # Testcode:
        #
        # Callback for output:
        def my_cb(self, value):
            print "Output is now: %s"%Value

        # init Eventhandler:
        evt = edev.EventHandler()

        # create gate:
        gate = AND()
        # connect callback to output:
        gate.o_out += my_cb
        # set input A = True
        gate.i_a(True)
        # set intput B = True
        gate.i_b(True)
        # set output B = False
        gate.i_b(False)

        # give Eventhandle some time to handle events:
        time.sleep(0.1)
        # stop eventhandler:
        evt.stop()
        
    This is a simple example how to write simple modules and how to use them.         
        """ 

import re



class InputWrapper:
    _d_callback = None
    _d_args     = None
    _d_name     = None

    def __init__(self, module, name, kwargs=None):
        self._d_callback    = module.input_dispacher
        self._d_args        = kwargs
        self._d_name        = name

    def __call__(self, value):
        return self._d_callback(self._d_name, value, self._d_args)




class DynamicModule:
    def __init__(self):
        pass

    def __getattr__(self, name):
        if re.match("^i_",name):
            return self.create_input(name)
        elif re.match("^o_",name):
            return self.create_output(name)
        else:
            raise AttributeError("Attribute %s not found"%name)

    
    def create_output(self, name):
        raise AttributeError("Attribute %s not found"%name)
    
    
    def create_input(self, name):
        raise AttributeError("Attribute %s not found"%name)

    
    def input_dispacher(self, name, kwargs=None):
        raise NotImplemented("The method input_dispacher have to be overridden!")
