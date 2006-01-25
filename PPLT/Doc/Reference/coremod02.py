import pyDCPU;

core = pyDCPU.Core();

# load "Socket"-module:
SoID = core.MasterTreeAdd(None, "Master.Interface.Socket", None,
                          {'TimeOut':'1.0'});
# crate two symbole (including connections)
core.SymbolTreeCreateSymbol("/con1", SoID, "10.1.1.1:80");
core.SymbolTreeCreateSymbol("/con2", SoID, "10.1.1.2:100");

# do a little HTTP:
core.SymbolTreeSetValue("/con1",'GET / HTTP\\1.0\n\r\n\r');
print core.SymbolTreeRead("/con1",1024);    #read max. 1024 bytes from stream

# read from con2:
print core.SymbolTreeRead("/con2",1024);

