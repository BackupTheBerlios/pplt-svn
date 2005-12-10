# ############################################################################ #
# This is part of the pyDCPU project. pyDCPU is a framework for industrial     # 
#   communication.                                                             # 
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


class ExportObject:
    """
        This is the class for all ExportModules:
            - define all function you have to provide to
                the pyDCPU System
        * don't overwrite the __init__() method!!!
        * the system will call the Setup() method first:
            there you can make some initialitaion
        * then it will call the Start() method in a new
            thread.
        * if the Modul will be unloaded, the system will
            call the Stop() method.        
    """
    def __init__(self, ID, SymbolTree, Parameters, Class, Logger):
        """
            DON'T OVERWRITE IT!!!
        """
        self.Parameters   = Parameters.copy();
        self.Logger       = Logger;
        self.SymbolTree   = SymbolTree;
        self.ID           = ID;
        self.Class        = Class;



    def setup(self):
        return(True);
    
    def start(self):
        return(False);

    def stop(self):
        return(True);
    


    def _GetID(self):
        return(self.ID);

    def _GetClass(self):
        return(self.Class);
    
    def _ToXMLNode(self, Document):
        pass;
