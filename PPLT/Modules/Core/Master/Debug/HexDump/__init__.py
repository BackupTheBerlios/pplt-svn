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
#   2005-03-07:
#       Add description (help text)



from hexdump import Object;

DCPUVERSION     = 0x000100;
VERSION         = 0x000100;
AUTHOR          = "Hannes Matuschek <hmatuschek[at]gmx.net>";
DATE            = "2005-03-07";

DESCRIPTION     = {'en': """This module dump all trafic as hex into the logging system.""",
                   'de': """Dieses Modul schreibt jeden Daten-Verkehr in das Logging-System."""};

PARAMETERS      = None;     # this module needs no parameters...

IS_ROOT_MODULE  = False;
CHILD_NEED_ADDR = False;
