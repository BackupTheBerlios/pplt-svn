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

# Revision:
#   2005-02-04:
#       + try/except 
#

#TODO:
#   + remove print / use self.__Logger...
#

import pyDCPU;
import CoreModuleInfo;
import xml.dom.minidom;
import traceback;
import zipimport;
import thread;
import string;
import sys;
import os.path;
import md5;
import Fingerprint;
import logging;


class Importer:
    def __init__(self, ModuleRootDir):
        self.__ModuleDataBase = ModuleDB(ModuleRootDir);
        self.__ModuleRootDir = ModuleRootDir;
        self.__Logger = logging.getLogger("pyDCPU");
    
    def NewMaster(self, Name, Connection, Parameters, Fingerprint):
        """ This Method create a object from the module [Name] with [Parameters] """
        
        # get meta data
        ModMeta = CoreModuleInfo.MetaData(os.path.normpath(self.__ModuleDataBase.ModDir(Name)));
        #check DCPUVersion;
        if not ModMeta.CheckDCPUVersion():
            raise Exceptions.ModuleRequirement("Bad pyDCPU version: get the actual version of PPLT from pplt.berlios.de")

        #check PythonVersion;
        if not ModMeta.CheckPythonVersion():
            raise Exceptions.ModuleRequirement("Bad python verion: update!");
        
        #check PythonModules;
        if not ModMeta.CheckPythonModules():
            raise Exceptions.ModuleRequirement("One or more python packages are missed!");

        #check Parameters;
        if not ModMeta.CheckParameters(Parameters.keys()):
            raise Exceptions.ModuleRequirement("Mad parameters: look at the module references!");

        #Automatic parameter extention.
        ModMeta.ExtendParameters(Parameters);

        #check if ROOT and Connection??? -> fail 
        if ModMeta.IsRootModule() and Connection:
            raise Exceptions.ModuleError("You can't connect a root-module to an other module!");
        
        Mod = self.__ModuleDataBase.GetModule(Name);
        if not Mod:
            raise Exceptions.ModuleError("Unable to load module \"%s\"!"%Name);

        Obj = Mod.Object(Fingerprint, Connection, Parameters, Name, self.__Logger);
        if not Obj.setup():
            raise Exceptions.ModuleSetup("Error while setup module \"%s\""%Name);
        return(Obj);


    def NewExporter(self, Name, Parameters, Fingerprint, SymbolTree):
        ModMeta = CoreModuleInfo.MetaData(os.path.normpath(self.__ModuleDataBase.ModDir(Name)));
        #check DCPUVersion;
        if not ModMeta.CheckDCPUVersion():
            raise Exceptions.ModuleRequirement("Bad pyDCPU version! Please update.");

        #check PythonVersion;
        if not ModMeta.CheckPythonVersion():
            raise Exceptions.ModuleRequirement("Bad python version: please update.");
        
        #check PythonModules;
        if not ModMeta.CheckPythonModules():
            raise Exceptions.ModuleRequirement("One or more python packages missed!");

        #check Parameters;
        if not ModMeta.CheckParameters(Parameters.keys()):
            raise Exceptions.ModuleRequirement("Mad parameters for module \"%s\": refer mod-reference!"%Name);

        #extend Parameters;
        ModMeta.ExtendParameters(Parameters);

        #check if not ROOT  
        if not ModMeta.IsRootModule():
            self.__Logger.warning("This module should be an root-module");
        
        Mod = self.__ModuleDataBase.GetModule(Name);
        if not Mod:
            raise Exceptions.ModuleError("Error while load module %s!"%Name);

        Obj = Mod.Object(Fingerprint, SymbolTree, Parameters, Name, self.__Logger);

        if not Obj.setup():
            raise Exceptions.ModuleSetup("Error while setup module %s"%Name);

        thread.start_new_thread(Obj.start,());
        return(Obj);


    def IsModule(self, Name):
        if self.__ModuleDataBase.GetModule(Name):
            return(True);
        return(False);

    def IsModuleRoot(self, Name):
        ModMeta = CoreModuleInfo.MetaData(os.path.normpath(self.__ModuleDataBase.ModDir(Name)));
        return(ModMeta.IsRootModule()); 

    def NeedChildAddress(self, Name):
        ModMeta = CoreModuleInfo.MetaData(os.path.normpath(self.__ModuleDataBase.ModDir(Name)));
        return(ModMeta.ChildNeedAddress());

    def GetParameterNames(self, Name):
        ModMeta = CoreModuleInfo.MetaData(os.path.normpath(self.__ModuleDataBase.ModDir(Name)));
        return(ModMeta.GetParameterNames());

    def IsParameterDuty(self, ModName, ParaName):
        ModMeta = CoreModuleInfo.MetaData(os.path.normpath(self.__ModuleDataBase.ModDir(ModName)));
        return(ModMeta.IsParameterDuty(ParaName));

    def GetParameterDefaultValue(self, ModName, ParaName):
        ModMeta = CoreModuleInfo.MetaData(os.path.normpath(self.__ModuleDataBase.ModDir(ModName)));
        return(ModMeta.GetParameterDefault(ParaName));



class ModuleDB:
    def __init__(self, RootDir):
        self.__Logger = logging.getLogger("pyDCPU");
        self.__RootDir = RootDir;
        self.__ModuleHash = {};
        
    def GetRootDir(self):
        return(self.__RootDir);

    def ModDir(self,ModName):
        tmp = ModName.split('.');
        tmp.insert(0,self.GetRootDir());
        return(string.join(tmp,"/")+".zip");
        
    def GetModule(self,Name):
        Path = self.ModDir(Name);

        tmp = Name.split(".");
        NName = string.join(tmp,'_');

        loader = zipimport.zipimporter(Path);

        sys.path.insert(0,Path);
        if not loader.find_module("__init__"):
            raise Exceptions.BadModule("Module %s has wrong format: not __init__.py found in %s"%(Name,Path))

        ModObj = loader.load_module("__init__");
        if not ModObj:
            raise Exceptions.ModuleError("Error while load __init__ from module %s"%Name);

        self.__ModuleHash.update( {Name:ModObj} );
        return(ModObj);
    



if __name__=="__main__":
    db = ModuleDB("/usr/PPLT/");
    mod = db.GetModule("Export.JVisu");
    print os.path.normpath(os.path.dirname(mod.__file__));
