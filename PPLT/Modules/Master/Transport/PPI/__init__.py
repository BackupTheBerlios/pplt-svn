# -*- encoding: utf8 -*-
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



from ModPPI import Object;

DCPUVERSION     = 0x000100;
VERSION         = 0x00001C;

AUTHOR          = "Hannes Matuschek <hmatuschek[at]gmx.net>";
DATE            = "2005-02-05";

DESCRIPTION     = {'en': """ A master module to access direct a PPI-BUS """,
                   'de': """ Ein MasterModul mit dem sie direkt auf einer
                               PPIBUS zu greifen können"""};

PARAMETERS      = {'Address':{'duty':True,
                              'default':'0',
                              'help':{'en':'This is the addr of the pc in ppibus.',
                                      'de':'Die adresse des PCs innerhalb des PPI-Buses'}
                              }
                   };

IS_ROOT_MODULE  = False;
CHILD_NEED_ADDR = True;
