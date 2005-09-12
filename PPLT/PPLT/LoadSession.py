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

#ChangeLog:
# 2005-06-03:
#   + Initial
import xml.dom.minidom
import string;
import logging;

def LoadSession(system, FileName):
    Logger = logging.getLogger("PPLT");
    Logger.debug("Try to load Session from %s"%FileName);
    try:
        doc = xml.dom.minidom.parse(FileName);
    except:
        Logger.error("Error while load Session from %s"%FileName);
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
        Para    = xmlFetchParameters(dev);
        Alias   = dev.getAttribute("alias");
        FQDN    = dev.getAttribute("fqdn");
        system.LoadDevice(FQDN, Alias, Para);

def LoadServers(system, Tag):
    srvlst = Tag.getElementsByTagName("Server");
    for srv in srvlst:
        Para    = xmlFetchParameters(srv);
        Alias   = srv.getAttribute("alias");
        FQSN    = srv.getAttribute("fqsn");
        DefUser = srv.getAttribute("user");
        Root    = srv.getAttribute("root");
        if not Root:
            Root = "/";
        system.LoadServer(FQSN, Alias, DefUser, Para,Root);

def LoadSymTree(system, Tag, PathList=[]):
    if not Tag:
        return(None);
    if Tag.nodeType != Tag.ELEMENT_NODE:
        return(LoadSymTree(system, Tag.nextSibling, PathList));
    if Tag.localName == "Symbol":
        Name    = Tag.getAttribute("name");
        Slot    = Tag.getAttribute("slot");
        Type    = Tag.getAttribute("type");
        Group   = Tag.getAttribute("group");
        Owner   = Tag.getAttribute("owner");
        Modus   = str(Tag.getAttribute("modus"));
        Path    = PathList2Str(PathList+[Name]);
        system.CreateSymbol(Path, Slot, Type, Modus, Owner, Group);
    if Tag.localName == "Folder":
        Name    = Tag.getAttribute("name");
        Group   = Tag.getAttribute("group");
        Owner   = Tag.getAttribute("owner");
        Modus   = Tag.getAttribute("modus");
        Path    = PathList2Str(PathList+[Name]);
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


