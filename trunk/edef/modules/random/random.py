import random
import edef

class RandomGen:
    def __init__(self):
        self.o_bool = edef.ValueOutput(False)
        self.o_int  = edef.ValueOutput(0)
        self.o_float = edef.ValueOutput(0.0)
        self.o_complx = edef.ValueOutput(0.0)
        
    def i_trigger(self, value):
        self.o_bool( random.choice([True,False]) )
        self.o_int( random.randint(0,100) )
        self.o_float( random.uniform(0,1) )
        self.o_complx( random.uniform(0,1)+random.uniform(0,1)*1j )




class Randomize:
    def __init__(self, variance=0.0):
        self._variance = float(variance)
        self.o_out = edef.ValueOutput(0.0)

    def i_in(self, value):
        value = float(value)
        rv = random.gauss(0,self._variance)
        self.o_out( value + (value * rv) )
