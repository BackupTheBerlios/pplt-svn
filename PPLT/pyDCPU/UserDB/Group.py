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



import User;
import xml.dom.minidom;

class Group:
    def __init__(self, Name, ParentGroup):
        self.__Name = Name;
        self.__SubGroupHash = {};
        self.__MemberHash = {};
        self.__ParentGroup = ParentGroup;





    # ######################################################################## #
    #                                                                          # 
    # ######################################################################## #
    def SetName(self, Name):
        self.__Name = Name;
        return(True);
    def GetName(self):
        return(self.__Name);





    # ######################################################################## #
    #                                                                          # 
    # ######################################################################## #
    def HasMembers(self):
        if len(self.__MemberHash.keys())>0 or len(self.__SubGroupHash.keys())>0:
            return(True);
        else:
            return(False);

    def IsMember(self, UserName, Direct=False):
        if self.__MemberHash.has_key(UserName):
            return(True);

        if Direct:
            return(False);
        if not self.__ParentGroup:
            return(False);
        return(self.__ParentGroup.IsMember(UserName));

    def GetParent(self):
        return(self.__ParentGroup);

    



    # ######################################################################## #
    #                                                                          # 
    # ######################################################################## #
    def CreateMember(self, Name, Passwd, Desc = None):
        #print "%s += %s"%(self.__Name, Name);
        Member = User.User(Name, Passwd, Desc);
        self.__MemberHash.update( {Name:Member} );
        return(Member);

    def GetMember(self, UserName):
        if self.__MemberHash.has_key(UserName):
            return(self.__MemberHash.get(UserName));
        for SubGroupName in self.__SubGroupHash.keys():
            SubGroup = self.__SubGroupHash.get(SubGroupName);
            retval = SubGroup.GetMember(UserName);
            if retval:
                return(retval);
        return(None);

    def DeleteMember(self, Name):
        if self.__MemberHash.has_key(Name):
            del self.__MemberHash[Name];
            return(True);
        else:
            print "I (%s) don't know %s"%(self.__Name, Name); 
            return(False);
        




    # ######################################################################## #
    #                                                                          # 
    # ######################################################################## #
    def CreateSubGroup(self, Name):
        SubGroup = Group(Name, self);
        self.__SubGroupHash.update( {Name:SubGroup} );
        return(SubGroup);

    def GetSubGroup(self, GroupName):
        if self.__SubGroupHash.has_key(GroupName):
            return(self.__SubGroupHash.get(GroupName));
        for SubGroupName in self.__SubGroupHash.keys():
            SubGroup = self.__SubGroupHash.get(SubGroupName);
            retval = SubGroup.GetSubGroup(GroupName);
            if retval:
                return(retval);
        return(None);

    def DeleteSubGroup(self, Name):
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
        myNode = Doc.createElement("Group");
        NameAttr = Doc.createAttribute("name");
        NameAttr.nodeValue = self.__Name;
        myNode.setAttributeNode(NameAttr);

        MbrLst = self.__MemberHash.keys();
        for MbrNm in MbrLst:
            Member = self.__MemberHash.get(MbrNm);
            tmpNode = Member.CreateXMLNode(Doc);
            if tmpNode:
                myNode.appendChild(tmpNode);

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
