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
# 2005-05-27:
#	- fixed bug in Server.__load():
#		missed to remove stop exsisting Core-Exporter on exception while load a new
#	- fixed bug in Server.destroy():
#		method is now error-sensitiv		
#	- fixed missing exception raise in Server.__init__() if server load fails.
import xml.dom.minidom;
import logging;

class Server:
	def __init__(self, CoreObject, FileName, ServerName, DefaultUser, Parameters, Root="/"):
		"""This is the class for pplt-server"""
		self.__Logger = logging.getLogger('PPLT');
		self.__CoreObject = CoreObject;
		self.__ServerObjects = [];
		self.__FileName = FileName;
		self.__ServerName = ServerName;
		self.__DefaultUser = DefaultUser;
		self.__Parameters = Parameters;
		self.__Root = Root;
		if not self.__load():
			raise Exception();

	def __load(self):
		doc = xml.dom.minidom.parse(self.__FileName);
		loads = doc.getElementsByTagName('Load');

		for load in loads:
			try:
				obj = ServerLoad(load,
								self.__CoreObject,
								self.__DefaultUser,
								self.__Parameters,
								self.__Root);
			except:
				self.__Logger.error("Error while Load a Server, maybe invalid format or not an server.");
				self.destroy();
				return(False);
			if not obj:
				self.__Logger.error("Error while Load a Server, maybe bad parameters.");
				self.destroy();
				return(False);
			self.__ServerObjects.append(obj);
		# --- done ---
		return(True);
	
	def destroy(self):
		for server in self.__ServerObjects:
			if self.__CoreObject.ExporterDel(server):
				self.__ServerObjects.remove(server);
			else:
				self.__Logger.error("Error while stop server");
				return(False);
		return(True);

	def getClassAndName(self):
		return(self.__ServerName);
	def getDefaultUser(self):
		return(self.__DefaultUser);
	def getParameters(self):
		return(self.__Parameters);
	def getRoot(self):
		return(self.__Root);

def ServerLoad(Node, Core, User, Vars, Root):
	modname = Node.attributes['name'].value;
	parameters = {};
	ParameterLoad(Node.firstChild, parameters, Vars);
	return(Core.ExporterAdd(modname,parameters,User,Root));



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
			elif Node.firstChild.nodeType == node.ELEMENT_NODE:
				varname = Node.firstChild.attributes['name'].value;
				value = Vars.get(varname);
		Paras.update( {name:value} );
	else:
		#logger.debug("Skip %s Tag in <Load>"%Node.localName);
		pass;
	return(ParameterLoad(Node.nextSibling, Paras, Vars));
	
