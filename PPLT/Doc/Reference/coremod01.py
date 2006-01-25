import pyDCPU;

core = pyDCPU.Core();

SerID = core.MasterTreeAdd(None, "Master.Interface.UniSerial", None,
                           {'Port':'0', 'Speed':'9600', 'Parity':'None',
                            'TimeOut':'0.5'});

core.SymbolTreeCreateSymbol("/serial", SerID);  # connect to data-channel
core.SymbolTreeCreateFolder("/config");
core.SymbolTreeCreateSymbol("/config/speed", SerID, 'speed');
core.SymbolTreeCreateSymbol("/config/parity", SerID, 'parity');
core.SymbolTreeCreateSymbol("/config/timeout", SerID, 'timeout');

# read max 1024 bytes from serial interface:
buff = core.SymbolTreeRead("/serial", 1024);
# echo them back:
core.SymbolTreeWrite("/serial", buff);

#get current speed:
speed = core.SymbolTreeGetValue("/config/speed");
print "Current speed: %i Baud"%speed;
#reset speed:
core.SymbolTreeSetValue("/config/speed",115200);

