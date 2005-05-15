import cmd;
import string;
import copy;
import sys;

class SymbolShell(cmd.Cmd):
    def __init__(self, Core, AliasTable):
        cmd.Cmd.__init__(self);
        self.__Core = Core;
        self.__AliasTable = AliasTable;
        self.CWP = [];
        self.CWD = CWDFromCWP(self.CWP);
        self.prompt = UpdatePrompt(self.CWD);


    def emptyline(self):
        pass;
        
    def do_exit(self, dummy=None):
        """ Exit this console and return to main console """
        return(True);

    def do_ls(self, dummy=None):
        """ List all symbols in the current folder """
        symbols = self.__Core.SymbolTreeListSymbols(self.CWD);
        folders = self.__Core.SymbolTreeListFolder(self.CWD);
        for folder in folders:
            print "[%s]\t\t%s\t%s\t%s"%(folder,
                                        self.__Core.SymbolTreeGetRight(self.CWD+'/'+folder),
                                        self.__Core.SymbolTreeGetOwner(self.CWD+'/'+folder),
                                        self.__Core.SymbolTreeGetGroup(self.CWD+'/'+folder));
        for symbol in  symbols:
            print "%s\t\t%s\t%s\t%s"%(symbol,
                                      self.__Core.SymbolTreeGetRight(self.CWD+'/'+symbol),
                                      self.__Core.SymbolTreeGetOwner(self.CWD+'/'+symbol),
                                      self.__Core.SymbolTreeGetGroup(self.CWD+'/'+symbol));

        return(False);
    
    def do_cd(self, name=None):
        """ Change into a folder """
        if not name or name == '':
            return(False);

        if name == '..':
            if len(self.CWP)==0:
                return(False);
            self.CWP = self.CWP[:-1];
            self.CWD = CWDFromCWP(self.CWP);
            self.prompt = UpdatePrompt(self.CWD);
            return(False);
        
        l = self.__Core.SymbolTreeListFolder(self.CWD);
        if l.count(name) == 1:
            self.CWP.append(name);
            self.CWD = CWDFromCWP(self.CWP);
            self.prompt = UpdatePrompt(self.CWD);
            return(False);
        print "No dir named %s"%name;
        return(False);

    def do_mkdir(self, DIR):
        """ Create a folder """
        if not DIR or DIR == '':
            print "USEAGE: mkdir DIRNAME";
            return(False);
        tmp = copy.copy(self.CWP);
        tmp.append(DIR);
        tmpp = CWDFromCWP(tmp);
        if not self.__Core.SymbolTreeCreateFolder(tmpp):
            print "Can't create folder %s"%tmpp;
        return(False);


    def do_mksym(self, Name):
        """ Create a new symbol.\n   USEAGE: mksym NAME """
        if not Name or Name == '':
            print "USEAGE: mksym NAME";
            return(False);
        #get SymbolSlot
        Slot = GetValue('SymbolSlot',None);
        if not Slot:
            print "Need SymbolSlotName";
            return(False);

        # check slot name
        SlotID = self.__AliasTable.GetID(Slot);
        if not SlotID:
            print "No Slot named %s found"%Slot;
            return(False);
        if not self.__Core.GetObjectClass(SlotID) == '[MasterSymbolSlot]':
            print "Object %s is not a symbol slot";
            return(Flase);
        
        # get type:
        Type = GetValue('Type',None);
        if not Type:
            print "Type needed";
            return(None);

        ncwp = copy.copy(self.CWP);
        ncwp.append(Name);
        ncwd = CWDFromCWP(ncwp);
        
        if not self.__Core.SymbolTreeCreateSymbol(ncwd, SlotID, Type):
            print "Error while create Symbol %s"%ncwd;
            return(False);
        return(False);


    def do_rmdir(self, DIR):
        """ Remove a empty folder """
        if not DIR or DIR == '':
            print "USEAGE: rmdir DIRNAME";
            return(False);

        tmp = copy.copy(self.CWP);
        tmp.append(DIR);
        tmpp = CWDFromCWP(tmp);
        if not self.__Core.SymbolTreeDeleteFolder(tmpp):
            print "Can't delete folder %s"%tmpp;
        return(False);

    def do_rmsym(self, Name):
        """ Remove a symbol """
        if not Name or Name == '':
            print "USEAGE: rmsym NAME";
            return(False);
        #create new path:
        ncwp = copy.copy(self.CWP);
        ncwp.append(Name);
        ncwd = CWDFromCWP(ncwp);
        # delete symbol
        if not self.__Core.SymbolTreeDeleteSymbol(ncwd):
            print "Error while del symbol %s"%ncwd;
            return(False);
        return(False);

    def do_read(self, Name):
        """ Read from a symbol\n   USEAGE: read SYMBOLNAME"""
        if not Name or Name == '':
            print "USEAGE: read SYMBOL";
            return(None);
        #create new path:
        ncwp = copy.copy(self.CWP);
        ncwp.append(Name);
        ncwd = CWDFromCWP(ncwp);
        #read value:
        Value = self.__Core.SymbolTreeGetValue(ncwd);
        print "Value of (%s): %s"%(ncwd,str(Value));
        return(False);

    def do_write(self, Str):
        """ Write in to symbol\n   USEAGE: write SYMBOLNAME VALUE"""
        if not Str or Str == '':
            print "USEAGE: write SYMBOL VALUE";
            return(False);

        tmp = Str.split(' ');
        if not len(tmp)==2:
            print "USEAGE: write SYMBOL VALUE";
            return(False);
        Name = tmp[0];
        Value = tmp[1];

        #create new path:
        ncwp = copy.copy(self.CWP);
        ncwp.append(Name);
        ncwd = CWDFromCWP(ncwp);
        #write value:
        ret = self.__Core.SymbolTreeSetValue(ncwd,Value);
        if not ret:
            print "Error while write to %s"%ncwd;
        return(False);

    def do_chown(self, Str):
        """ Change the owner of a symbol or folder\n   USEAGE: chown OWNER SYMBOL|FOLDER"""
        if not Str or Str == '':
            print "USAGE: chown OWNER SYMBOL|FOLDER";
            return(False);
        tmp = Str.split(' ');
        para = [];
        for item in tmp:
            if item != '':
                para.append(item);
        if len(para) != 2:
            print "USAGE: chown OWNER SYMBOL|FOLDER";
            return(False);
        Symbol = tmp[1];
        Name = tmp[0];

        #create new path:
        ncwp = copy.copy(self.CWP);
        ncwp.append(Symbol);
        ncwd = CWDFromCWP(ncwp);
        if not self.__Core.SymbolTreeSetOwner(ncwd,Name):
            print "Error while chown";
            return(False);
        return(False);


    def do_chgrp(self, Str):
        """ Change the group of a symbol or folder\n   USEAGE: chgrp GROUP SYMBOL|FOLDER"""
        if not Str or Str == '':
            print "USAGE: chgrp GROUP SYMBOL|FOLDER";
            return(False);
        tmp = Str.split(' ');
        para = [];
        for item in tmp:
            if item != '':
                para.append(item);
        if len(para) != 2:
            print "USAGE: chgrp GROUP SYMBOL|FOLDER";
            return(False);
        Symbol = tmp[1];
        Name = tmp[0];

        #create new path:
        ncwp = copy.copy(self.CWP);
        ncwp.append(Symbol);
        ncwd = CWDFromCWP(ncwp);
        if not self.__Core.SymbolTreeSetGroup(ncwd,Name):
            print "Error while chown";
            return(False);
        return(False);

    def do_chmod(self, Str):
        """ Change the access rights (modus) of a symbol or folder\n   USEAGE: chmod MODUS SYMBOL|FOLDER"""
        if not Str or Str == '':
            print "USAGE: chmod MODUS SYMBOL|FOLDER";
            return(False);
        tmp = Str.split(' ');
        para = [];
        for item in tmp:
            if item != '':
                para.append(item);
        if len(para) != 2:
            print "USAGE: chmod MODUS SYMBOL|FOLDER";
            return(False);
        Symbol = tmp[1];
        Modus = tmp[0];

        #create new path:
        ncwp = copy.copy(self.CWP);
        ncwp.append(Symbol);
        ncwd = CWDFromCWP(ncwp);
        if not self.__Core.SymbolTreeSetRight(ncwd,Modus):
            print "Error while chown";
            return(False);
        return(False);









#
# Usefull Functions
#
def SplitPath(Path):
    tmp = Path.split('/');
    PList = [];
    for item in tmp:
        if not item == '':
            PList.append(item);
    return(PList);

def CWDFromCWP(CWP):
    return('/' + string.join(CWP,'/'));
def UpdatePrompt(CWD):
    return("SYMBOL:%s> "%CWD);

def GetValue(Name, Default):
    if Default:
        Prompt = "%s [%s]> "%(Name,Default);
    else:
        Prompt = "%s> "%Name;
    sys.stdout.write(Prompt);
    Value = sys.stdin.readline();
    return(Value.strip());
