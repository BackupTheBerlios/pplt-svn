import threading
import random
import time
from pplt import CModule, IValueModule, CValueConnection
from pplt import PPLTError


class RandomGenerator (CModule, IValueModule):
    _my_mean_period = None
    _my_variance = None
    _my_event_thread = None
    
    def __init__(self, parameters):
        CModule.__init__(self, parameters)

        self._my_mean_period = float(parameters['period'])
        self._my_variance    = float(parameters['variance'])

        self._my_event_thread = threading.Thread(None, self._my_event_loop, None, (self,))



    def connect(self, address, child=None):
        if not address in ["bool", "integer", "float", "period", "variance"]:
            raise PPLTError("Invalid address: %s"%address)

        con = CValueConnection(self, child)
        self._d_connections.addConnection(con, address)
        return con



    def disconnect(self, con_id):
        self._d_connections.remConnection(con_id)



    def set(self, con_id, value):
        (con,addr) = self._d_connections.getConnectionByID(con_id)
        if addr == "period":
            self._my_mean_period = float(value)
        elif addr == "variance":
            self._my_variance = float(value)
        else:
            raise PPLTError("The connection %s is read only!"%addr)



    def get(self, con_id):
        (con, addr) = self._d_connections.getConnectionByID(con_id)
        if addr == "bool":
            return random.choice([True,False])
        if addr == "integer":
            return random.randint(0,100)
        if addr == "float":
            return random.random()
        if addr == "period":
            return self._my_mean_period
        if addr == "variance":
            return self._my_variance
        raise Exception("Invalid address %s: This should never happen!"%(addr))



    def _my_event_loop(self):
        if not isinstance(self, RandomGenerator):
            raise Exception("oops...")

        while True:
            tts = random.gauss(self._my_mean_period, self._my_vaiance)
            time.sleep(tts)

            for cont in ["bool", "integer", "foat"]:
                cons = self._d_connections.getConnectionsByAddress(cont)
                for con in cons:
                    if cont == "bool":
                        con.push( random.choice([True,False]) )
                    if cont == "integer":
                        con.push( random.randint(0,100) )
                    if cont == "float":
                        con.psuh( random.random() )

                    



