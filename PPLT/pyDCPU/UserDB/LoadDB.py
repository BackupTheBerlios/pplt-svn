# ############################################################################ #
# This is part of the pyDCPU project. pyDCPU is a framework for industrial     # 
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


# ChangeLog:
# 2005-08-25:
#   Add proxy-feature.

import User;
import Group;
import UserDB;
import xml.dom.minidom;
import logging;

def ParseFile(DB, FileName, Logger):
    if not isinstance(DB, UserDB.UserDB):
        Logger.error("No UserDB given");
        return(False);
    
    Document = xml.dom.minidom.parse(FileName);
    #FIXME: Check if unlink is needed!
    
    if not isinstance(Document, xml.dom.minidom.Node):
        Logger.error("Error while ParseFile...");
        return(False);

    if not Document.hasChildNodes():
        Logger.error("Invalid File Format");
        #Document.unlink();
        return(False);
    
    UserDBNode = Document.getElementsByTagName("UserDB")[0];
    if not UserDBNode.hasChildNodes():
        Logger.error("Invalid DB Format");
        #Document.unlink();
        return(False);

    UserDBAttr = GetAttributesFrom(UserDBNode);
    if not UserDBAttr:
        Logger.error("Invalid DB Format: No SuperUser spez...");
        #Document.unlink();
        return(False);
    
    SuperUser = UserDBAttr.get('superuser');
    if not SuperUser:
        Logger.error("No super user def...");
        #Document.unlink();
        return(False);

        
    if not ProcessUserDB(UserDBNode.firstChild, DB):
        Logger.error("error while process user db file");
        #Document.unlink();
        return(False);

    if not DB.SetSuperUser(SuperUser):
        #Document.unlink();
        return(False);
 
    #Document.unlink();
    return(True);
    


def ProcessUserDB(Node, DB):
    Logger = logging.getLogger('pyDCPU');
    if not isinstance(Node, xml.dom.minidom.Node):
        return(True);
    if not isinstance(DB, UserDB.UserDB):
        return(False);

    if IsGroupTag(Node):
        GroupAttr = GetAttributesFrom(Node);
        if GroupAttr:
            if GroupAttr.has_key('name'):
                Name = GroupAttr.get('name');
                if DB.CreateGroup(None, Name):
                    Logger.debug("Group \"%s\" added"%Name);
                    if Node.hasChildNodes():
                        ProcessGroup(Node.firstChild, Name, DB);
                else:
                    Logger.error("Error while create group, mybe group \"%s\" already exists"%Name);

    if not Node.nextSibling:
        return(True);
    return(ProcessUserDB(Node.nextSibling, DB));


def ProcessGroup(Node, ParentGroupName, DB):
    if not isinstance(DB, UserDB.UserDB):
        return(False);
    Logger = logging.getLogger('pyDCPU');
    
    if IsMemberTag(Node):
        MemberAttr = GetAttributesFrom(Node);
        if MemberAttr:
            if MemberAttr.has_key('name') and MemberAttr.has_key('passwd'):
                Name = MemberAttr.get('name');
                Desc = MemberAttr.get('desc');
                Pass = MemberAttr.get('passwd');
                if DB.CreateMember(ParentGroupName, Name, Pass, Desc, Encode=False):
                    Logger.debug("Add member %s to %s"%(Name,ParentGroupName));
                else:
                    Logger.error("Error while create user, maybe user \"%s\" already exists"%Name);
        else:
            Logger.error("MemberTag without attrs");

    elif IsProxyTag(Node):
        ProxyAttr = GetAttributesFrom(Node);
        if ProxyAttr:
            if ProxyAttr.has_key("for"):
                For = ProxyAttr.get("for");
                if DB.CreateProxy(ParentGroupName, For, CareLess=True):
                    Logger.debug("Create proxy for %s in %s"%(For, ParentGroupName));
                else:
                    Logger.error("Error while create proxy for %s"%For);
        else:
            Logger.error("Proxytag without attr.");

    elif IsGroupTag(Node):
        GroupAttr = GetAttributesFrom(Node);
        if GroupAttr:
            if GroupAttr.has_key('name'):
                Name = GroupAttr.get('name');
                if DB.CreateGroup(ParentGroupName, Name):
                    Logger.debug("Add subgroup %s to %s"%(Name, ParentGroupName));
                    if Node.hasChildNodes():
                        ProcessGroup(Node.firstChild, Name, DB);
                else:
                    Logger.error("Error whil create group, mybe group \"%s\" already exists"%Name);
    else:
        pass;

    if not Node.nextSibling:
        return(True);

    return(ProcessGroup(Node.nextSibling, ParentGroupName, DB));


def IsGroupTag(Node):
    if not isinstance(Node, xml.dom.minidom.Node):
        return(False);
    if not Node.nodeType == Node.ELEMENT_NODE:
        return(False);
    if not Node.localName == "Group":
        return(False);
    else:
        return(True);
    return(False);

def IsMemberTag(Node):
    if not isinstance(Node, xml.dom.minidom.Node):
        return(False);
    if not Node.nodeType == Node.ELEMENT_NODE:
        return(False);
    if not Node.localName == "Member":
        return(False);
    else:
        return(True);
    return(False);

def IsProxyTag(Node):
    if not isinstance(Node, xml.dom.minidom.Node):
        return(False);
    if not Node.nodeType == Node.ELEMENT_NODE:
        return(False);
    if not Node.localName == "Proxy":
        return(False);
    else:
        return(True);
    return(False);

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

