#!/usr/bin/python
import sys;
import PPLT;


system = PPLT.System();
system.LoadDevice("PLC.S7-200",
					"s7",
					{"Port":"0","PCAddr":"0","S7Addr":"2"});


system.CreateFolder("/simatic");
system.CreateSymbol("/simatic/SMB28","s7::Marker::SMB28","Byte");
system.CreateSymbol("/simatic/SM0.5","s7::Marker::SM0.5","Bool");


#system.LoadServer("Web.PPLTWebServer","web","admin",{"Address":"10.1.1.4","Port":"4711"});
system.LoadServer("Visu.JVisuServer","jvisu","admin",{"Address":"10.1.1.4","Port":"2200"});


system.SaveSession("test.xml");
