import pyDCPU;

core = pyDCPU.Core();

SerID = core.MasterTreeAdd(None, "Master.Interface.UniSerial", None,
                           {'Port':'0', 'Speed':'9600', 'Parity':'None',
                            'TimeOut':'1.0'});

StaID = core.MasterTreeAdd(SerID, "Master.Debug.Statistic", None, None);

# instead of direct export the serial-module
# I will export the data-tunnel of the statistic-module
core.SymbolTreeCreateSymbol("/serial", StaID);
# creat folder ans symbols for stat. values:
core.SymbolTreeCreateFolder("/stat");
core.SymbolTreeCreateSymbol("/stat/read_bytes", StaID, "read_data");
core.SymbolTreeCreateSymbol("/stat/write_bytes", StaID, "write_data");
core.SymbolTreeCreateSymbol("/stat/read_speed", StaID, "read_speed");
core.SymbolTreeCreateSymbol("/stat/write_speed", StaID, "write_speed");
core.SymbolTreeCreateSymbol("/stat/errors", StaID, "error");

#write something to the serial interface:
core.SymbolTreeWrite("/serial", "Hallo world...");
#get and print statistic:
num = core.SymbolTreeGetValue("/stat/write_bytes");
speed = core.SymbolTreeGetValue("/stat/write_speed");
errors = core.SymbolTreeGetValue("/stat/errors");
print "Written %i bytes (%fb/s) with %i errors."%(num,speed,errors);


