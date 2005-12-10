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
            self.__Logger.error("Bad pyDCPU Version: please get the actual PPLT and Modules Package from pplt.berlios.de");
            return(None);

        #check PythonVersion;
        if not ModMeta.CheckPythonVersion():
            self.__Logger.error("Bad Python version, please update");
            return(None);
        
        #check PythonModules;
        if not ModMeta.CheckPythonModules():
            self.__Logger.error("One or more python packages missed!");
            return(None);

        #check Parameters;
        if not ModMeta.CheckParameters(Parameters.keys()):
            self.__Logger.error("Parameter error");
            return(None);

        #extend Parameters;
        ModMeta.ExtendParameters(Parameters);

        #check if ROOT and Connection??? -> fail 
        if ModMeta.IsRootModule() and Connection:
            self.__Logger.error("This module is an root-module");
            return(None);
        
        Mod = self.__ModuleDataBase.GetModule(Name);
        if not Mod:
            self.__Logger.error("Error while Load Module [%s]"%Name)
            return(None);

        try:
            Obj = Mod.Object(Fingerprint, Connection, Parameters, Name, self.__Logger);
        except pyDCPU.SetupModError:
            self.__Logger.error("Error while init instance of %s"%Name);
            return(None);
        except:
            self.__Logger.error("Unknown error while init module %s"%Name);
            traceback.print_exc();
            return(None);

        try:
            if not Obj.setup():
                self.__Logger.error("Error while setup object");
                return(None);
        except Exception, e:
            self.__Logger.error("Exception while setup(): %s"%str(e));
            return None;
        return(Obj);


    def NewExporter(self, Name, Parameters, Fingerprint, SymbolTree):
        ModMeta = CoreModuleInfo.MetaData(os.path.normpath(self.__ModuleDataBase.ModDir(Name)));
        #check DCPUVersion;
        if not ModMeta.CheckDCPUVersion():
            self.__Logger.error("Bad pyDCPU Version: please get the actual PPLT and Modules Package from pplt.berlios.de");
            return(None);

        #check PythonVersion;
        if not ModMeta.CheckPythonVersion():
            self.__Logger.error("Bad Python version, please update");
            return(None);
        
        #check PythonModules;
        if not ModMeta.CheckPythonModules():
            self.__Logger.error("One or more python packages missed!");
            return(None);

        #check Parameters;
        if not ModMeta.CheckParameters(Parameters.keys()):
            self.__Logger.error("Parameter error");
            return(None);

        #extend Parameters;
        ModMeta.ExtendParameters(Parameters);

        #check if not ROOT  
        if not ModMeta.IsRootModule():
            self.__Logger.warning("This module should be an root-module");
        
        Mod = self.__ModuleDataBase.GetModule(Name);
        if not Mod:
            self.__Logger.error("Error while Load Module [%s]"%Name)
            return(None);

        try:
            Obj = Mod.Object(Fingerprint, SymbolTree, Parameters, Name, self.__Logger);
        except pyDCPU.SetupModError:
            self.__Logger.error("Error while init instance of %s"%Name);
            return(None);
        except:
            traceback.print_exc();
            self.__Logger.error("Unkown error while create instance of %s"%Name);
            return(None);

        if not Obj.setup():
            self.__Logger.error("Error while setup instance of %s"%Name);
            return(None);

        try:
            thread.start_new_thread(Obj.start,());
        except thread.error:
            self.__Logger.error("Error while create new thread for %s"%Name);
            return(None);
        except:
            self.__Logger.error("Error while start export module %s"%Name);
            return(None);
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

        try:
            loader = zipimport.zipimporter(Path);
        except zipimport.ZipImportError:
            self.__Logger.error("Zip error while %s"%Path);
            return(None);

        sys.path.insert(0,Path);
        if not loader.find_module("__init__"):
            self.__Logger.error("Module has wrong format");
            return(None);

        ModObj = loader.load_module("__init__");
        if not ModObj:
            self.__Logger.error("Error while load module '__init__.py'");
            return(None);

        self.__ModuleHash.update( {Name:ModObj} );
        return(ModObj);
    



if __name__=="__main__":
    db = ModuleDB("/usr/PPLT/");
    mod = db.GetModule("Export.JVisu");
    print os.path.normpath(os.path.dirname(mod.__file__));
