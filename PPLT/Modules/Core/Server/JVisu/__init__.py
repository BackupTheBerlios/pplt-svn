import pyDCPU;
from JVisu import Object;

#Changelog:
# 2005-05-27:
#	- fixed problem with blocking socket

DCPUVERSION     = 0x000100;     #HEX version-number of pyDCPU-package this module was written for
VERSION         = 0x000101;     #HEX version-number of this package.

AUTHOR          = "Hannes Matuschek <hmatuschek[AT]gmx.net>";       
DATE            = "2005-03-07";                                     #Last update.


#a description in multible lang.
DESCRIPTION     = {'en': """This module is a JVisu-Server""",
                   'de': """Dieses Modul is ein JVisu-Server"""};

PARAMETERS      = {'Address':{'duty':True,
                              'help':{'en':'The IP address to bind to.',
                                      'de':'Die IP Adresse an die der Server gebunden werden soll.'},
                              'default':'127.0.0.1'
                              },
                   'Port':{'duty':False,
                           'help':{'de':'The port to listen to.',
                                   'en':'Der Port des Servers.'},
                           'default':'2200'}
                   };
