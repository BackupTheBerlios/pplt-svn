#!/usr/bin/python
import xml.dom.minidom;

class Context:
	def __init__(self, Vars):
		self.__Vars = Vars;
		self.__SwitchFor = None;
		self.__IsServer = False;
		self.__IsDevice = False;

	def GetValue(self, Of):
		return(self.__Vars.get(Of));

	def SetSwitch(self, VarName):
		self.__SwitchFor = VarName;

	def GetSwitch(self):
		return(self.__Vars.get(self.__SwitchFor));

	def Load(self, Name=None, Parent = None, Paras=None, Addr=None):
		if self.__IsServer:
			print "CTX: Load Server %s with \"%s\""%(Name,str(Paras));
		else:
			print "CTX: Load Device %s with \"%s\" @ %s"%(Name,str(Paras),str(Addr));
		return(True);

	def SetServer(self):
		self.__IsServer = True;

	def SetDevice(self):
		self.__IsDevice = True;

	def IsServer(self):return(self.__IsServer);

	def IsDevice(self):return(self.__IsDevice);




def DocWalker(Node, CTX):
	if not Node:
		return(None);

	if Node.nodeType == Node.ELEMENT_NODE:
		if Node.localName == "PPLTDevice":
			CTX.SetDevice();
			DocWalker(Node.firstChild, CTX);
		elif Node.localName == "PPLTServer":
			CTX.SetServer();
			DocWalker(Node.firstChild, CTX);

		elif Node.localName == "setup":
			DocWalker(Node.firstChild, CTX);

		elif Node.localName == "Switch":
			variable = str(Node.getAttribute("variable"));
			#print "SWITCH: for %s"%variable;
			CTX.SetSwitch(variable)
			SwitchWalker(Node.firstChild, CTX);

		elif Node.localName == "Load":
			name  = str(Node.getAttribute("name"));
			(paras,addr) = ParameterWalker(Node.firstChild, CTX, {}, None);
			if CTX.Load(name,paras,addr): #if load success:
				DocWalker(Node.firstChild, CTX);

		elif Node.localName == "DebugInfo":
			print "DEBUG: %s"%str(TextWalker(Node.firstChild,None));

		elif Node.localName == "RaiseError":
			raise Exception(str(ErrorWalker(Node.firstChild,None)));

		else:
			#print "ignore element: %s"%Node.localName;
			pass;
	
	return(DocWalker(Node.nextSibling, CTX));





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





def VarWalker(Node, CXT):
	return( CTX.GetValue(str(Node.getAttribute("name"))) );





def SwitchWalker(Node,CTX):
	if not Node:
		return(None);

	if Node.nodeType == Node.ELEMENT_NODE:
		if Node.localName == "Case":
			value = str(Node.getAttribute("value"));
			if value == CTX.GetSwitch():
				return(DocWalker(Node.firstChild, CTX));
		elif Node.localName == "Default":
			DocWalker(Node.firstChild, CTX);
		else:
			print "SWITCH: ignore tag \"%s\""%Node.localName;
	
	return(SwitchWalker(Node.nextSibling,CTX));



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





if __name__ == "__main__":
	doc = xml.dom.minidom.parse("setup1.xml");

	variables = {'Test':'c'};
	CTX = Context(variables);

	DocWalker(doc.documentElement, CTX)

