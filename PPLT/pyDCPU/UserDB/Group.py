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

#ChangeLog:
# 2005-08-25:
#   Add user-proxy feature

import User;
import xml.dom.minidom;

class Group:
    """ Class of grouzp objects. """
    def __init__(self, Name, ParentGroup):
        """ """
        self.__Name = Name;
        self.__SubGroupHash = {};
        self.__MemberHash = {};
        self.__ProxyList = [];
        self.__ParentGroup = ParentGroup;





    # ######################################################################## #
    #                                                                          # 
    # ######################################################################## #
    def SetName(self, Name):
        """ Sets the name of this group. """
        self.__Name = Name;
        return(True);
    def GetName(self):
        """ Return the name of the group. """
        return(self.__Name);





    # ######################################################################## #
    #                                                                          # 
    # ######################################################################## #
    def HasMembers(self):
        """ Returns true if the group has members or subgroups. """
        if len(self.__MemberHash.keys())>0 or len(self.__SubGroupHash.keys())>0:
            return(True);
        else:
            return(False);

    def IsMember(self, UserName, Direct=False):
        """ Check if the give user ís member of this group.
 if Direct == True it also checks if the user is member of 
 any sub group. """
        if self.__MemberHash.has_key(UserName):
            return(True);

        if Direct:
            return(False);
        if UserName in self.__ProxyList:
            return(True);
        if not self.__ParentGroup:
            return(False);
        return(self.__ParentGroup.IsMember(UserName, Direct=False));

    def GetParent(self):
        """ Returns the parent group (object). """
        return(self.__ParentGroup);

    



    # ######################################################################## #
    #                                                                          # 
    # ######################################################################## #
    def CreateMember(self, Name, Passwd, Desc = None):
        """ Create a new member of this group. """
        Member = User.User(Name, Passwd, Desc);
        self.__MemberHash.update( {Name:Member} );
        return(Member);

    def GetMember(self, UserName):
        """ Get the user (object) by user-name. """
        if self.__MemberHash.has_key(UserName):
            return(self.__MemberHash.get(UserName));
        for SubGroupName in self.__SubGroupHash.keys():
            SubGroup = self.__SubGroupHash.get(SubGroupName);
            retval = SubGroup.GetMember(UserName);
            if retval:
                return(retval);
        return(None);

    def DeleteMember(self, Name):
        """ Remove a member by name. """
        if self.__MemberHash.has_key(Name):
            del self.__MemberHash[Name];
            return(True);
        else:
            print "I (%s) don't know %s"%(self.__Name, Name);
            return(False);
        



    # ######################################################################## #
    #                                                                          # 
    # ######################################################################## #
    def CreateProxy(self, Name):
        """ Create a proxy for an user. """
        if Name in self.__ProxyList:
            return(True);
        self.__ProxyList.append(Name);
        return(True);

    def DeleteProxy(self, Name):
        """ Removes a proxy-member. """
        if Name in self.__ProxyList:
            self.__ProxyList.remove(Name);
            return True;
        return False;




    # ######################################################################## #
    #                                                                          # 
    # ######################################################################## #
    def CreateSubGroup(self, Name):
        """ Create a subgroup. """
        SubGroup = Group(Name, self);
        self.__SubGroupHash.update( {Name:SubGroup} );
        return(SubGroup);

    def GetSubGroup(self, GroupName):
        """ Get the group (object) of a subgroup by name. """
        if self.__SubGroupHash.has_key(GroupName):
            return(self.__SubGroupHash.get(GroupName));
        for SubGroupName in self.__SubGroupHash.keys():
            SubGroup = self.__SubGroupHash.get(SubGroupName);
            retval = SubGroup.GetSubGroup(GroupName);
            if retval:
                return(retval);
        return(None);

    def DeleteSubGroup(self, Name):
        """ Remove a subgroup. The subgroup must be empty. """
        if self.__SubGroupHash.has_key(Name):
            SubGroup = self.__SubGroupHash.get(Name);
            if not SubGroup.HasMembers():
                del self.__SubGroupHash[Name];
                del SubGroup;
                return(True);
        return(False);
 




    # ######################################################################## #
    #                                                                          # 
    # ######################################################################## #
    def CreateXMLNode(self, Doc):
        """ Iternal used method to save the userdatabase. """
        myNode = Doc.createElement("Group");
        NameAttr = Doc.createAttribute("name");
        NameAttr.nodeValue = self.__Name;
        myNode.setAttributeNode(NameAttr);

        #save all direct members:
        MbrLst = self.__MemberHash.keys();
        for MbrNm in MbrLst:
            Member = self.__MemberHash.get(MbrNm);
            tmpNode = Member.CreateXMLNode(Doc);
            if tmpNode:
                myNode.appendChild(tmpNode);

        #save all proxys
        for PrxNm in self.__ProxyList:
            tmpNode = Doc.createElement("Proxy");
            ForAttr = Doc.createAttribute("for");
            ForAttr.nodeValue = PrxNm;
            tmpNode.setAttributeNode(ForAttr);
            myNode.appendChild(tmpNode);

        #save all subgroups:
        GrpLst = self.__SubGroupHash.keys();
        for GrpNm in GrpLst:
            SubGroup = self.__SubGroupHash.get(GrpNm);
            tmpNode = SubGroup.CreateXMLNode(Doc);
            if tmpNode:
                myNode.appendChild(tmpNode);
        return(myNode);





    # ######################################################################## #
    #                                                                          # 
    # ######################################################################## #
    def ListMembers(self):
        List = self.__MemberHash.keys();
        List.sort();
        return(List);
    
    def ListSubGroups(self):
        List = self.__SubGroupHash.keys();
        List.sort();
        return(List);

    def ListProxys(self):
        l = self.__ProxyList;
        l.sort();
        return(l);

    def GoToSubGroup(self, GroupName):
        if not self.__SubGroupHash.has_key(GroupName):
            return(None);
        return(self.__SubGroupHash.get(GroupName));

    def GetPath(self):
        Path = '';
        if self.__ParentGroup:
            Path = self.__ParentGroup.GetPath();
        Path += "/%s"%(self.__Name);
        return(Path);
