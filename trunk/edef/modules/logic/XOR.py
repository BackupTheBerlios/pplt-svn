import edef

class XOR:
    def __init__(self):
        self.o_out = edef.ValueOutput(False)
        
        self._a = False
        self._b = False
    
    def i_a(self, value):
        self._a = value
        if self._a ^ self._b: self.o_out(True)
        else: self.o_out(False)
        
        
    def i_b(self, value):
        self._b = value
        if self._a ^ self._b: self.o_out(True)
        else: self.o_out(False)