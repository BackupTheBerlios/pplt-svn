# -*- encoding: latin-1 -*-
# ############################################################################ # 
# This is part of the PPLT project.                                            # 
#                                                                              # 
# Copyright (C) 2003-2005 Hannes Matuschek <hmatuschek@gmx.net>                # 
#                                                                              # 
# This library is free software; you can redistribute it and/or                # 
# modify it under the terms of the GNU Lesser General Public                   # 
# License as published by the Free Software Foundation; either                 # 
# version 2.1 of the License, or (at your option) any later version.           # 
#                                                                              # 
# This library is distributed in the hope that it will be useful,              # 
# but WITHOUT ANY WARRANTY; without even the implied warranty of               # 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU             # 
# Lesser General Public License for more details.                              # 
#                                                                              # 
# You should have received a copy of the GNU Lesser General Public             # 
# License along with this library; if not, write to the Free Software          # 
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA    # 
# ############################################################################ # 

#TODO:
#   + make it real platformindipendent!!!
#

#REVISION:
#   2005-02-04:
#       + complete description
#

from UniSerial import Object;


# ***
# It follows a complete description of this pyDCPU module.
# (for more information see at the documentation)
#

DCPUVERSION     = 0x000100;     #HEX version-number of pyDCPU-package this module was written for
VERSION         = 0x00001C;     #HEX version-number of this package.

AUTHOR          = "Hannes Matuschek <hmatuschek[AT]gmx.net>";       
DATE            = "2005-02-04";                                     #Last update.


#a description in multible lang.
DESCRIPTION     = {'en': """ This Module implements a systemindipendent Serial interface.""",
                   'de': """ Dieses Modul stellt eine systemunabhängige serielle Schnittstelle zur Verfügung"""};

#THE PARAMETERS YOU NEED TO RUN UNISERIAL
PARAMETERS      = {'Port':{'duty':True,
                           'default':'0',
                           'help':{'en':'Insert here the Portnumber.',
                                   'de':'Geben sie hier den Port an.'}
                           },
                   'Speed':{'duty':True,
                            'default':'9600',
                            'options':['50','75','110','134','150','200','300',
                                       '600','1200','1800','2400','4800','9600',
                                       '14400','19200','38400','57600','115200'],
                            'strict_options':False,
                            'help':{'en':'The speed in BAUD.',
                                    'de':'Die Geschwindigkeit in BAUD.'}
                            },
                   'Parity':{'duty':False,
                             'default':'None',
                             'options':['None','Even','Odd'],
                             'strict_options':True,
                             'help:':{'en':'Parity check.',
                                      'de':'Paritätsprüfung.'}
                             },
                   'TimeOut':{'duty':False,
                              'default':None,
                              'help':{'en':'Timeout in s.',
                                      'de':'Timeout in s.'}
                              }
                    }


IS_ROOT_MODULE  = True;
CHILD_NEED_ADDR = False;
