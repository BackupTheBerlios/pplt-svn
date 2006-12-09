# ########################################################################## #
# Exceptions.py
#
# 2006-09-01
# Copyright 2006 Hannes Matuschek
# hmatuschek@gmx.net
# ########################################################################## #
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# ########################################################################## #



class PPLTError (Exception):
    def __init__(self, msg): Exception.__init__(self, msg);




class CorruptInterface (PPLTError):
    def __init__(self, msg): PPLTError.__init__(self, msg);


#class NotImplemented (CorruptInterface):
#    def __init__(self, msg): CorruptInterface.__init__(self, msg);




class ItemBusy (PPLTError):
    def __init__(self, msg): PPLTError.__init__(self, msg);


class ItemNotFound (PPLTError):
    def __init__(self, msg): PPLTError.__init__(self, msg);




#
# Follwoing exceptions are used inside the importer subsystem. The base 
# exception is ModuleImportError derived from PPLTError. All other import
# related exceptions inhert from this class.
#
class ModuleImportError( PPLTError ):
    """ This exception will be raise if a module can't be imported or seted 
        up. """
    pass        

class InvalidGrammarVersion( ModuleImportError ):
    """ This exception will be raised if a module description has the wrong 
        grammar version. """
    pass

class MissingDependency( ModuleImportError ):
    """ This exception will be raised by the CImporter to indicate that a 
        dependency of the module is not satisfied. """
    def __init__(self, msg=""):
        ModuleImportError.__init__(self, "Missing dependency: %s"%msg)
