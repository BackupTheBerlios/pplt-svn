# ############################################################################ #
# This is part of the PPLT project. PPLT is a framework for industrial         # 
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

# Changelog:
# 2005-05-28:
#	- fixed missing exception catching try/except in SetupStepLoad.Load()
#	- fixed missing unloading all core-modules of a device if one core-mod
#		could not be loaded
# 2005-05-27:
#	Release as version 0.2.0

import string;
import xml.dom.minidom;
import logging;

class Setup:
	def __init__(self, XMLNodes):
		self.__Steps = FetchSteps(XMLNodes);
		self.__Logger = logging.getLogger('PPLT');
		if not self.__Steps:
			self.__Logger.error("Error while load setup description");
 
	def DoSetup(self, Core, VarHash):
		if not self.__Steps.Load(Core, None, VarHash):
			self.__Steps.Unload();
			return(False);
		return(True);
    
	def Unload(self):
		return(self.__Steps.Unload());

	def GetObjByNameSpace(self, NameSpace):
		return(self.__Steps.GetObjByNameSpace(NameSpace));
        
class SetupStep:
	def __init__(self):
		self.Logger = logging.getLogger('PPLT');
		self.Children = [];
	def AddChild(self, Child):
		self.Children.append(Child);
	def IsMyNameSpace(self, NameSpace):
		return(None);	#dummy
	def GetObjByNameSpace(self, NameSpace):
		objID = self.IsMyNameSpace(NameSpace);
		if objID:
			return(objID);
		for child in self.Children:
			objID = child.GetObjByNameSpace(NameSpace);
			if objID:
				return(objID);
		return(None);
                
class SetupStepLoad(SetupStep):
	def __init__(self, ModuleName, NameSpace):
		SetupStep.__init__(self);
		self.__ModuleName = ModuleName;
		self.__ModuleNameSpace = NameSpace;
		self.__Parameters = {};
		self.__Static = None;
		self.__Object = None;
		self.__Address = None;
		self.__NameSpace = NameSpace;

	def GetModName(self):
		return(self.__ModuleName);
	def IsMyNameSpace(self,NameSpace):
		if NameSpace == self.__NameSpace:
			return(self.__Object);
		return(None);
	def AddParameter(self, Name, Variable=None, Value=None):
		try:
			para = Parameter(Value, Variable);
		except:
			self.Logger.error("Error while create Parameter Object");
			return(False);
		self.__Parameters.update( {Name:para} );

	def SetAddress(self, Value = None, Variable=None):
		try:
			self.__Address  = Parameter(Value, Variable);
		except:
			self.Logger.error("Error while create Parameter Object");
			return(False);
            
	def Load(self, Core, ParentID, VarHash):
		self.__Core = Core;
		ret = {};
		paranames = self.__Parameters.keys();
		for name in paranames:
			para = self.__Parameters.get(name);
			if para.Static:
				ret[name] = para.Value;
			else:
				ret[name] = VarHash.get(para.VarName);

        
		if not self.__Address:
			addr = None;
		elif self.__Address.Static:
			addr = self.__Address.Value;
		else:
			addr = VarHash.get(self.__Address.VarName);
       
		self.Logger.debug("Try to load \"%s\" with %s at %s"%(self.__ModuleName,str(ret),str(addr)));
        
		#try:
		self.__Object = Core.MasterTreeAdd(ParentID, self.__ModuleName, addr, ret);
		#except:
		#	self.Logger.error("Exception while load %s"%self.__ModuleName);
	#		return(False);
		if not self.__Object:
			self.Logger.error("Error while load Module %s"%self.__ModuleName);
			return(False);
        
		for child in self.Children:
			if not child.Load(Core, self.__Object, VarHash):
				self.Logger.debug("One child couldnot be loaded...");
				return(False);
		return(True);
    
	def Unload(self):
		self.Logger.debug("Unlink all chidren");
		for child in self.Children:
			child.Unload();
		if self.__Object:
			self.Logger.debug("Unload my Object");
			self.__Core.MasterTreeDel(self.__Object);
		return(True);

class Parameter:
	def __init__(self, Value = None, Variable = None):
		self.__Logger = logging.getLogger('PPLT');
		self.Value = None;
		self.VarName = None;
		self.Static = None;
        
		if Value == None and Variable == None:
			self.__Logger.errro("Need Variablename or Value");
			raise Exception('Need Variable or Value');
		if Value:
			self.Static = True;
			self.Value = Value;
		else:
			self.Static = False;
			self.Value = None;
			self.VarName = Variable;

            
def FetchSteps(XMLNode):
    if not XMLNode:
        return(None);
    if XMLNode.nodeType == XMLNode.TEXT_NODE:
        return(FetchSteps(XMLNode.nextSibling));
    
    if XMLNode.localName == 'Load':
        attr = GetAttributesFrom(XMLNode);
        if not attr.has_key('name'):
            return(False);
        step = SetupStepLoad(attr.get('name'), attr.get('namespace'));
        if XMLNode.hasChildNodes():
            if not FetchStep(step, XMLNode.firstChild):
                print "Error while FetchStep()";
                return(None);
        return(step);
    return(None);
    
    
def FetchStep(ParentStep, XMLNode):
    logger = logging.getLogger('PPLT');
    if XMLNode == None:
        return(True);
    
    if XMLNode.localName == 'Parameter':
        name = GetAttributesFrom(XMLNode).get('name');
        cont = GetContentFrom(XMLNode.firstChild);
        if isinstance(cont, (unicode,str)): #content is a string
            logger.debug("Add static para %s = \"%s\""%(name,string.strip(cont)));
            ParentStep.AddParameter(name, Value=string.strip(cont));        #add static parameter to Parent
        else:
            attr = GetAttributesFrom(cont);
            varname = attr.get('name');
            logger.debug("Add dyn. para %s = ValueOf(%s)"%(name,string.strip(varname)));
            ParentStep.AddParameter(name, Variable=string.strip(varname));  #add dynamic parameter to Parent
    
    if XMLNode.localName == 'Address':
        cont = GetContentFrom(XMLNode.firstChild);
        if isinstance(cont, (unicode,str)): #content is a string
            ParentStep.SetAddress(Value=string.strip(cont));        #add static addr
        else:
            attr = GetAttributesFrom(cont);
            varname = attr.get('name');
            ParentStep.SetAddress(Variable=string.strip(varname));  #add dynamic addr
    
    if XMLNode.localName == 'Load':
        attr = GetAttributesFrom(XMLNode);
        step = SetupStepLoad(attr.get('name'), attr.get('namespace'));
        if not FetchStep(step, XMLNode.firstChild):
            return(False);
        ParentStep.AddChild(step);
    
    return(FetchStep(ParentStep, XMLNode.nextSibling));


def GetAttributesFrom(Node):
    if not isinstance(Node, xml.dom.minidom.Node):
        return(None);
    if not Node.hasAttributes():
        #print "Node has no attr.";
        return(None);

    Attr = {};

    for AttrName in Node.attributes.keys():
        Name = Node.attributes[AttrName].name;
        Value = Node.attributes[AttrName].value;
        Attr.update( {Name:Value} );
    return(Attr);

def GetContentFrom(Node, rc=''):
    if not Node:
        return(rc);
    if Node.nodeType == Node.TEXT_NODE:
        rc += Node.data;
    else:
        return(Node);
    return(GetContentFrom(Node.nextSibling,rc));    
