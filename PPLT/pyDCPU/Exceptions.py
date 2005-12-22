# ############################################################################ #
# This is part of the pyDCPU project. pyDCPU is a framework for industrial     # 
# communication.                                                               # 
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



#
# This file contains the exception-classes for all the
#   exceptions, may raised while using/running the pyDCPU
#   System.
#

class Error(Exception):
    """ Base exception-class for all execptions raised by pyDCPU
            system and modules """
    pass;

# General exceptions:
class ItemNotFound(Error): pass;            # if a objectid, foder, symbol, module doesn't exists
class ItemBusy(Error): pass;                # if a module is busy (locked) or a object is still used 

# Exceptions related to Modules:
class ModuleError(Error): pass;             # general module error class
class ModuleSetup(ModuleError): pass;       # if a module can't be setted up.
class BadModule(ModuleError): pass;         # if a module mismatch the API or meta.xml is bad
class ModuleRequirement(ModuleError): pass; # if a requirement of a module is missing.

#Exceptions related to the symboltree
class SymbolError(Error): pass;             # general symboltree error class
class AccessDenied(SymbolError): pass;      # if you don't have the permission to access a symbol/folder



#
# Old class exceptions:
#
class ModError(Error):
    """ Base class for all exceptions raised in a module. """
    pass;



class SetupModError(ModError):
    pass;



class LockModError(ModError):
    """ This execption will be raised, if the module you manted
            to access was locked: [retry] """
    pass;


class IOModError(ModError):
    """ This exception should be raised, if there was an IOError:
        This means:
            - error while access to a data-source
            - protocol-errors [retry]"""
    pass;



class FatIOModError(ModError):
    """ This execption should be raise, if the communication is
            broken down: [stop]"""
    pass;



class TimeOutError(ModError):
    pass;
    

class ReadOnlyModError(ModError):
    """ This exception should be raised, if the module is readonly"""
    pass;
