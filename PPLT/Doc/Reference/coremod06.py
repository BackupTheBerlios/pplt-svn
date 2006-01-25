import pyDCPU;

# init core:
core = pyDCPU.Core();

# load module:
echo = core.MasterTreeAdd(None, "Master.Debug.Echo", None, None);

# create symbol:
core.SymbolTreeCreateSymbol("/echo", echo);

#do write/read:
core.SymbolTreeWrite("/echo", "Hello world...");
print core.SymbolTreeRead("/echo", 1024); # read max. 1024 bytes
