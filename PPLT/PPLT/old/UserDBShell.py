import cmd;
import string;
import sys;
import pyDCPU.UserDB;
import getpass;

class UserShell(cmd.Cmd):
    def __init__(self, DataBase):
        cmd.Cmd.__init__(self);
        self.CWD  = '/'
        self.Group = DataBase;
        self.prompt = "USERDB:%s> "%self.CWD;
        self.DataBase = DataBase;

    def emptyline(self):
        pass;

    def do_exit(self, dummy=None):
        """ Exit."""
        return(True);
      
    def do_info(self, dummy=None):
        """ Print a short information about the UserDB."""
        print self.DataBase.GetInfo();
        return(False);
    
    def do_ls(self, dummy=None):
        """ List the members and subgroup of the current group."""
        MemberList = self.Group.ListMembers();
        GroupList = self.Group.ListSubGroups();
        for Member in MemberList:
            print Member;
        for Group in GroupList:
            print "[%s]"%Group;
        return(False);
    

    def do_cd(self, GroupName):
        """ cd NAME\n  Change to subgroup NAME or to parentgroup with '..'. """
        if GroupName == '..':
            newGroup = self.Group.GetParent();
            if newGroup == None:
                newGroup = self.DataBase;
        else:
            newGroup = self.Group.GoToSubGroup(GroupName);
            if not newGroup:
                print "no group named \"%s\""%(GroupName);
                return(False);
            
        self.Group = newGroup;
        self.__setCWD(newGroup.GetPath());
        return(False);


    def do_mkgrp(self, GrpName):
        """ mkgrp NAME\n  Create a new subgroup in the current group """
        if self.CWD == '/':
            Parent = None;
        else:
            Parent = self.Group.GetName();
        
        tmpGrp = self.DataBase.CreateGroup(Parent,GrpName);

        if not tmpGrp:
            print "Error while create subgroup";
            return(False);
        return(False);


    def do_rmgrp(self, GrpName):
        """ rmgrp NAME\n  Remove subgroup NAME. """
        if not self.Group.ListSubGroups():
            print "%s does not exist"%GrpName;
            return(False);
        if not self.Group.ListSubGroups().count(GrpName):
            print "%s does not exist"%GrpName;
            return(False);
        if not self.DataBase.DeleteGroup(GrpName):
            print "%s is not empty";
        return(False);


    def do_mkuser(self, UserName):
        """ mkuser NAME\n  Create a new user in the current group."""
        if self.CWD == '/':
            print "Can only create members in groups"
            return(False);

        pass1 = getpass.getpass('Password: ');
	pass2 = getpass.getpass('Retype: ');
        pass1 = string.strip(pass1);
	pass2 = string.strip(pass2);
        
	if not pass1 == pass2:
	    print "No equeal";
	    return(False);
	    
        sys.stdout.write("A short desc.: ");
        desc = sys.stdin.readline();
        desc = string.strip(desc);

        if not self.DataBase.CreateMember(self.Group.GetName(), UserName, pass1, desc, True):
            print "Error while create user.";
        return(False);

    def do_rmuser(self, UserName):
        """ rmuser NAME\n  Remove user NAME from current group."""
        if not self.Group.ListMembers():
            print "no user named %s"%UserName;
            return(False);
        if not self.Group.ListMembers().count(UserName)>0:
            print "no user names %s"%UserName;
            return(False);
        if not self.DataBase.DeleteMember(self.Group.GetName(), UserName):
            print "error while del user";
        return(False);


    def do_su(self, UserName):
        """ su NAME\n  Set the SuperUser to NAME. """
        if not self.DataBase.SetSuperUser(UserName):
            print "Error while set super user...";
        return(False);


    def do_save(self, FileName):
        """ save FILENAME\n Save the DataBase to FILENAME or to actual DataBase if obmitted."""
        if FileName == '':
            FileName = None;

        if not self.DataBase.SaveToFile(FileName):
            print "Error while save to file...";
            
        


    def __setCWD(self, CWD):
        self.CWD = CWD;
        self.prompt = "USERDB:%s> "%self.CWD;
        return(None);






if __name__ == '__main__':
    UserDB = pyDCPU.UserDB.UserDB(None, 'UserDB.xml', True);
    if UserDB.IsDataBase():
        sh = Shell(UserDB);
        sh.cmdloop();
