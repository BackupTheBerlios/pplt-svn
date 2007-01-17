from Output import ValueOutput
from EventManager import EventManager
import time
import logging
from Module import DynamicModule, InputWrapper

def my_callback(value):
    print "Got %s"%value


class NotModule(DynamicModule):
    
    def __init__(self):
        DynamicModule.__init__(self)
        self.o_out = ValueOutput(False)
        self.i_in  = InputWrapper(self, "in")

    def input_dispacher(self, name, value, args):
        self.o_out(not value)

    def create_output(self, name):
        return self.o_out
       



mod = NotModule()

try:
    mod.o_out += my_callback
    mod.i_in(False)

finally:
    time.sleep(0.01)
    EventManager.factory().stop()

