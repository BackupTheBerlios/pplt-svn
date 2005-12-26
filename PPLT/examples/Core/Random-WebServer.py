#!/usr/bin/python
import pyDCPU;

# start the core:
core = pyDCPU.Core("/usr/PPLT");

# load "ramdom" module:
MID = core.MasterTreeAdd(None, "Master.Debug.Random", None, None);

# create some symbols:
core.SymbolTreeCreateFolder("/test");
core.SymbolTreeCreateSymbol("/test/bool",  MID, Address="Bool");
core.SymbolTreeCreateSymbol("/test/int",   MID, Address="Integer");
core.SymbolTreeCreateSymbol("/test/float", MID, Address="Float");

#load webserver module:
EID = core.ExporterAdd("Export.PPLTWeb", {"Address":"127.0.0.1", "Port":"8080"}, "nobody");

#endless loop:
while True: pass;

