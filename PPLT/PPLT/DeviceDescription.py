import xml.dom.minidom;
import string;
import logging;
import Setup;

def LoadSetup(FileName):
    doc = xml.dom.minidom.parse(FileName);
    setupnodes = doc.getElementsByTagName('Setup');
    return(Setup.Setup(setupnodes[0].firstChild));


def LoadDescription(FileName,Lang,AltLang):
	doc = xml.dom.minidom.parse(FileName);
	descNodes = doc.getElementsByTagName("Head");
	return(Description(descNodes[0],Lang,AltLang));

class Description:
	def __init__(self, xmlNode, Lang, AltLang):
		self.__Logger = logging.getLogger("PPLT");
		self.__Description = {};
		self.__RequiredModules = [];
		self.__RequiredVariables = {};
		self.__NameSpaces = {};
		self.__Lang = Lang;
		self.__AltLang = AltLang;

		tmpNodeLst = getNodesByTagName(xmlNode.firstChild, "Description");
		for node in tmpNodeLst:
			self.__addModDescription(node);
		
		tmpNodeLst = getNodesByTagName(xmlNode.firstChild, "Require");
		for node in tmpNodeLst:
			self.__addRequire(node);
		
		tmpNodeLst = getNodesByTagName(xmlNode.firstChild, "Provide");
		for node in tmpNodeLst:
			self.__addProvide(node)


	def __addModDescription(self, xmlNode):
		langAttr = xmlNode.attributes.get("lang");
		if not langAttr:
			self.__Logger.warning("Module Description Node has no lang attr. (skipping)");
			return(False);
		lang = langAttr.value;
		text = getTextFromNode(xmlNode.firstChild);
		self.__Logger.debug("Add mod-descr for lang %s with %i bytes"%(lang,len(text)));
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

	def __addProvide(self, xmlNode):
		tmpNodeLst = getNodesByTagName(xmlNode.firstChild, "NameSpace");
		for node in tmpNodeLst:
			self.__addNameSpace(node);
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

	def __addNameSpace(self, xmlNode):
		try:
			ns = NameSpace(xmlNode);
		except:
			self.__Logger.warning("Error while fetch namespace.");
			return(False);
		self.__NameSpaces.update( {ns.GetName():ns} );
		return(True);


	def GetDescription(self, lang=None, altlang=None):
		if not lang:
			lang = self.__Lang;
		if not altlang:
			altlang = self.__AltLang;
		self.__Logger.debug("Try to get lang %s"%lang);
		txt = self.__Description.get(lang);
		if txt:
			return(txt);
		self.__Logger.debug("Try to get lang %s"%altlang);
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

	def GetNameSpaces(self):
		return(self.__NameSpaces.keys());
	
	def GetSlots(self, Name):
		ns = self.__NameSpaces.get(Name);
		if not ns:
			self.__Logger.debug("No NS %s found"%Name);
			return(None);
		return(ns.GetSlots());

	def GetSlotType(self, NS, Name):
		ns = self.__NameSpaces.get(NS);
		if not ns:
			self.__Logger.debug("No NS %s found"%NS);
			return(None);
		return(ns.GetSlotType(Name));

	def GetSlotMode(self, NS, Name):
		ns = self.__NameSpaces.get(NS);
		if not ns:
			self.__Logger.debug("No NS found %s"%NS);
			return(None);
		return(ns.GetSlotMode(Name));

	def GetSlotDescription(self, NS, Name, lang=None, altlang=None):
		if not lang:
			lang = self.__Lang;
		if not altlang:
			altlang = self.__AltLang;

		ns = self.__NameSpaces.get(NS);
		if not ns:
			self.__Logger.debug("No NS %s found"%NS);
			return(None);
		return(ns.GetSlotDescription(Name, lang, altlang));

	def GetSlotRanges(self, Name):
		ns = self.__NameSpaces.get(Name);
		if not ns:
			self.__Logger.debug("No NameSpace named %s found"%Name);
			return(None);
		return(ns.GetSlotRanges());
	
	def GetSlotRangeDescription(self, NS, Name, lang=None, altlang=None):
		if not lang:
			lang = self.__Lang;
		if not altlang:
			altlang = self.__AltLang;

		ns = self.__NameSpaces.get(NS);
		if not ns:
			self.__Logger.warning("No NameSpace named %s found"%NS);
			return(None);
		return(ns.GetSlotRangeDescription(Name, lang, altlang));



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

	

 
class NameSpace:
	def __init__(self, xmlNode):
		self.__Logger = logging.getLogger("PPLT");
		self.__Slots = {};
		self.__SlotRanges = {};

		attr = xmlNode.attributes.get("name");
		if not attr:
			self.__Logger.warning("No namespace-name given!");
			raise Exception("No namespace-name given!");
		self.__Name = attr.value;
		
		nodelst = getNodesByTagName(xmlNode.firstChild, "Slot");
		for node in nodelst:
			self.__addSlot(node);

		nodelst = getNodesByTagName(xmlNode.firstChild, "SlotRange");
		for node in nodelst:
			self.__addSlotRange(node);

	def __addSlot(self, xmlNode):
		try:
			slot = Slot(xmlNode);
		except:
			self.__Logger.warning("Can't parse <Slot>");
			return(False);
		self.__Slots.update( {slot.GetName():slot} );
		return(True);

	def __addSlotRange(self, xmlNode):
		try:
			slot = Slot(xmlNode);
		except:
			self.__Logger.warning("Can't parse <Slot>");
			return(False);
		self.__SlotRanges.update( {slot.GetName():slot} );
		return(True);

	def GetName(self):
		return(self.__Name);
	
	def GetSlots(self):
		return(self.__Slots.keys());

	def GetSlotRanges(self):
		return(self.__SlotRanges.keys());

	def GetSlotType(self, Name):
		slot = self.__Slots.get(Name);
		if not slot:
			self.__Logger.debug("No slot %s found"%Name);
			return(None);
		return(slot.GetType());

	def GetSlotMode(self, Name):
		slot = self.__Slots.get(Name);
		if not slot:
			self.__Logger.debug("No slots %s found"%Name);
			return(None);
		return(slot.GetMode());

	def GetSlotDescription(self, Name, lang, altlang):
		slot = self.__Slots.get(Name);
		if not slot:
			self.__Logger.debug("No slot %s found"%Name);
			return(None);
		return(slot.GetDescription(lang, altlang));

	def GetSlotRangeDescription(self, Name, lang, altlang):
		slot = self.__SlotRanges.get(Name);
		if not slot:
			self.__Logger.debug("No slotrange %s found"%Name);
			return(None);
		return(slot.GetDescription(lang, altlang));


class Slot:
	def __init__(self, xmlNode):
		self.__Logger = logging.getLogger("PPLT");
		self.__Description = {};
		self.__Type = None;		#undef.
		self.__Mode = "rw";		#read and write
		
		attr = xmlNode.attributes.get("name");
		if not attr:
			self.__Logger.warning("No slot name given!");
			raise Exception("No Slot name given.");
		self.__Name = attr.value;
	
		attr = xmlNode.attributes.get("type");
		if attr:
			self.__Type = attr.value;
		
		attr = xmlNode.attributes.get("mode");
		if attr:
			self.__Mode = attr.value;

		nodelst = getNodesByTagName(xmlNode.firstChild, "Description");
		for node in nodelst:
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

	def GetType(self):
		return(self.__Type);
	
	def GetMode(self):
		return(self.__Mode);
	
	def GetDescription(self, lang, altlang):
		txt = self.__Description.get(lang);
		if txt:
			return(txt);
		return(self.__Description.get(altlang));




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


