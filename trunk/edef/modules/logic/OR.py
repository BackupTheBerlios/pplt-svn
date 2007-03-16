import edef

class OR:
    def __init__(self):
        self._d_in_a = None
        self._d_in_b = None
        self.o_out = edef.BoolOutput(False)

    def i_a(self, value):
        self._d_in_a = value
        if self._d_in_a or self._d_in_b:
            self.o_out(True)
        else:
            self.o_out(False)
     
    def i_b(self, value):
        self._d_in_b = value
        if self._d_in_a or self._d_in_b:
            self.o_out(True)
        else:
            self.o_out(False)     