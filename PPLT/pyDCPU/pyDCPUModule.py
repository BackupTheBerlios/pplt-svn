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



import imp;
import sys;
import xml.sax;
import xml.sax.handler;
import textwrap;
import os.path;
import md5;
import random;

class pyDCPUXMLHandler(xml.sax.handler.ContentHandler):
    """ This is the Handler for the SAX parser..."""

    def __init__(self,Module):
        """Init: Set valid elements, set some initial values etc..."""
        self.dcpuValidElements = ['BridgeModule', 'DynBridgeModule',
                                  'MasterModule', 'ExportModule', 'Name', 'Path',
                                  'Version', 'Author', 'Icon', 'ChildNeedAddr',
                                  'Description','Parameter','Option'];
        self.dcpuIsValidElement = False;
        self.dcpuElementCont = "";
        if not Module:
            return(None);
        self.Module= Module;
        self.curPara = None;

    def startDocument(self):
        pass;
    def endDocument(self):
        pass;
	
    def startElement(self,Name,Attr):
        """ """
        try:
            self.dcpuValidElements.index(Name);
            self.dcpuIsValidElement = True;
			
            if Name == "MasterModule":
                self.Module.Type = "Master";
            if Name == "ExportModule":
                self.Module.TYpe = "Export";
                
            if Name == "Parameter":
                if Attr.has_key("name"):
                    self.curPara = dcpuParameter(Attr.get("name"));
                    if Attr.has_key("duty"):
                        if Attr.get("duty")=="true":
                            self.curPara.Duty = True;
                        if Attr.has_key("default"):
                            self.curPara.Default = Attr.get("default");
                    else:
                        self.curPara = None;
        except:
            self.dcpuIsValidElement = False;
	

    def endElement(self,Name):
        if Name=="Parameter":
            if self.curPara:
                self.Module.Parameters.append(self.curPara);
                self.curPara = None;
        if Name=="Option":
            if self.curPara:
                self.curPara.appendOption(self.dcpuElementCont);
        if Name=="Description":
            if self.curPara:					# it is a descr of a Parameter
                self.curPara.Description = textwrap.dedent(self.dcpuElementCont);
            else:
                self.Module.Description = textwrap.dedent(self.dcpuElementCont);
        if Name=="Name":
            self.Module.Name = textwrap.dedent(self.dcpuElementCont);
        if Name=="Path":
            self.Module.Path = textwrap.dedent(self.dcpuElementCont);
        if Name=="Version":
            self.Module.Version = textwrap.dedent(self.dcpuElementCont);
        if Name=="Author":
            self.Module.Author = textwrap.dedent(self.dcpuElementCont);
        if Name=="Icon":
            # FIXME: save icon file path...
            self.Module.Icon = None;

        if Name=="ChildNeedAddr":
            if self.dcpuElementCont == "true":
                self.Module.ChildNeedAddr = True;
            else:
                self.Module.ChildNeedAddr = False;

        self.dcpuIsValidElement = False;
        self.dcpuElementCont = "";
		
    def characters(self,Content):
        #FIXME: make is better with regepx...
        if Content != "\n":
            self.dcpuElementCont += Content;

class dcpuParameter:
    def __init__(self,Name):
        if not Name:
            print "Error; no Parameter Name...";
        self.Name = Name;
        self.Options = [];
        self.Description = "";
        self.Duty = False;
        self.Default = None;
    def appendOption(self,Option):
        if Option:
            self.Options.append(Option);

			

# ************************************************* #
# Module Class                                      #
# **************************************************#
class pyDCPUModule:
    """
        Main Module Class. This Class holds all information
        about the Modul, and also provides some methods to
        create new pyDCPUObjects from loaded Modules...
        IMPORTANT:
            To provide a fast app. start; i only load the module
            description. If you create a new Object from this
            module, i will load the real python module...
    """
    
    def __init__(self, XMLFile, DirList, IDList, Logger):
        """
            INIT: I will parse the given XMLFile and save all
            information into this ClassInstance...
        """
        if XMLFile == None:
            print "Error; No filename...";
            return(None);
        if -1 == XMLFile.find(".xml"):
            print XMLFile," is not an XML File";
            return(None);
	    
        self.Name = None;               #Name of Module
        self.Path = None;               #The File of Module
        self.Version = None;            #Versionnumber
        self.Author = None;             #Author Name and MailAddr
        self.IconFile = None;           #Icon
        self.ChildNeedAddr = False;     #If a instance of this mod will need a
                                        # addr for a connection.
        self.Description = None;        #A short description (text)
                                        # FIXME: multi lang!!!
        self.Parameters = [];           #List Of Parameters...
		
        self.Module = None;	        #Binary of Module, will be loaded later...
		
        self.Type = None;               #Important: The Type
                                        # (Master/Export-Module) 
		
        self.Logger = Logger;           #The Logging object.
        self.ModDirList = DirList;
        self.ObjectIDList = IDList;     #List of ID (for reating unique IDs)


	#
	# Parse Description File...
	#
        handler = pyDCPUXMLHandler(self);
        sax = xml.sax.parse(XMLFile,handler);	
		

    def appendParameter(self,Parameter):
        if Parameter is dcpuParameter:
            self.Parameters.append(Parameter);
	

    def valid(self):
        # FIXME: nonsense...
        return(False);
	

    def new(self, Parameter=None):
        """ With this method i will create a new object from this class.
        """
        #self.Logger.debug('Try to get Modul');
        Module = dcpuImport(self.Name,self.ModDirList,self.Path);

        if Module:
            #self.Logger.debug('Ok, modul exists...');
            NewObj = Module.Object(Parameter,self.Logger,self.Name);
		
            if NewObj:
                self.Logger.debug('Ok, new obj created');
                NewObj.ID = dcpuCreateNewID(self.ObjectIDList);
                NewObj.Class = self.Name;
                
                if not NewObj.setup():
                    self.Logger.warning("Error while Setup...");
                    NewObj.destroy();
                    return(None);
                return(NewObj);

            else:
                self.Logger.warning('Opps, Error while create Obj (invalid Parameter???)');
                return(None);
        else:
            self.Logger.error("Can't load Modul");
            return(None);



def dcpuImport(Name, PathList, SubPath):
    if sys.modules.has_key(Name):
        return sys.modules[Name];

    myPathList = [];
    for Path in PathList:
        myPathList.append("%s/%s"%(Path,SubPath));

    fp, pathname, description = imp.find_module(Name, myPathList);
    sys.path.append(os.path.dirname(os.path.abspath(pathname)));
    
    try:
        return (imp.load_module(Name, fp, pathname, description));
    finally:
	# Since we may exit via an exception, close fp explicitly.
        if fp:
            fp.close()

def dcpuCreateNewID(ObjectIDList):
    """ This function creates a unique ObjectID..."""
    tmpID = md5.new("%i"%(random.randint(1,1000000000))).hexdigest();

    while(ObjectIDList.count(tmpID)):
        tmpID = md5.new("%i"%(randint(1,1000000000))).hexdigest();
    return(tmpID);
