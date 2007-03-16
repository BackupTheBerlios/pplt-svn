import edef

class NOT:
    def __init__(self):
        self.o_out = edef.ValueOutput(False)

    def i_in(self, value):
        self.o_out(not value)
     
   