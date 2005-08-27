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
# 2005-08-26:
#	- changed passwords will now be saved
# 2005-08-25:
#	- Add user-proxy feature.
#	- replace print by logging

import User;
import Group;
import LoadDB;
import Session;
import xml.dom.minidom;
import md5;

"""
    This module holds the UserDB class. (Check UserDB.UserDB)
"""

class UserDB:
    """
        The UserDB-Class holds all methods you need to load/save the
        user-database file. To modify the user/group tree and to verify user
        logons. Also you can, if the database was loaded, ask the object if a
        spezific user belongs to a spezific group.
        
                                                        Have a lot of fun.
    """

    def __init__(self, Logger, FileName=None, AutoSave = True):
        """
            This is the init method. (you know)
                * The first option is the loggerobject used to log error,
                    warning and debuging messages.
                * The second option is the filename/path to the user-database
                    file to load or to save to. (later)
                * The last boolean option means to autosave all changes you will
                    make to the user/group tree.
        """
        self.__GroupHash = {};
        self.__GroupNameList = [];
        self.__MemberNameList = [];
        self.__SuperUser = None;
        self.__Logger = Logger;
        self.__DBFileName = FileName;
        self.__SystemSession = None;
        self.__AutoSave = False;

        self.__SessionHash = {};
        
        if self.__DBFileName:
            if not self.LoadFromFile():
                self.__DBFileName = None;
                self.__AutoSave = False;
                
        self.__AutoSave = AutoSave;


        


    # ######################################################################## #
    # Set Super and Dummy user...                                              # 
    # ######################################################################## #
    def SetSuperUser(self, Name):
        """
            This method will change the superuser. (see into the reference to
            find out more)
            NOTE:
                The user that will become superuser must already exist! Else
                this method fill fail.
        """
        if not self.__MemberNameList.count(Name):
            return(False);
        self.__SuperUser = Name;

        if self.__AutoSave:
            self.SaveToFile();
        return(True);

    def GetSuperUser(self):
        """ This method returns the name of the superuser"""
        return(self.__SuperUser);

    def IsSuperUser(self, Name):
		return(self.__SuperUser == Name);

    def GetSuperUserGrp(self):
        """ This method returns the grp-name of the grp where superuser is member of """
        Grp = self.GetGroupByUserName(self.GetSuperUser());
        if not Grp:
            return(None);
        return(Grp.GetName());





    # ######################################################################## #
    # Validating Users and check membership                                    # 
    # ######################################################################## #
    def IsMemberOf(self, GroupName, MemberName):
        """
            This method will test if the user belongs to the group
        """
        if not self.__MemberNameList.count(MemberName):
            return(False);
        if not self.__GroupNameList.count(GroupName):
            return(False);

        Group = self.GetGroupByName(GroupName);
        if not Group:
            self.__Logger.warning("inconsistent grouplist... remove");
            self.__GroupNameList.remove(GroupName);
            return(False);
        return(Group.IsMember(MemberName));
    
    def ValidUser(self, UserName, Passwd):
        """
            This method will test if the password for this user.
        """
        if not self.__MemberNameList.count(UserName):
            self.__Logger.warning("User %s not found"%UserName);
            return(False);

        User = self.GetUserByName(UserName);
        if not User:
            self.__Logger.warning("inconsistent userlist... remove %s"%UserName);
            self.__MemberNameList.remove(UserName);
            return(False);
        return(User.CheckPasswd(Passwd));

    def UserExists(self, UserName):
        if not self.__MemberNameList.count(UserName):
            self.__Logger.warning("User %s not found"%UserName);
            return(False);
        return(True);
    def GroupExists(self, GroupName):
        if not self.__GroupNameList.count(GroupName):
            self.__Logger.warning("Group %s not found"%GroupName);
            return(False);
        return(True);



    # ######################################################################## #
    # Following method handle sessions/session-IDs                             # 
    # ######################################################################## #
    def Logon(self, UserName, Passwd):
        """
            To access the SymbolTree you will need a sessionID generated by
            this method.
        """
        if not self.ValidUser(UserName, Passwd):
            self.__Logger.debug("%s: invalid user or passwd"%UserName);
            return(None);
        SessionID = Session.MakeSessionID(self.__SessionHash.keys());
        self.__SessionHash.update( {SessionID: UserName} );
        return(SessionID);

    def Logoff(self, SessionID):
        """
            This method will end a session.
        """
        if not self.__SessionHash.has_key(SessionID):
            # session already was aborted
            return(False);
        del self.__SessionHash[SessionID];
        return(True);


    def GetSession(self, UserName):
        SessionID = Session.MakeSessionID(self.__SessionHash.keys());
        self.__SessionHash.update( {SessionID: UserName} );
        return(SessionID);


    def SessionGetUserName(self, SessionID):
        """
            Return the username of a session.
        """
        return(self.__SessionHash.get(SessionID));

    def SessionGetUser(self, SessionID):
        """
            Return the user-obj of a session.
        """
        UserName = self.__SessionHash.get(SessionID);
        if not UserName:
            # no session with this id
            return(None);
        return(self.GetUserByName(UserName));

    def OpenSystemSession(self):
        """
            If you use pyDCPU as a lib. you need also a session to access the
            SymbolTree.
        """
        if self.__SystemSession:
            return(self.__SystemSession);
        self.__SystemSession = Session.MakeSessionID(self.__SessionHash.keys());
        return(self.__SystemSession);

    def CloseSystemSession(self):
        """ """
        self.__SystemSession = None;
        return(True);

    def IsSystemSession(self, SessionID):
        """
            Check if it is a SystemSession...
        """
        if self.__SystemSession == SessionID:
            return(True);
        return(False);



    # ######################################################################## #
    #                                                                          # 
    # ######################################################################## #
    def CreateMember(self, GroupName, Name, Passwd, Desc, Encode=False):
        """
            This method will create a new user in the give Group.
        """
        if not Name or not Passwd or not GroupName:
            self.__Logger.error("No name | no passwd | no group");
            return(False);
        if self.__MemberNameList.count(Name):
            self.__Logger.error("Member already exists");
            return(False);
        if not self.__GroupNameList.count(GroupName):
            self.__Logger.error("Group %s not found"%GroupName);
            return(False);

        if Encode: Passwd = md5.new(Passwd).hexdigest();

        Group = self.GetGroupByName(GroupName);
        Group.CreateMember(Name, Passwd, Desc);
        self.__MemberNameList.append(Name);

        if self.__AutoSave:
            self.SaveToFile();
        return(True);


    def GetGroupByUserName(self, Name):
        """ This method will return the grp of user given by name """
        if not self.__MemberNameList.count(Name):
            return(None);

        GrpNmLst = self.__GroupNameList;
        #self.__Logger.debug("search %s in %s"%(Name,str(GrpNmLst)));
        for GrpNm in GrpNmLst:
            #Group = self.__GroupHash.get(GrpNm);
            Group = self.GetGroupByName(GrpNm);
            if Group.IsMember(Name,Direct=True):
                return(Group);
        return(None);

    
    def GetUserByName(self, Name):
        """
            This method will return the user-obj to the give name.
        """
        if not self.__MemberNameList.count(Name):
            return(None);
        
        Grp = self.GetGroupByUserName(Name);
        if Grp:
            return(Grp.GetMember(Name));
        
        self.__Logger.warning("inconsitent userlist... remove %s"%Name);
        self.__MemberNameList.remove(Name);
        return(None);

    def DeleteMember(self, GroupName, MemberName):
        """
            This method will delete the give user from the give group.
        """
        if not self.__GroupNameList.count(GroupName):
            self.__Logger.error("No group named %s"%GroupName);
            return(False);
        if not self.__MemberNameList.count(MemberName):
            self.__Logger.error("No member named %s"%MemberName);
            return(False);

        if MemberName == self.__SuperUser:
            self.__Logger.error("Can not del superuser");
            return(False);

        Group = self.GetGroupByName(GroupName);
        if not Group:
            self.__Logger.error("inconsistent grouplist... delete");
            self.__GroupNameList.remove(GroupName);
            return(False);
        if not Group.DeleteMember(MemberName):
            self.__Logger.error("Error while remove member from Group");
            return(False);

        #delete all proxys for this user.
        self.DeleteAllProxy(MemberName);

        self.__Logger.debug("DeleteMember(): sucess");
        self.__MemberNameList.remove(MemberName);

        if self.__AutoSave:
            self.SaveToFile();
        return(True);

    def ChangePassword(self, MemberName, Passwd, Encode=True):
        """ This method will change the passwd of the given user. Return True
 on success and False else. """
        if not self.__MemberNameList.count(MemberName):
            return(False);
        user = self.GetUserByName(MemberName);
        if Encode: Passwd = md5.new(Passwd).hexdigest();
        user.SetPasswd(Passwd);
        if self.__AutoSave:
            self.SaveToFile();
        return(True);





    # ######################################################################## #
    #                                                                          # 
    # ######################################################################## #
    def CreateProxy(self, Group, Name, CareLess = False):
        """ Create a proxy of user (Name) in group (Group), if
 CareLess == False (default) the method checks if user (Name)
 exists before crateing the proxy. """
        #check if user exists (if careless=false):
        if not CareLess:
            if not self.UserExists(Name):
                return(False);
        group = self.GetGroupByName(Group);
        if not group:
            return(False);
        if not group.CreateProxy(Name):
            return(False);
        if self.__AutoSave:
            self.SaveToFile();
        return(True);

    def DeleteProxy(self, Group, Name):
        """ Delete the proxy of user (Name) in group (Group). """
        group = self.GetGroupByName(Group);
        if not group:
            return(False);
        if not group.DeleteProxy(Name):
            return(False);
        if self.__AutoSave:
            self.SaveToFile();
        return(True);

    def DeleteAllProxy(self, Name):
        """ Delete all proxys for a user. """ 
        for GrpName in self.__GroupNameList:
            group = self.GetGroupByName(GrpName);
            if group:
                group.DeleteProxy(Name);
        if self.__AutoSave:
            self.SaveToFile();
        return(True);


    # ######################################################################## #
    #                                                                          # 
    # ######################################################################## #
    def CreateGroup(self, ParentGroup, Name):
        """
            This method will create a new group as a subgroup of given
            parentgroup. If parentgroup is None it will create a new
            "root" group.
        """
        if not Name:
            self.__Logger.error("No Name...");
            return(False);
        if Name in self.__GroupNameList:
            self.__Logger.error("Group already exists");
            return(False);

        if not ParentGroup:
            newGroup = Group.Group(Name,None);
            self.__GroupNameList.append(Name);
            self.__GroupHash.update( {Name:newGroup} );
            return(True);

        if not self.__GroupNameList.count(ParentGroup):
            self.__Logger.error("ParentGroup %s dosn't exists"%ParentGroup);
            return(False);
        PGroup = self.GetGroupByName(ParentGroup);
        PGroup.CreateSubGroup(Name);
        self.__GroupNameList.append(Name);

        if self.__AutoSave:
            self.SaveToFile();
        return(True);

    def GetGroupByName(self, Name):
        """
            Will return the group-obj. for the given name.
        """
        if not Name in self.__GroupNameList:
            return(None);
        if self.__GroupHash.has_key(Name):
            return(self.__GroupHash.get(Name));

        GrpNmLst = self.__GroupHash.keys();
        for GrpNm in GrpNmLst:
            Group = self.__GroupHash.get(GrpNm);
            tmpGrp= Group.GetSubGroup(Name);
            if tmpGrp:
                return(tmpGrp);
        self.__Logger.warning("inconsistent grouplist... remove");
        self.__GroupNameList.remove(Name);
        return(None);

    def DeleteGroup(self, GroupName):
        """
            This method will delete this group. Note: it must be empty.
        """
        if not self.__GroupNameList.count(GroupName):
            return(False);
        Group = self.GetGroupByName(GroupName);
        if not Group:
            self.__Logger.warning("inconsistent grouplist... delete");
            self.__GroupNameList.remove(GroupName);
            return(False);

        # if the group is a sub group of mine
        if self.__GroupHash.has_key(GroupName):
            Group = self.__GroupHash.get(GroupName);
            if Group.HasMembers():
                return(False);
            del self.__GroupHash[GroupName];
            del Group;
            self.__GroupNameList.remove(GroupName);
            if self.__AutoSave:
                self.SaveToFile();
            return(True);
    
        ParentGroup = Group.GetParent();
        if not ParentGroup:
            self.__Logger.fatal("Oh my god!!! -> No parentgroup for group %s"%GroupName);
            return(False);
        
        if not ParentGroup.DeleteSubGroup(GroupName):
            return(False);
        self.__GroupNameList.remove(GroupName);

        if self.__AutoSave:
            self.SaveToFile();
        return(True);





    # ######################################################################## #
    #                                                                          #
    # ######################################################################## #
    def SaveToFile(self, FileName=None):
        """
            This method will save the user/group tree into the give file.
            if no file is give, the tree will be saved in the file you spec at
            the __init__ method.
            Note: if you put a filename there the filename you spec. at the
            __init__ method will be overwriten.
        """
        if FileName:
            self.__DBFileName = FileName;
        if not self.__DBFileName:
            return(False);
        
        impl = xml.dom.minidom.getDOMImplementation();
        Doc = impl.createDocument(None, "UserDB", None);

        myNode = Doc.documentElement;
        SUAttr = Doc.createAttribute("superuser");

        SUAttr.nodeValue = self.__SuperUser;
        myNode.setAttributeNode(SUAttr);

        GrpLst = self.__GroupHash.keys();
        for GrpNm in GrpLst:
            Group = self.__GroupHash.get(GrpNm);
            tmpNode = Group.CreateXMLNode(Doc);
            if tmpNode:
                myNode.appendChild(tmpNode);

        try:
            FilePtr = open(self.__DBFileName, "wb");
        except:
            self.__Logger.error("Error while Open File (for writeing): %s"%self.__DBFileName);
            Doc.unlink();
            return(False);

        FilePtr.write(Doc.toprettyxml('   '));
        FilePtr.close();
        Doc.unlink();
        return(True);


    def LoadFromFile(self, FileName=None):
        """
            This method loads a the user/group tree from the give file.
            If there is no file give or None: it will load from the
            file given at __init__.
        """
        if FileName:
            self.__DBFileName = FileName;

        if not LoadDB.ParseFile(self, self.__DBFileName, self.__Logger):
            self.__Logger.error("Error while parse file %s."%self.__DBFileName);
            return(False);
        return(True);

    def IsDataBase(self):
        """
            This method will return True if the database was sucsessful loaded.
        """
        if self.__DBFileName:
            return(True);
        return(False);




    # ######################################################################## #
    # Following methos a used to browse throught the groups like browsing a    #
    # filesystem                                                               #
    # ######################################################################## #
    def ListMembers(self):
        """
            I have no Members...
        """
        return ([]);

	def ListProxys(self):
		return([]);

    def ListSubGroups(self):
        """
            Return a list of known groups
        """
        List = self.__GroupHash.keys();
        List.sort();
        return(List);

    def GoToSubGroup(self, GroupName):
        """
            Return a subgroup
        """
        if not self.__GroupHash.has_key(GroupName):
            return(None);
        return(self.__GroupHash.get(GroupName));

    def GetPath(self):
        """
            My path is '/'
        """
        return('/');

    def GetParent(self):
        """
            I have no Parent
        """
        return(None);

    def GetInfo(self):
        """
            Return a info-string...
        """
        SUGrp = self.GetGroupByUserName(self.__SuperUser);
        
        info = "";
        info += "Filename     : %s\n"%self.__DBFileName;
        info += "Superuser    : %s\n"%self.__SuperUser;
        if SUGrp:
            info += "SuperUserGrp : %s\n"%SUGrp.GetName();
        info += "Users        : %i\n"%len(self.__MemberNameList);
        info += "Groups       : %i\n"%len(self.__GroupNameList);
        info += "AutoSave     : %i"%self.__AutoSave;
        return(info);








