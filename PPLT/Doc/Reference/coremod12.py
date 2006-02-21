import pyDCPU;

core = pyDCPU.Core();

serID = core.MasterTreeAdd(None, "Master.Interface.UniSerial",
                           None, {"Port":"0", "Parity":"None",
                           "TimeOut":"1.0", "Speed":"115200"});
gsmID = core.MasterTreeAdd(serID, "Master.Device.GSM", None, None);

core.SymbolTreeCreateSymbol("/sms", gsmID, "sms:01624779681");
core.SymbolTreeCreateSymbol("/net", gsmID, "network");
core.SymbolTreeCreateSymbol("/bat", gsmID, "battery");
core.SymbolTreeCreateSymbol("/qua", gsmID, "quality");
core.SymbolTreeCreateSymbol("/err", gsmID, "errorrate");

net = core.SymbolTreeGetValue("/net");
bat = core.SymbolTreeGetValue("/bat");
qua = core.SymbolTreeGetValue("/qua");
err = core.SymbolTreeGetValue("/err");

msg = "Report: Network:%i Battery:%i Quality:%i Errors:%i"%(net,bat,qua,err);
print msg;

core.SymbolTreeSetValue("/sms",msg);

