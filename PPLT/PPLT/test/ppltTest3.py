#!/usr/bin/python
import PPLT;

psys = PPLT.System();

info = psys.GetServerInfo("RPC.SimpleExport");
print info.GetDescription()


print info.GetRequiredVariableNames();
print info.GetVariableDefaultValue("Port")
