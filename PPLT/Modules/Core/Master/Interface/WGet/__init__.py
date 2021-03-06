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

#REVISION:
# 2005-02-16:
#   initial
# 2005-03-07:
#   Add complete description.


from wget import Object;


# ***
# It follows a complete description of this pyDCPU module.
# (for more information see at the documentation)
#

DCPUVERSION     = 0x000100;     #HEX version-number of pyDCPU-package this module was written for
VERSION         = 0x000100;     #HEX version-number of this package.

AUTHOR          = "Hannes Matuschek <hmatuschek[AT]gmx.net>";       
DATE            = "2005-03-07";                                     #Last update.


#a description in multible lang.
DESCRIPTION     = {'en': """Fetch a web site or parts ot them.""",
                   'de': """Holt die Gesammte oder einen Teil eier WEB-Seite"""};

PARAMETERS      = {'port':{'duty':False,
                           'default':'80',
                           'help':{'en':'Port of server.',
                                   'de':'Port des Servers.'}
                           },
                   'host':{'duty':True,
                            'default':'www.23inch.de',
                            'help':{'en':'Address of server.',
                                    'de':'Die Adresse der Servers.'}
                           }
                   }


IS_ROOT_MODULE  = True;
CHILD_NEED_ADDR = True;
