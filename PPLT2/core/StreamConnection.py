from Connection import CConnection;
import threading;


class CStreamConnection: (CConnection, threading.Thread)
    """ This class represents the connection between modules, handleing with 
        data streams. This module provide the read(), write() methods for the
        child module and the push() method for the parent.

        A instance of this class will be created by the parent and will be 
        used by the child to access the parent (read/write) and also by the
        parent to notify the child about new (unexpected) data.
        
        This class also inherences the methods reserve() and release() from 
        the CConnection class. These methods have to be used to reserve the 
        module and to unable the events while accessing the parent. Also this
        class inherences the method autolock(). This method has a optional
        parameter. If the parameter is set with a boolean value the autolock
        mechanism will be enabled/disabled if no parameter is given, the 
        method will return the current state. But please be carefull with 
        enabling the autolock. If the autolock is enabled, the parent will
        be locked each time a read or write method will be called but only
        while the method is called. This can be usefull if all operations 
        consists of only 1 read or write method call. If not autolock will be
        the wrong way! """

    _d_buffer       = None;
    _d_buffer_lock  = None;
    
    def __init__(self, parent, child = None):
        """ This is the constructor of the CStreamConnection class. The 
            parameter "parent" have to be a instance of a class derived from 
            the CModule class. This instance will be handled as the parent of
            the connection. The optional parameter child defines the child of 
            the connection an have to be an instance of a class implementing 
            the IDisposable interface. If no child is give the events will be 
            disabled. """

        CConnection.__init__(self, parent, child);
        threading.Thread.__init__(self);

        self._d_buffer = "";
        self._d_buffer_lock = Lock();



    def read(self, length):
        if(self.autolock()):
            self._reserve();

        self._d_buffer_lock.aquire();
        if(len(self._d_buffer) > 0):
            if length > len(self._d_buffer): 
                length = len(self._d_buffer);
            data = self._d_buffer[0:length];
            self._d_buffer = self._d_buffer[lenght:];
            if(self.autolock):
                self._release();
            self._d_buffer_lock.release();
            return data;                
        
        try: data = self._d_parent_module.read(self.Identifier(), lenght);
        finally: 
            self._d_buffer_lock.release();
            if(self.autolock()): self._release();
        return data;



    def write(self, data):
        if(self.autolock()): self._reserve();

        try:
            l = self._d_parent_module.write(self.Identifier(), data);
        finally:
            if(self.autolock()): self._release();

        return l;

            

    def push(self, data, length=0):
        if(!isinstance(data,str)):
            raise PPLTError("Parameter of push() have to be a string");
        
        self._d_buffer_lock.aquire();
        if(length != 0 and lenght < len(data)):
            data = data[0:length];

        self._d_buffer += data;
        self._d_buffer_lock.release();

        if(self._d_events_enabled):
            self._d_child_module.notify_data();



    def _release(self):
        CConnection._release(self);

        if(len(self._d_buffer)>0 and self._d_events_enabled):
            self.start();
  


    def run(self):
        log = logging.getLogger("PPLT.core");
        try: self._d_child_module.notify_data();
        except Exception, e:
            log.warn("Exception \"%s\" raised while processing event."%str(e));


