#!/usr/bin/python
import xml.dom.minidom
import PPLT;
import string;
import logging;

def LoadSession(system, FileName):
	Logger = logging.getLogger("PPLT");
	Logger.debug("Try to load Session from %s"%FileName);
	try:
		doc = xml.dom.minidom.parse(FileName);
	except:
		Logger.errro("Error while load Session from %s"%FileName);
		return(False);

	dev_tag = doc.getElementsByTagName("Devices")[0];
	sym_tag = doc.getElementsByTagName("SymbolTree")[0];
	srv_tag = doc.getElementsByTagName("Servers")[0];

	LoadDevices(system, dev_tag);
	LoadSymTree(system, sym_tag.firstChild);
	LoadServers(system, srv_tag);
	return(True);

def LoadDevices(system, Tag):
	devlst = Tag.getElementsByTagName("Device");
	for dev in devlst:
		Para	= xmlFetchParameters(dev);
		Alias	= dev.getAttribute("alias");
		FQDN	= dev.getAttribute("fqdn");
		system.LoadDevice(FQDN, Alias, Para);

def LoadServers(system, Tag):
	srvlst = Tag.getElementsByTagName("Server");
	for srv in srvlst:
		Para	= xmlFetchParameters(srv);
		Alias	= srv.getAttribute("alias");
		FQSN	= srv.getAttribute("fqsn");
		DefUser	= srv.getAttribute("user");
		system.LoadServer(FQSN, Alias, DefUser, Para);

def LoadSymTree(system, Tag, PathList=[]):
	if not Tag:
		return(None);
	if Tag.nodeType != Tag.ELEMENT_NODE:
		return(LoadSymTree(system, Tag.nextSibling, PathList));
	if Tag.localName == "Symbol":
		Name	= Tag.getAttribute("name");
		Slot	= Tag.getAttribute("slot");
		Type	= Tag.getAttribute("type");
		Group	= Tag.getAttribute("group");
		Owner	= Tag.getAttribute("owner");
		Modus	= Tag.getAttribute("modus");
		Path	= PathList2Str(PathList+[Name]);
		system.CreateSymbol(Path, Slot, Type, Modus, Owner, Group);
	if Tag.localName == "Folder":
		Name	= Tag.getAttribute("name");
		Group	= Tag.getAttribute("group");
		Owner	= Tag.getAttribute("owner");
		Modus	= Tag.getAttribute("modus");
		Path	= PathList2Str(PathList+[Name]);
		system.CreateFolder(Path, Modus, Owner, Group);
		if Tag.hasChildNodes():
			LoadSymTree(system,Tag.firstChild,PathList+[Name]);
	return(LoadSymTree(system,Tag.nextSibling,PathList));


def xmlFetchParameters(Node):
	parameter = {};
	parlst = Node.getElementsByTagName("Parameter");
	for par in parlst:
		name = par.getAttribute("name");
		value = xmlFetchText(par.firstChild);

		parameter.update( {name:value} );
	return(parameter);

def xmlFetchText(Node,txt=""):
	if not Node:
		return(txt);
	if Node.nodeType == Node.TEXT_NODE:
		txt += string.strip(Node.data);
	return(xmlFetchText(Node.nextSibling,txt));

def PathList2Str(PathLst):
	p = "";
	if len(PathLst) == 0:
		return("/");
	for item in PathLst:
		p += "/"+item;
	return(p);



system = PPLT.System();
LoadSession(system, "test.xml");

