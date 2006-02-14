# ########################################################################### #
# This is part of the PPLT project. PPLT is a framework for master-slave      #
# based communication.                                                        #
# Copyright (C) 2003-2006 Hannes Matuschek <hmatuschek@gmx.net>               #
#                                                                             #
# This library is free software; you can redistribute it and/or               #
# modify it under the terms of the GNU Lesser General Public                  #
# License as published by the Free Software Foundation; either                #
# version 2.1 of the License, or (at your option) any later version.          #
#                                                                             #
# This library is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU            #
# Lesser General Public License for more details.                             #
#                                                                             #
# You should have received a copy of the GNU Lesser General Public            #
# License along with this library; if not, write to the Free Software         #
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA   #
# ########################################################################### #

# Message-direction
MESSAGE_UP          = 1;
MESSAGE_DOWN        = 2;
MESSAGE_DIRECTIONS  = (MESSAGE_UP, MESSAGE_DOWN);

#Event priorities:
MESSAGE_PRI_HIGHEST = 10;
MESSAGE_PRI_HIGH    = 5;
MESSAGE_PRI_NORMAL  = 0;
MESSAGE_PRI_LOW     = -5;
MESSAGE_PRI_LOWEST  = -10;
MESSAGE_PRIORITIES  = (MESSAGE_PRI_HIGHEST, MESSAGE_PRI_HIGH,
                       MESSAGE_PRI_NORMAL, MESSAGE_PRI_LOW,
                       MESSAGE_PRI_LOWEST);
