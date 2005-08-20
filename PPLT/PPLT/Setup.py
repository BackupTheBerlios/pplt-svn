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

#CHANGELOG:
# 2005-08-20:
#	- fixed Setup() and DocWaker() to reakt on error while loading
#	  the core-modules
# 2005-07-26:
#	reimplement


import xml.dom.minidom;
import logging;



def Setup(CTX, FileName):
	doc = xml.dom.minidom.parse(FileName);
	try:
		DocWalker(doc.documentElement, CTX, None);
	except:
		CTX.Unload();
		return(False);
	return(True);


class Context:
	def __init__(self, Vars, CoreObj, DefaultUser=None, Root=None):
		self.__Core = CoreObj;

		self.__Vars = Vars;
		self.__DefaultUser = DefaultUser;
		self.__SrvRoot = Root;

		self.__SwitchFor = None;
		self.__IsServer = False;
		self.__CoreModules = CoreMods(None,self.__Core, False);
		self.__NameSpaceMap = {};
	
		self.__Logger = logging.getLogger("PPLT");



	def GetValue(self, Of):
		return(self.__Vars.get(Of));

	def SetSwitch(self, VarName):
		self.__SwitchFor = VarName;

	def GetSwitch(self):
		return(self.__Vars.get(self.__SwitchFor));

	def Load(self, Name, Paras, Parent = None, Addr=None, NameSpace=None):
		self.__Logger.info("Load %s"%str(Name));

		if self.__IsServer:
			# LOAD A SERVER
			ID = self.__Core.ExporterAdd(	Name,
											Paras,
											self.__DefaultUser,
											self.__SrvRoot);
			if not ID:
				self.__Logger.error("Error while load a core module: Abort");
				return(None);
			self.__CoreModules.AddChild( CoreMods(ID,self.__Core,True) );
		else:
			#LOAD A DEVICE:
			ID = self.__Core.MasterTreeAdd(	Parent,
											Name,
											Addr,
											Paras);
			if not ID:
				self.__Logger.error("Error while load a core module: Abort");
				return(None);
			if Parent:
				ParMod = self.__CoreModules.Find(Parent);
			else:
				ParMod = self.__CoreModules;
			ParMod.AddChild( CoreMods(ID, self.__Core, False) );
			self.__Logger.debug("Add Namespace %s for %s"%(NameSpace,Name));
			self.__NameSpaceMap.update( {NameSpace:ID} );
		return(ID);

	def Unload(self):
		return(self.__CoreModules.Destroy());

	def GetObjByNameSpace(self, NS):
		return(self.__NameSpaceMap.get(NS));

	def SetServer(self):
		self.__Logger.debug("This is a Server...");
		self.__IsServer = True;

	def SetDevice(self):
		self.__Logger.debug("This is a Device...");
		self.__IsServer = False;

	def IsServer(self):return(self.__IsServer);

	def IsDevice(self):return(not self.__IsServer);






class CoreMods:
	def __init__(self, ID, Core, IsServer):
		self.__ID = ID;
		self.__Core = Core;
		self.__Children = [];
		self.__IsServer = IsServer;

	def HasChildren(self):
		if len(self.__Children)>0:
			return(True);
		return(False);

	def AddChild(self, Child):
		self.__Children.append(Child);

	def Destroy(self):
		for child in self.__Children:
			if not child.Destroy():
				return(False);
			self.__Children.remove(child);
		if self.__ID:
			if self.__IsServer:
				return(self.__Core.ExporterDel(self.__ID));
			return(self.__Core.MasterTreeDel(self.__ID));
		return(True);

	def GetID(self):
		return(self.__ID);
				
	def Find(self, ID):
		if self.__ID == ID:
			return(self);

		for child in self.__Children:
			mod = child.Find(ID);
			if mod:
				return(mod);
		return(None);













def DocWalker(Node, CTX, ParentID=None):
	if not Node:
		return(None);

	if Node.nodeType == Node.ELEMENT_NODE:
		if Node.localName == "PPLTDevice":
			CTX.SetDevice();
			DocWalker(Node.firstChild, CTX);
		elif Node.localName == "PPLTServer":
			CTX.SetServer();
			DocWalker(Node.firstChild, CTX);

		elif Node.localName == "Setup":
			DocWalker(Node.firstChild, CTX);

		elif Node.localName == "Switch":
			variable = str(Node.getAttribute("variable"));
			CTX.SetSwitch(variable)
			SwitchWalker(Node.firstChild, CTX, ParentID);

		elif Node.localName == "Load":
			name  = str(Node.getAttribute("name"));
			(paras,addr) = ParameterWalker(Node.firstChild, CTX, {}, None);

			if Node.hasAttribute("namespace"):
				NS = str(Node.getAttribute("namespace"));
			else:
				NS = None;
			myID = CTX.Load(name, paras, Parent=ParentID, Addr=addr, NameSpace=NS); #if load success:
			if myID:
				DocWalker(Node.firstChild, CTX, myID);
			else:	#error while loading
				raise Exception("Error while load \"%s\""%name);

		elif Node.localName == "DebugInfo":
			print "DEBUG: %s"%str(TextWalker(Node.firstChild,None));

		elif Node.localName == "RaiseError":
			raise Exception(str(ErrorWalker(Node.firstChild,None)));

		else:
			#print "ignore element: %s"%Node.localName;
			pass;
	
	return(DocWalker(Node.nextSibling, CTX, ParentID));


def TextWalker(Node, CTX, txt=""):
	if not Node:
		return(txt);

	if Node.nodeType == Node.TEXT_NODE:
		txt += str(Node.data);

	elif Node.nodeType == Node.ELEMENT_NODE:
		if Node.localName == "Variable":
			txt += VarWalker(Node, CTX);
		else:
			print "ignore tag: %s"%Node.localName;

	return(TextWalker(Node.nextSibling, CTX, txt));


def ErrorWalker(Node, CTX, txt=""):
	return(TextWalker(Node, CTX, txt));


def VarWalker(Node, CTX):
	return( CTX.GetValue(str(Node.getAttribute("name"))) );


def SwitchWalker(Node,CTX, ParentID):
	if not Node:
		return(None);

	if Node.nodeType == Node.ELEMENT_NODE:
		if Node.localName == "Case":
			value = str(Node.getAttribute("value"));
			if value == CTX.GetSwitch():
				return(DocWalker(Node.firstChild, CTX, ParentID));
		elif Node.localName == "Default":
			DocWalker(Node.firstChild, CTX, ParentID);
		else:
			print "SWITCH: ignore tag \"%s\""%Node.localName;
	
	return(SwitchWalker(Node.nextSibling,CTX, ParentID));


def ParameterWalker(Node, CTX, paras={}, addr=None):
	if not Node:
		return( (paras,addr) );

	if Node.nodeType == Node.ELEMENT_NODE:
		if Node.localName == "Parameter":
			name = str(Node.getAttribute("name"));
			value = TextWalker(Node.firstChild,CTX);
			paras.update( {name:value} );
		elif Node.localName == "Address":
			addr = TextWalker(Node.firstChild,CTX);
			
	return(ParameterWalker(Node.nextSibling, CTX, paras, addr));