# ############################################################################ #
# USEFULL FUNCTIONS:                                                           #  
# ############################################################################ #
#  Create a new DataBase:                                                      # 
# ############################################################################ #
def CreateNewDataBase(File, AdminGroup, AdminName, Passwd, Description):
    """
        This function will create a minimal user/group database from the given
        options
    """
    if not File or not AdminGroup or not AdminName or not Passwd:
        return(False);

    Passwd = md5.new(Passwd).hexdiggest();

    impl = xml.dom.minidom.getDOMImplementation();
    Doc = impl.createDocument(None, "UserDB", None);

    myNode = Doc.documentElement;
    SUAttr = Doc.createAttribute("superuser");
    SUAttr.nodeValue = AdminName;
    myNode.setAttributeNode(SUAttr);

    GNode = Doc.createElement("Group");
    GName = Doc.createAttribute("name");
    GName.nodeValue = AdminGroup;
    GNode.setAttributeNode(GName);
    myNode.appendChild(GNode);

    ANode = Doc.createElement("Member");
    AName = Doc.createAttribute("name");
    AName.nodeValue = AdminName;
    ANode.setAttributeNode(AName);
    APass = Doc.createAttribute("passwd");
    APass.nodeValue = Passwd;
    ANode.setAttributeNode(APass);

    if Description:
        ADesc = Doc.createAttribute("desc");
        ADesc.nodeValue = Description;
        ANode.setAttributeNode(ADesc);

    GNode.appendChild(ANode);

    try:
        FilePtr = open(File,"wb");
    except:
        print "Error while open file %s"%File;
        return(False);

    FilePtr.write(Doc.toprettyxml('   '));
    FilePtr.close();
    return(True);
