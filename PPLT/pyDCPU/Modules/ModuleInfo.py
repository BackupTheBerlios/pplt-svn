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


import pyDCPU;
import logging;
import xml.dom.minidom;


def CheckVersion(Module, Force=False):
    """
        This function checks if the pyDCPU version fits to the Version
        a spec. module needs.
    """
    Logger = logging.getLogger("pyDCPU");
    
    try:
        modVersion = Module.DCPUVERSION;
    except:
        Logger.error("No VERSION in module");
        return(False);

    dcpuVersion = pyDCPU.VERSION;

    if (dcpuVersion & 0xff0000) != (modVersion & 0xff0000):
        Logger.error("Major versionnumber is different! Unable to load module");
        Logger.info("Need %i but dcpuversion is %i"%(modVersion,dcpuVersion));
        return(False);

    if (dcpuVersion&0x00ffff) < (modVersion&0x00ffff):
        if Force:
            Logger.warning("Minor version of dcpu is less then required by mod!!!");
            return(True);
        else:
            Logger.error("Minor number of dcpu is less then require by Module: Can't load (use Force)");
            return(False);

    Logger.debug("Mod: %x -> Sys %x FIT"%(modVersion,dcpuVersion));
    return(True);


def CheckParameters(Module, Parameters):
    """
        This method check at first if all needed (duty) parameters
        are in the given Parameters-hash. Then it will test, if
        there are some strict-options, that the value is in the
        option list.
    """
    Logger = logging.getLogger("pyDCPU");
    try:
        modParameters = Module.PARAMETERS;
    except:
        Logger.warning("Module have no parameters???");
        return(True);

    if not isinstance(modParameters,dict):
        Logger.debug("Module need no parameters");
        return(True);

    for ParaName in modParameters.keys():
        modPara = modParameters.get(ParaName);

        # check if there are all duty parameters 
        if modPara.has_key('duty'):
            if modPara['duty']:
                if not Parameters.has_key(ParaName):
                    Logger.error("Parameter \"%s\" is needed!"%ParaName);
                    return(False);
                else:
                    Logger.debug("Ok, duty Parameter \"%s\" is present"%ParaName);
            else:
                #is not duty
                pass;
        else:
            Logger.debug("Parameter \"%s\" has no \"duty\" attr."%ParaName);
            pass;

        # check for strict Options
        if modPara.has_key('options'):
            optList = modPara['options'];
            if modPara.has_key('strict_options'):
                if modPara['strict_options']:
                    if Parameters.has_key('ParaName'):
                        Value = Parameters[ParaName];
                        if 0 == optList.count(Value):
                            Logger.error("Value \"%s\" not in OptionList for parameter \"%s\""%(Value,ParaName));
                            Logger.info("Must be one of: %s"%str(optList));
                            return(False);
                        else: #all ok:
                            pass;
                    else: #strict parameter is not duty
                        pass;
                else: #is not strict
                    pass;
            else: #has no strict attr.->not strict
                Logger.debug("No 'strict_options' attr. for parameter \"%s\""%(ParaName));
                pass;
        else: #has no options->choose free
            pass;
    #END FORALL
    Logger.debug("Parameters are OK");
    return(True);
     

                             
def GetAuthor(Module):
    try:
        return(Module.AUTHOR);
    except:
        return('None');

def GetDate(Module):
    try:
        return(str(Module.DATE));
    except:
        return("None");

def ChildNeedAddress(Module):
    logger = logging.getLogger('pyDCPU');
    try:
        if Module.CHILD_NEED_ADDRESS:
            return("True");
    except:
        logger.warning("Module has no CHILD_NEED_ADDR");
        return("False");
    return("False");

def IsRoot(Module):
    try:
        if Module.IS_ROOT_MODULE:
            return("True");
    except:
        return("False");
    return("False");


def GetVersionString(Module):
    try:
        Version = Module.VERSION;
    except:
        return("");
    patch = Version&0xff;
    minor = (Version>>8)&0xff;
    major = (Version>>16)&0xff;
    return("%i.%i.%i"%(major,minor,patch));

        
def GetDescription(Module, Lang, DefaultLang = 'en'):
    Logger = logging.getLogger('pyDCPU');

    try:
        desc = Module.DESCRIPTION;
    except:
        Logger.debug("No description for this module");
        return('none');

    if not isinstance(desc, dict):
        Logger.warning("Invalid description for this module");
        return('none');
    if len(desc) <1:
        Logger.debug("Empty description");
        return('none');
    
    if desc.has_key(Lang):
        return(desc[Lang]);
    Logger.debug("Can't find desc. for lang \"%s\" try to get \"%s\""%(Lang,DefaultLang));
    if desc.has_key(DefaultLang):
        return(desc[DefaultLang]);
    Logger.debug("Can't find desc. for default lang. take the first.");
    return(desc[desc.keys()[0]]);

