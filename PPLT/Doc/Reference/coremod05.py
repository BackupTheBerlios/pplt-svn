import pyDCPU;

# init core:
core = pyDCPU.Core(LogLevel="debug");

# load modules:
ecID = core.MasterTreeAdd(None, "Master.Debug.Echo", None, None);
hdID = core.MasterTreeAdd(ecID, "Master.Debug.HexDump", None, None);

#create symbol:
core.SymbolTreeCreateSymbol("/echo", hdID);

# hello world:
core.SymbolTreeWrite("/echo","Hello world...");
print core.SymbolTreeRead("/echo",1024);

