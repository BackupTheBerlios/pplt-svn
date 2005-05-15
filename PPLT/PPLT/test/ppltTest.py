#!/usr/bin/python
import sys;
import PPLTSystem;


system = PPLTSystem.System();
system.LoadDevice("PLC.S7-200",
					"s7",
					{"Port":"1","PCAddr":"0","S7Addr":"2"});

system.LoadDevice("Mobile.GSMMobilePhone",
					"handy",
					{"Port":"0","Speed":"115200"});

system.CreateFolder("/simatic");
system.CreateSymbol("/simatic/SMB28","s7::Marker::SMB28","Byte");
system.CreateSymbol("/simatic/SM0.5","s7::Marker::SM0.5","Bool");

system.CreateFolder("/handy");
system.CreateSymbol("/handy/battery", "handy::GSM::battery","DWord");
system.CreateSymbol("/handy/signal", "handy::GSM::quality","DWord");
system.CreateSymbol("/handy/manufacturer" ,"handy::GSM::manufacturer", "String");
system.CreateSymbol("/handy/model","handy::GSM::model", "String");

system.LoadServer("Web.PPLTWebServer","web","admin",{"Address":"10.1.1.4","Port":"4711"});
system.LoadServer("Visu.JVisuServer","jvisu","admin",{"Address":"10.1.1.4","Port":"2200"});

while True:
	pass;
