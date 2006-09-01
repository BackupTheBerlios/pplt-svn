
import Exceptions;
import Object;
import Interfaces;

class CConnection: (CObject)
    _d_events_enabled   = None;
    _d_autolock         = None;
    _d_parent_module    = None;
    _d_child_module     = None;
    _d_event_status     = None;
    
    def __init__(self, parent, child = None):
        CObject.__init__(self);
        if(!isinstance(parent, CModule)):
            raise CorruptInterface("Parentmodule have to inherence CModule!");

        if(None == child): self._events_enabled = False;
        elif(!isinstance(child, IDisposable)):
            raise CorruptInterface("Child have to inherence IDisposable!");

        self._d_parent_module   = parent;
        self._d_autolock        = False;
        self._d_events_enabled  = True;
        self._d_event_status    = True;
        self._d_child_module    = child;


    def __del__(self):
        if(None != self._d_parent_module): 
            self._d_parent_module.close(self.Identifier());

    def reserve(self):
        log = logging.getLogger("PPLT.core");
        if(self._d_autolock):
            log.warn("Autolock enabled AND reserve called: This may cause into a deadlock!");
        self._reserve();


    def _reserve(self):        
        self._d_event_status = self._d_events_enabled;
        self._d_events_enabled = False;
        self._d_parent_module.reserve();



    def release(self):
        log = logging.getLogger("PPLT.core");
        if(self._d_autolock):
            log.warn("Autolock enabled AND release() called!");
        self._release();


    def _release(self):
        self._d_events_enabled = self._d_event_status;
        self._d_parent_module.release();



    def autolock(self, status = None):
        if(status == None): return self._d_autolock;
        if(not status in [True, False]):
            raise PPLTError("Only boolean values are allowed as parameters for autolock()");
        self._d_autolock = status;
        return None;
           
        
