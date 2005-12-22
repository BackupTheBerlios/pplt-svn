#!/usr/bin/python
import PPLT;
import sys;
import time;

system = PPLT.System();

if not system.LoadDevice("PLC.S7-200", "S7", {"Port":"1","S7Addr":"2","PCAddr":"0"}): raise Exception("unable to load S7");
if not system.CreateSymbol("/test", "S7::Marker::AB0", "uInteger"): raise Exception("unable to create symbol")
if not system.LoadServer("Visu.JVisuServer", "JV", "admin", {"Address":"127.0.0.1", "Port":"2201"}): raise Exception("Unable to load server");

while 1:
    time.sleep(100.0);
