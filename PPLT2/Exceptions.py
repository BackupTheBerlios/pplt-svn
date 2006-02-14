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


class Error (Exception):
    """ This is the general base-exception for the PPLT2 project.
 all PPLT-code and modules will raised (should raise) this or a
 exception derived from this. """



class InternalError (Error):
    """ This is the base-exception for all internal errors.
 If this exception or one derived from this will indicated an serious
 internal error. Mostly an indicatior for mad code!"""



class ModuleError (Error):
    """ This is the base-exception for all module related errors."""



class ItemNotFound (Error):
    """ This exception will be raised if an item (symbol, module, ...) can't 
 be found."""



class ItemBusy (Error):
    """ This exception will be raised if an item (module) is busy. Also it 
    will be used for a time-out-error."""
