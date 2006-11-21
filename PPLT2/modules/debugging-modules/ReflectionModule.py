from core import CModule, IStreamModule
from core import CAsyncStreamConnection
from core import PPLTError, ItemBusy
from core import _fmtid;
import logging



class ReflectionModule(CModule, IStreamModule):
    _d_timeout  = None;
    _d_logger   = None;

    def __init__(self, parameters = None):
        CModule.__init__(self);

        try: self._d_timeout = float(parameters['timeout']);
        except: self._d_timeout = 0.1;

        self._d_logger = logging.getLogger("PPLT.core");
        self._d_logger.debug("Setup ReflectionModule with timeout %s"%self._d_timeout);

    def connect(self, addr, child=None):
        if not isinstance(addr,str):
            raise PPLTError("This module need addresses to connect.");

        self._d_logger.debug("connect with addr %s"%addr);
        
        if self._d_connections.count(addr)>=2:
            raise ItemBusy("There are allready 2 connection with addr %s"%addr);

        con = CAsyncStreamConnection(self, child, self._d_timeout);
        self._d_connections.addConnection(con,addr);
        return con;


    def disconnect(self, con_id):
        self._d_logger.debug("Close connection \"%s\" ..."%_fmtid(con_id));
        self._d_connections.remConnection(con_id);

    
    def write(self, con_id, data):
        (con,addr) = self._d_connections.getConnectionByID(con_id);
        if self._d_connections.count(addr) != 2:
            self._d_logger.warn("The other connection to %s is missing!", addr);

        cons = self._d_connections.getConnectionsByAddr(addr);
        if cons[0].identifier() == con_id: con = cons[1];
        else: con = cons[0];

        con.push(data);


    def list_connection(self):
        self._d_logger.debug("There are %i connections left:"%self._d_connections.count());
        for (cid, addr) in self._d_connections._d_id_addr_map.items():
            self._d_logger.debug("\t -> %s (%s)"%(addr, cid));


