import cmd;
import string;
import sys;
import PPLTBugReport;
import logging;


class MasterShell(cmd.Cmd):
    def __init__(self, Core, AliasTable):
        cmd.Cmd.__init__(self);
        self.__Core = Core;
        self.__AliasTable = AliasTable;
        self.CWP = [];
        self.CWD = CWDFromCWP(self.CWP);
        self.CPI = CPIFromCWP(self.CWP, self.__AliasTable);
        self.prompt = UpdatePrompt(self.CWD);
        self.Logger = logging.getLogger('pyDCPU');


    def emptyline(self):
        return(False);

    def do_exit(self, dummy=None):
        """ Return to main console."""
        return(True);


    def do_cd(self, Name):
        """ Change "into" the given module, to access all attached modules."""
        if not Name or Name == '':
            return(False);
        
        if Name == '..':
            if len(self.CWP) == 0:
                return(False);
            self.CWP = self.CWP[:-1];
            self.CPI = CPIFromCWP(self.CWP,self.__AliasTable);
            self.CWD = CWDFromCWP(self.CWP);
            self.prompt = UpdatePrompt(self.CWD);
            return(False);
        
        cl = self.__Core.MasterTreeList(self.CPI);
        cid= self.__AliasTable.GetID(Name);
        if not cid:
            print "%s unkown"%Name;
            return(False);
        if not cl.count(cid)==1:
            print "%s unkown"%Name;
            return(False);
        self.CWP.append(Name);
        self.CWD = CWDFromCWP(self.CWP);
        self.CPI = cid;
        self.prompt = UpdatePrompt(self.CWD);
        return(False);


    def do_ls(self, dummy=None):
        """ List all modules attached on the current. """
        cl = self.__Core.MasterTreeList(self.CPI);
        for child in cl:
            print self.__AliasTable.GetAlias(child);
        return(False);


    def do_rm(self, Alias):
        """ Remove/unload a module """
        if not Alias or Alias == '':
            print "USEAGE: rm ALIAS";
            return(False);
        cl = self.__Core.MasterTreeList(self.CPI);
        cid = self.__AliasTable.GetID(Alias);
        if not cid:
            print "%s unknown"%Alias;
            return(False);
        if not cl.count(cid):
            print "%s unknown"%Alias;
            return(False);
        if not self.__Core.MasterTreeDel(cid):
            print "Can't del %s"%Alias;
            return(False);
        self.__AliasTable.DelAlias(Alias);
        return(False);
    

    def do_load(self, Para):
        """ Load a module and attach it to the current.\n   USEAGE: load MODULENAME ALIAS """
        if not Para or Para == '':
            print "USAGE: load MODULE_NAME ALIAS";
            return(False);

        ParaList = SplitParameter(Para);
        if len(ParaList) != 2:
            print "USAGE: load MODULE_NAME ALIAS";
            return(False);

        ModName = ParaList[0];
        Alias   = ParaList[1];
        print "Load %s as \"%s\""%(ModName,Alias);

        # load a symbolslot if ModName == [SymbolSlot]
        if ModName == '[SymbolSlot]':
            # check if we are not at root-level
            if not self.CPI:
                print "A SymbolSlot can only be loaded as a child of an other module";
                return(False);

            #check if we need address
            ParentClass = self.__Core.GetObjectClass(self.CPI);
            self.Logger.debug("Parent class %s"%str(ParentClass));            
            ChildNeedAddr = self.__Core.ModInfoNeedChildAddress(ParentClass);
            self.Logger.debug("Need I a address %s"%str(ChildNeedAddr));
            
            #GetAddress:
            Address = None;
            if ChildNeedAddr:
                Address = GetValue('Connection Address',None);

            #Get Type:
            Type = GetValue('Type',None);

            #Get CacheLiveTime:
            TOStr = GetValue('Cache Time','0.5');
            if TOStr == '':
                TimeOut = 0.5;
            else:
                try:
                    TimeOut = float(ToStr);
                except:
                    print "Invalid Str: %s -> Set TimeOut to 0.5"%(TOStr);
                    TimeOut = 0.5;
                
            #create SymbolSlot:
            try:
                SySl = self.__Core.MasterTreeAttachSymbolSlot(self.CPI, Address, Type,TimeOut);
            except:
                Report = PPLTBugReport.CreateReport(None);
                if Report:
                    Report.send();
                return(False);
            
            if not SySl:
                print "Error while create new symbolslot!";
                return(False);
            # add alias to table
            self.__AliasTable.Add(Alias, SySl);
            return(False);  #END

                                                          
        # check ModName
        if not self.__Core.ModInfoModuleExsist(ModName):
            print "No Module named %s!"%ModName;
            return(False);

        # check if this module can be loaded here:
        IsRootMod = self.__Core.ModInfoIsRoot(ModName);
        if IsRootMod and self.CPI:
            print "%s is a root-module: can only be loaded at /"%ModName;
            return(False);
        if not IsRootMod and not self.CPI:
            print "%s is not a root-module: can only be loaded as a child of an other module";
            return(False);

        # need a addr?
        ChildNeedAddr = False;
        if self.CPI:      #if there is an parent
            ParentClass = self.__Core.GetObjectClass(self.CPI);
            self.Logger.debug("Parent class %s"%str(ParentClass));            
            ChildNeedAddr = self.__Core.ModInfoNeedChildAddress(ParentClass);
            self.Logger.debug("Do child need addr: %s"%str(ChildNeedAddr));

        # get parameter names
        ParaList = self.__Core.ModInfoGetParaNames(ModName);
        if not ParaList:
            ParaList = [];
            
        Options = {};

        # get addr. if needed
        Address = None;
        if ChildNeedAddr:
            Address = GetValue('Connection Address',None);

        # get all the parameters
        for Para in ParaList:
            DefValue = self.__Core.ModInfoGetParaDefVal(ModName, Para);
            Value = GetValue( Para, DefValue );
            if not Value:
                if DefValue:
                    Value = DefValue;
            if Value:
                Options.update( {Para: Value} );

        #create object from module
        try:
            ObjID = self.__Core.MasterTreeAdd(self.CPI, ModName, Address, Options);
        except:
            Report = PPLTBugReport.CreateReport(None);
            if Report:
                Report.send();
            return(False);
        if not ObjID:
            print "Error while create new Object from %s"%ModName;
            return(False);
        #add alias to table
        self.__AliasTable.Add(Alias,ObjID);
        return(False);




#
# Usefull Functions
#
def GetValue(Name, Default):
    if Default:
        Prompt = "%s [%s]> "%(Name,Default);
    else:
        Prompt = "%s> "%Name;
    sys.stdout.write(Prompt);
    Value = sys.stdin.readline();
    return(Value.strip());

def SplitParameter(ParaStr):
    tmp = ParaStr.split(' ');
    PList = [];
    for item in tmp:
        if not item == '':
            PList.append(item);
    return(PList);

def SplitPath(Path):
    tmp = Path.split('/');
    PList = [];
    for item in tmp:
        if not item == '':
            PList.append(item);
    return(PList);

def CWDFromCWP(CWP):
    return('/' + string.join(CWP,'/'));

def CPIFromCWP(CWP, AliasTable):
    if len(CWP) ==0:
        return(None);
    return(AliasTable.GetID(CWP[-1]));

def UpdatePrompt(CWD):
    return("MASTER:%s> "%CWD);
    
