import pyDCPU;
import parallel;


# ### --- UniParallel ---
# A platform-indipendent implementation of the prallelport. Useing the pyparallel 
# pythonmodule [http://pyserial.sf.net].
#
# This module provides following connectors:
# ----------------------------------------------------------------------------
#   [None]  --- (Stream) (io)   IEEE 1284 implementation (TODO) 
#   p0..p1  --- (Bool) (io)     the singe pins of the parallel port
#   STROBE  --- (Bool) (o)     
#   ACK     --- (Bool) (i)
#   BUSY    --- (Bool) (i)
#   PE      --- (Bool) (i)
#   SLCT    --- (Bool) (o)
#   FD      --- (Bool) (o)
#   ERROR   --- (Bool) (i)
#   INIT    --- (Bool) (o)
#   SLCT_IN --- (Bool) (i)
# ----------------------------------------------------------------------------

class Object(pyDCPU.MasterObject):
    def setup(self):
        port = int(self.Parameters["Port"]);
        self.ParallelPort = parallel.Parallel(port);
        # reserve port:
        # 

    def destroy(self):
        # free port
        pass;
        
    def connect(self,Address):
        ValidAddresses = ("p0","p1","p2","p3","p4","p5","p6","p7","STROBE", "ACK", "BUSY", 
                          "PE", "SLCT", "FD", "ERROR", "INIT", "SLCT_IN");
        if Address in ValidAddresses:
            con = pyDCPU.ValueConnection(self, "Bool", Address);
        else: raise pyDCPU.Exceptions.ModuleSetup("Can't connect to parallel port: Unknown address: %s");    
        return con;    

    def read(self, Connection, Len=None):
        Addr = Connection.Address;
        if Addr in ("STROBE","SLCT","FD","INIT"):
            raise pyDCPU.Exceptions.AccessDenied("UNIPARALLEL: The pin %s is write-only!"%Addr);
        if Addr == "ACK": return self.ParallelPort.getInAcknowlege();
        elif Addr == "BUSY": return self.ParallelPort.getInBusy();
        elif Addr == "PE": return self.ParallelPort.getInPaperOut();
        elif Addr == "ERROR": return self.ParallelPort.getInError();
        elif Addr == "SLCT_IN": return self.ParallelPort.getInSelected();
        else: raise pyDCPU.Exceptions.Error("Connector %s not implemented yet."%Addr);
        
    def write(self, Connection, Data):
        raise pyDCPU.Exceptions.Error("Write not implemented yet."); 
