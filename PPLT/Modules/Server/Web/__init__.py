import pyDCPU;
from PPLTWeb import Object;

#CHANGELOG:
# 2005-05-27:
#	- fixed problem with blocking socket


DCPUVERSION = 0x000100;
VERSION     = 0x000002;


AUTHOR = "Hannes Matuschek"
DATE   = "2005-04-28";

DESCRIPTION =  {'en':'A simple WebServer that serves the symboltree.',
				'de':'Ein einfacher WebServer der den Symbolbaum exportiert.'};
PARAMETERS = {'Address':{'duty':False,
						'help':	{'en':'The address to bind to',
								'de':'Die Adresse, auf der der Server laufen soll.'},
						'default':'127.0.0.1'
						},
			'Port':{'duty':False,
					'help':{'en':'Port to bind to'},
					'default':'4711'}
			};

