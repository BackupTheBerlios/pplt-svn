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

import xml.dom.minidom;
import string;
import logging;
import Version;


class MetaData:
	def __init__(self, Document, Lang, AltLang):
		self.__Logger = logging.getLogger("PPLT");
		
		head = Document.getElementsByTagName("Head")[0];
		srvtag = Document.getElementsByTagName("PPLTServer")[0];

		self.__Version = Version.Version(str(srvtag.getAttribute("version")));
		self.__Name = str(srvtag.getAttribute("name"));
		self.__ClassString = str(srvtag.getAttribute("class"));

		self.__Description = {};
		self.__RequiredModules = [];
		self.__RequiredVariables = {};
		self.__Lang = Lang;
		self.__AltLang = AltLang;

		tmpNodeLst = getNodesByTagName(head.firstChild, "Description");
		for node in tmpNodeLst:
			self.__addModDescription(node);
		
		tmpNodeLst = getNodesByTagName(head.firstChild, "Require");
		for node in tmpNodeLst:
			self.__addRequire(node);
		#--- done ---

	def __addModDescription(self, xmlNode):
		langAttr = xmlNode.attributes.get("lang");
		if not langAttr:
			self.__Logger.warning("Module Description Node has no lang attr. (skipping)");
			return(False);
		lang = langAttr.value;
		text = getTextFromNode(xmlNode.firstChild);
		self.__Logger.debug("Add description for lang %s(%iB)"%(lang,len(text)));
		self.__Description.update( {lang:text} );
		return(True);

	def __addRequire(self, xmlNode):
		tmpNodeLst = getNodesByTagName(xmlNode.firstChild, "DCPUModule");
		for node in tmpNodeLst:
			self.__addRequiredModule(node);
		
		tmpNodeLst = getNodesByTagName(xmlNode.firstChild, "Variable");
		for node in tmpNodeLst:
			self.__addRequiredVariable(node);
		return(True);

	def __addRequiredModule(self, xmlNode):
		if not xmlNode.firstChild:
			self.__Logger.warning("Empty required module entry: skipping");
			return(False);
		if not xmlNode.firstChild.nodeType == xmlNode.TEXT_NODE:
			self.__Logger.warning("Invalid format: skipping");
			return(False);
		mod = getTextFromNode(xmlNode.firstChild);
		if len(mod)>0:
			self.__RequiredModules.append(mod);
		return(True);

	def __addRequiredVariable(self, xmlNode):
		try:
			var = Variable(xmlNode);
		except:
			self.__Logger.warning("Error while fetch variable.");
			return(False);
		self.__RequiredVariables.update( {var.GetName():var} );
		return(False);

	def GetName(self): return(self.__Name);
	def GetClass(self): return(self.__ClassString);
	def GetVersion(self): retunr(self.__Version);

	def GetDescription(self, lang=None, altlang=None):
		if not lang:
			lang = self.__Lang;
		if not altlang:
			altlang = self.__AltLang;

		txt = self.__Description.get(lang);
		if txt:
			return(txt);
		return(self.__Description.get(altlang));

	def GetRequiredModules(self):
		return(self.__RequiredModules);

	def GetRequiredVariableNames(self):
		return(self.__RequiredVariables.keys());

	def GetVariableDefaultValue(self, Name):
		var = self.__RequiredVariables.get(Name);
		if not var:
			self.__Logger.debug("Var %s not found"%Name);
			return(None);
		return(var.GetDefaultValue());

	def GetVariableDescription(self, Name, lang=None, altlang=None):
		if not lang:
			lang = self.__Lang;
		if not altlang:
			altlang = self.__AltLang;
		var = self.__RequiredVariables.get(Name);
		if not var:
			self.__Logger.debug("Var %s not found"%Name);
			return(None);
		return(var.GetDescription(lang,altlang));



class Variable:
	def __init__(self, xmlNode):
		self.__Logger = logging.getLogger("PPLT");
		self.__Description = {};
		self.__DefaultValue = None;		#undef

		attr = xmlNode.attributes.get("name");
		if not attr:
			self.__Logger.warning("No variable-name given!");
			raise Exception("no variable-name given!");
		self.__Name = attr.value;
		
		attr = xmlNode.attributes.get("default");
		if attr:
			self.__DefaultValue = attr.value;
		
		descList = getNodesByTagName(xmlNode.firstChild, "Description");
		for node in descList:
			self.__addDescription(node);


	def __addDescription(self, xmlNode):
		langAttr = xmlNode.attributes.get("lang");
		if not langAttr:
			self.__Logger.warning("Module Description Node has no lang attr. (skipping)");
			return(False);
		lang = langAttr.value;
		text = getTextFromNode(xmlNode.firstChild);
		self.__Description.update( {lang:text} );
		return(True);
		
		
	def GetName(self):
		return(self.__Name);

	def GetDescription(self, lang, altlang):
		txt = self.__Description.get(lang);
		if txt:
			return(txt);
		return(self.__Description.get(altlang));

	def GetDefaultValue(self):
		return(self.__DefaultValue);

	

	

#
# USEFULL FUNCTIONS:
#
def getNodesByTagName(xmlNode, Name):
	tmp = None;

	if not xmlNode:
		return([]);
	
	if xmlNode.nodeType == xmlNode.ELEMENT_NODE:
		if xmlNode.localName == Name:
			tmp = xmlNode;
	
	lst = getNodesByTagName(xmlNode.nextSibling, Name);
	if tmp:
		lst.insert(0,tmp);
	return(lst);

def getTextFromNode(xmlNode):
	if not xmlNode:
		return("");
	tmp = None;
	txt = getTextFromNode(xmlNode.nextSibling);
	if xmlNode.nodeType == xmlNode.TEXT_NODE:
		tmp = NormString(xmlNode.data)
	if not tmp:
		return(txt);
	return(tmp+txt);


def NormString(txt):
	nlst = [];
	tmpl = txt.split();
	for tmp in tmpl:
		if tmp != "":
			nlst.append(tmp);
	return(string.join(nlst));


