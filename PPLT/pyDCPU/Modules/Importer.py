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
import ModuleInfo;
import xml.dom.minidom;
import traceback;
#import ihooks;
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
       
        Mod = self.__ModuleDataBase.GetModule(Name);
        if not Mod:
            self.__Logger.error("Error while Load Module [%s]"%Name)
            return(None);
        if not ModuleInfo.CheckVersion(Mod,True):
            self.__Logger.error("Invalid dcpuVersion for mod %s"%Name);
            return(None);
        if not ModuleInfo.CheckParameters(Mod,Parameters):
            self.__Logger.error("Invalid Parameters for mod %s"%Name);
            return(None);
        if Mod.IS_ROOT_MODULE and Connection:
            self.__Logger.error("This module mus be loaded as a root module");
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
        
        if not Obj.setup():
            self.__Logger.error("Error while setup object");
            return(None);
        return(Obj);


    def NewExporter(self, Name, Parameters, Fingerprint, SymbolTree):
        Mod = self.__ModuleDataBase.GetModule(Name);
        if not Mod:
            self.__Logger.error("Error while Load Module [%s]"%Name)
            return(None);
        if not ModuleInfo.CheckVersion(Mod,True):
            self.__Logger.error("Invalid dcpuVersion for mod %s"%Name);
            return(None);
        if not ModuleInfo.CheckParameters(Mod,Parameters):
            self.__Logger.error("Invalid Parameters for mod %s"%Name);
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
    

    def GetModuleInfoXML(self, Name, Lang):
        return(self.__ModuleDataBase.GetModuleInfoXML(Name,Lang));
    def IsModule(self, Name):
        if self.__ModuleDataBase.GetModule(Name):
            return(True);
        
    def IsModuleRoot(self, Name):
        Module = self.__ModuleDataBase.GetModule(Name);
        try:
            return(Module.IS_ROOT_MODULE);
        except:
            self.__Logger.info("Module \"%s\" has no IS_ROOT_MODULE item."%Name);
            return(False);
        return(False);

    def NeedChildAddress(self, Name):
        Module = self.__ModuleDataBase.GetModule(Name);
        self.__Logger.debug("DIR(%s): %s"%(Name,dir(Module)));
        self.__Logger.debug("FILE(%s): %s"%(Name,Module.__file__));
        try:
            self.__Logger.debug("ChildNeedAddr: %s"%str(Module.CHILD_NEED_ADDR));
            return(Module.CHILD_NEED_ADDR);
        except:
            self.__Logger.info("Module \"%s\" has no CHILD_NEED_ADDR item."%Name);
            return(False);
        return(False);

    def GetParameterNames(self, Name):
        Module = self.__ModuleDataBase.GetModule(Name);
        if not Module:
            return(None);
        try:
            return(Module.PARAMETERS.keys());
        except:
            self.__Logger.debug("Module \"%s\" has no Parameters ?!?"%Name);
            return(None);
        return(None);

    def GetParameter(self, ModName, ParaName):
        Module = self.__ModuleDataBase.GetModule(ModName);
        if not Module:
            self.__Logger.warning("No Module named %s found"%ModName);
            return(None);
        if dir(Module).count('PARAMETERS') != 1:
            self.__Logger.warning("No PARAMETERS defined");
            return(None);
        if not Module.PARAMETERS:
            self.__Logger.warning("PARAMETERS of %s is None"%ModName);
            return(None);    
        if not Module.PARAMETERS.has_key(ParaName):
            self.__Logger.warning("No Parameter %s found in %s"%(ParaName,ModName));
            return(None);
        return(Module.PARAMETERS[ParaName]);

    def IsParameterDuty(self, ModName, ParaName):
        Para = self.GetParameter(ModName, ParaName);
        if not Para:
            return(False);
        if Para.has_key('duty'):
            return(Para['duty']);
        return(False);

    def GetParameterDefaultValue(self, ModName, ParaName):
        Para = self.GetParameter(ModName, ParaName);
        if not Para:
            return(None);
        if Para.has_key('default'):
            return(Para['default']);
        return(None);

    def GetParametersOptionList(self, ModName, ParaName):
        Para = self.GetParameter(ModName, ParaName);
        if not Para:
            return(None);
        if Para.has_key('options'):
            return(Para['options']);
        return(None);

    def IsParamerterOptionStrict(self, ModName, ParaName):
        Para = self.GetParameter(ModName, ParaName);
        if not Para:
            return(False);
        if Para.has_key('strict_options'):
            return(Para.get('strict_options'));
        return(False);
        

class ModuleDB:
    def __init__(self, RootDir):
        self.__Logger = logging.getLogger("pyDCPU");
        self.__RootDir = RootDir;
        self.__ModuleHash = {};
        
    def GetRootDir(self):
        return(self.__RootDir);

    def __ModDir(self,ModName):
        tmp = ModName.split('.');
        tmp.insert(0,self.GetRootDir());
        return(string.join(tmp,"/")+".zip");
        
    def GetModule(self,Name):
        #if self.__ModuleHash.has_key(Name):
        #    self.__Logger.debug("Module %s already loaded"%Name);
        #    return(self.__ModuleHash[Name]);
        
        Path = self.__ModDir(Name);

        tmp = Name.split(".");
        NName = string.join(tmp,'_');
        
        #Stuff = self.__ModuleLoader.find_module('__init__',[Path]);
        try:
            loader = zipimport.zipimporter(Path);
        except zipimport.ZipImportError:
            self.__Logger.error("Zip error while %s"%Path);
            return(None);
        
        sys.path.insert(0,Path);
        if not loader.find_module("__init__"):
            self.__Logger.error("Module has wrong format");
            return(None);
        
        ModObj = loader.load_module('__init__');
        if not ModObj:
            self.__Logger.error("Error while load module '__init__.py'");
            return(None);

        self.__ModuleHash.update( {Name:ModObj} );
        return(ModObj);
    

    def GetModuleInfoXML(self, Name, Lang):
        Mod = self.__ModuleHash.get(Name);
        if not Mod:
            self.__Logger.debug("Module %s not loadet, try to get"%Name);
            Mod = self.GetModule(Name);
        if not Mod:
            self.__Logger.error("Error while get module %s"%Name);
            return(None);
        return(ModuleInfo.GetModuleInfoXML(Mod,Name,Lang));




