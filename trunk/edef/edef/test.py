import edef
import time


def TestOut(value):
    print "Value: %s"%value


class AND:
    def __init__(self):
        self.o_out = edef.ValueOutput(False)
        self._d_in_a = False
        self._d_in_b = False

    @edef.BoolDeco
    def i_a(self, value):
        self._d_in_a = value
        if self._d_in_a and self._d_in_b:
            self.o_out(True)
        else:
            self.o_out(False)

    @edef.IntegerDeco
    def i_b(self, value):
        self._d_in_b = value
        if self._d_in_a and self._d_in_b:
            self.o_out(True)
        else:
            self.o_out(False)



# TEST
edef.Logger()
gate = AND()
try:
    gate.o_out += gate.i_a
    gate.o_out += TestOut
finally:
    time.sleep(0.1)
    edef.EventManager().stop()
