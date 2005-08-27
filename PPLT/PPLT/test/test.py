#!/usr/bin/python
import PPLT;
import sys;

system = PPLT.System();

if not system.LoadDevice("Debug.RandomGenerator", "rand", {}):
	print "Error while load device \"random\".";
	sys.exit();

if not system.CreateSymbol("/r_bool","rand::Generator::Bool","Bool"):
	print "Error while create symbol."
	sys.exit();
if not system.LoadServer(	"Web.PPLTWebServer", "web", "admin",
							{"Address":"10.1.1.4", "Port":"8080"}):
	print "Error while load server.";
	sys.exit();

print "Start...";
while 1:
	pass;
							
