# -*- encoding: latin-1 -*-

import pyDCPU;
from SimpleExport import Object;

DCPUVERSION     = 0x000100;     #HEX version-number of pyDCPU-package this module was written for
VERSION         = 0x000001;     #HEX version-number of this package.

AUTHOR          = "Hannes Matuschek <hmatuschek[AT]gmx.net>";       
DATE            = "2005-03-07"; #Last update.


#a description in multible lang.
DESCRIPTION     = {'en': """This module is a simple XML-RPC (http) server.""",
                   'de': """Dieses Modul stellt einen eifachen XML-RPC (http) Server dar."""};

PARAMETERS      = {'Address':{'duty':False,
                              'help':{'en':'The address to bind to.',
                                      'de':'An auf diese Addresse hört der Server.'},
                              'default':'127.0.0.1'
                              },
                   'Port':{'duty':False,
                           'help':{'de':'',
                                   'en':''},
                           'default':'8080'}
                   };