def GetParameterList(Module):
    try:
        para = Module.PARAMETERS;
    except:
        return([]);
    if not isinstance(para,dict):
        return([]);
    return(para.keys());

def GetParameterHelp(Module,ParaName,Lang):
    try:
        para = Module.PARAMETERS;
    except:
        return('None');
    if not isinstance(para,dict):
        return('None');
    if not para.has_key(ParaName):
        return('None');
    Parameter = para.get(ParaName);
    if not Parameter.has_key('help'):
        return('None');
    Help = Parameter.get('help');
    if not isinstance(Help,dict):
        return('None');
    
    if Help.has_key(Lang):  #try to get Lang:
        return(Help.get(Lang));
    if Help.has_key('en'):  #try to get Lang:en
        return(Help.get('en'));
    if len(Help.keys())>0:  #get first found
        return(Help.get(Help.keys()[0]));
    return('None');


def GetParameterDuty(Module, ParaName):
    try:
        para = Module.PARAMETERS;
    except:
        return('False');
    if not isinstance(para,dict):
        return('False');
    if not isinstance(para.get(ParaName),dict):
        return('False');
    Parameter = para.get(ParaName);
    if not Parameter.has_key('duty'):
        return('False');
    if Parameter.get('duty'):
        return('True');
    return('False');

def GetDefaultValue(Module, ParaName):
    try:
        para = Module.PARAMETERS;
    except:
        return(None);
    if not isinstance(para,dict):
        return(None);
    if not isinstance(para.get(ParaName),dict):
        return(None);
    Parameter = para.get(ParaName);
    if not Parameter.has_key('default'):
        return(None);
    return(Parameter.get('default'));

def IsStrictOption(Module,ParaName):
    try:
        para = Module.PARAMETERS;
    except:
        return('False');
    if not isinstance(para,dict):
        return('False');
    if not isinstance(para.get(ParaName),dict):
        return('False');
    Parameter = para.get(ParaName);
    if not Parameter.has_key('strict_options'):
        return('False');
    if Parameter.get('strict_options'):
        return('True');
    return('False');


def GetOptionList(Module,ParaName):
    try:
        para = Module.PARAMETERS;
    except:
        return([]);
    if not isinstance(para,dict):
        return([]);
    if not isinstance(para.get(ParaName),dict):
        return([]);
    Parameter = para.get(ParaName);
    if not isinstance(Parameter.get('options'),list):
        return([]);
    return(Parameter.get('options'));    
    
def GetModuleInfoXML(Module,Name,Lang):
    """
        This function gets the module anr return the
        module_info as XML
    """
    dom = xml.dom.minidom.getDOMImplementation();
    doc = dom.createDocument(None, "ModuleInfo", None);
    docnode = doc.documentElement;

    docnode.setAttribute('modname',Name);

    vernode = doc.createElement("Version");
    docnode.appendChild(vernode);
    ver     = doc.createTextNode(GetVersionString(Module));
    vernode.appendChild(ver);

    authnode = doc.createElement("Author");
    docnode.appendChild(authnode);
    author = doc.createTextNode(GetAuthor(Module));
    authnode.appendChild(author);

    datenode = doc.createElement("Date");
    docnode.appendChild(datenode);
    date = doc.createTextNode(GetDate(Module));
    datenode.appendChild(date);

    rootnode = doc.createElement("IsRootModule");
    docnode.appendChild(rootnode);
    root = doc.createTextNode(IsRoot(Module));
    rootnode.appendChild(root);

    cnanode = doc.createElement("ChildNeedAddress");
    docnode.appendChild(cnanode);
    cna = doc.createTextNode(ChildNeedAddress(Module));
    cnanode.appendChild(cna);

    descnode = doc.createElement("Description");
    docnode.appendChild(descnode);
    desctext = GetDescription(Module,Lang);
    desc = doc.createTextNode(desctext);
    descnode.appendChild(desc);

    ParaList = GetParameterList(Module);
    for Para in ParaList:
        paranode = doc.createElement('Parameter');
        paranode.setAttribute('name',Para)
        paranode.setAttribute('duty',GetParameterDuty(Module,Para));
        paranode.setAttribute('strict',IsStrictOption(Module,Para));
        docnode.appendChild(paranode);

        helpnode = doc.createElement('Help');
        paranode.appendChild(helpnode);
        help = doc.createTextNode(GetParameterHelp(Module,Para,Lang));
        helpnode.appendChild(help);

        DefaultValue = GetDefaultValue(Module,Para);
        if DefaultValue:
            defaultnode = doc.createElement('Default');
            paranode.appendChild(defaultnode);
            default = doc.createTextNode(DefaultValue);
            defaultnode.appendChild(default);

        Options = GetOptionList(Module,Para);
        for Opt in Options:
            optnode = doc.createElement('Option');
            paranode.appendChild(optnode);
            opt = doc.createTextNode(str(Opt));
            optnode.appendChild(opt);
            
    return(doc.toprettyxml(indent='  '));
    
