
import Object;
import threading;

class CModule: (CObject)
    _d_module_lock = None;
    _d_module_parameters = None;

    def __init__(self, parameters):
        CObject.__init__(self);
        self._d_module_lock = threading.Lock();
        self._d_module_parameters = parameters;
        
    def reserve(self): self._d_module_lock.acquire();
        
    def release(self): self._d_module_lock.release();

