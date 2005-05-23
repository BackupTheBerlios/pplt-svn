#!/usr/bin/python
import PPLT;
import sys;

""" This script process a install description file. Meaning: installing a set of pyDCPUModules. """

# check options
if len(sys.argv)!=2:
    print "USEAGE: python PPLTModInstall.py InstFile.xml";
    sys.exit();
 
# get config of PPLTSystem
Config = PPLT.Config();

# get filename from commandline options
filename = sys.argv[1];

print "Process \"%s\""%filename;

# process install desc. file
PPLT.InstallSet(filename,Config.GetBasePath());

# thats all...
