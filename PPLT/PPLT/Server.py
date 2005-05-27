import xml.dom.minidom;
import logging;

class Server:
	def __init__(self, CoreObject, FileName, ServerName, DefaultUser, Parameters):
		"""This is the class for pplt-server"""
		self.__Logger = logging.getLogger('PPLT');
		self.__CoreObject = CoreObject;
		self.__ServerObjects = [];
		self.__FileName = FileName;
		self.__ServerName = ServerName;
		self.__DefaultUser = DefaultUser;
		self.__Parameters = Parameters;
		self.__load();

	def __load(self):
		doc = xml.dom.minidom.parse(self.__FileName);
		loads = doc.getElementsByTagName('Load');

		for load in loads:
			try:
				obj = ServerLoad(load,
								self.__CoreObject,
								self.__DefaultUser,
								self.__Parameters);
			except:
				self.__Logger.error("Error while Load a Server");
				return(False);
			if not obj:
				self.__Logger.error("Error while Load a Server");
				self.destroy();
				return(False);
			self.__ServerObjects.append(obj);
		# --- done ---
		return(True);
	
	def destroy(self):
		for server in self.__ServerObjects:
			self.__CoreObject.ExporterDel(server);
		return(True);

	def getClassAndName(self):
		return(self.__ServerName);



def ServerLoad(Node, Core, User, Vars):
	modname = Node.attributes['name'].value;
	parameters = {};
	ParameterLoad(Node.firstChild, parameters, Vars);
	return(Core.ExporterAdd(modname,parameters,User));



def ParameterLoad(Node, Paras, Vars):
	logger = logging.getLogger('PPLT');
	if not Node:
		return(True);
	if Node.localName == 'Parameter':
		logger.debug("Process <Parameter>");
		name = Node.attributes['name'].value;
		if Node.hasChildNodes():
			if Node.firstChild.nodeType == Node.TEXT_NODE:
				value = string.strip(Node.firstChild.data);
		else:
			value = Vars.get(Node.attributes['var'].value);
		Paras.update( {name:value} );
	else:
		logger.debug("Skip %s Tag in <Load>"%Node.localName);
	return(ParameterLoad(Node.nextSibling, Paras, Vars));
	
