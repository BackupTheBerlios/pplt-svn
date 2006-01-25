import pyDCPU;

core = pyDCPU.Core();

# load serial interface:
serID = core.MasterTreeAdd(None, "Master.Interface.UniSerial", None,
                           {'Port':'0', 'Speed':'9600', 'Parity':'Even',
                            'TimeOut':'1.0'});
# load PPI:
ppiID = core.MasterTreeAdd(serID, "Master.Transport.PPI", None,
                           {'Address':'0'});

#create symbols:
core.SymbolTreeCreateSymbol("/ppi1",ppiID, '1');
core.SymbolTreeCreateSymbol("/ppi2",ppiID, '2');

# Now you can read/write directly from/to the PPI BUS by using the
# SymbolTreeRead() and SymbolTreeWrite() core-methods. 
# If you read/write from/to the symbol /ppi1 you will recv/send packages
# from/to the device address by #1 and the symbol /ppi2 is for the device
# #2. 
