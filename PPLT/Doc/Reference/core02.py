import pyDCPU;

PPI_ADDRESS = "0";  # bus-address of the PC 
S7_ADDRESS  = "2";  # bus address of the S7

[...]

core = pyDCPU.Core();

# load serial-interface module:
ser_id = core.MasterTreeAdd(None, "Master.Interface.UniSerial", 
                            None, {"Port":"0", "Speed":"9600", 
                                   "TimeOut":"0.5", "Parity":"Even"});

# load PPI module (and attach to serial-interface):
ppi_id = core.MasterTreeAdd(ser_id, "Master.Transport.PPI", 
                            None, {"Address":PPI_ADDRESS});

#load S7 module (and attach to PPI-module):
s7_id  = core.MasterTreeAdd(ppi_id, "Master.Device.S7", 
                            S7_ADDRESS, None);

[...]
