#!/usr/bin/python
import PPLT;
import sys;

system = PPLT.System();

if not system.LoadDevice("Debug.RandomGenerator", "rand", {}):
	print "Error while load device \"random\".";
	sys.exit();

if not system.CreateFolder("/test"):
	print "Error while create folder";
	sys.exit();

if not system.CreateFolder("/test/test2"):
	print "Error while create folder (2)";
	sys.exit();

if not system.CreateSymbol("/test/test2/r_bool","rand::Generator::Bool","Bool"):
	print "Error while create symbol."
	sys.exit();

if not system.MoveFolder("/test/test2","/test/test"):
	print "Error whil move folder";
	sys.exit();

print "ls /: %s"%str(system.ListFolders("/"));
print "ls /test: %s"%str(system.ListFolders("/test"));
print "ls /test/test: %s"%str(system.ListSymbols("/test/test"))
