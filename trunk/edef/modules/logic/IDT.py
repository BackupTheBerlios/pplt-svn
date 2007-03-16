import edef

class IDT:
    def __init__(self):
        self.o_out = edef.ValueOutput()

    def i_in(self, value):
        self.o_out(value)
 
