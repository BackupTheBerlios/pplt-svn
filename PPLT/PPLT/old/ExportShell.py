#import pyDCPU;
import cmd;
import sys;


class ExportShell(cmd.Cmd):
    def __init__(self, Core, AliasTable):
        cmd.Cmd.__init__(self);
        self.__Core = Core;
        self.__AliasTable = AliasTable;
        self.prompt = "SERVER> ";
        
    def do_exit(self, dummy=None):
        """ Exit this console\n   USEAGE: exit"""
        return(True);

    def emptyline(self):
        return(False);
    
    def do_ls(self, dummy = None):
        """ List all loaded server modules by there aliases.\n   USEAGE: ls"""
        lst = self.__Core.ExporterList();
        for expid in lst:
            alias = self.__AliasTable.GetAlias(expid);
            if alias:
                print alias;
        return(False);

    def do_load(self, parameter):
        """ Load a server-module.\n  USEAGE: load MODULENAME ALIAS"""
        lst = parameter.split(' ');
        para = [];
        for item in lst:
            if item != '':
                para.append(item);
        
        if len(para) != 2:
            print "USAGE: load MODULENAME ALIAS";
            return(False);
        NAME = para[0];
        ALIAS = para[1];
        
        if not self.__Core.ModInfoModuleExsist(NAME):
            print "Module %s do not exist"%NAME;
            return(False);

        DEFUSER = GetValue('default user',None);

        opthash  = {};
        opt = self.__Core.ModInfoGetParaNames(NAME);
        for option in opt:
            default = self.__Core.ModInfoGetParaDefVal(NAME,option);
            value = GetValue(option,default);
            if not value:
                print "Input needed";
                return(False);
            opthash.update( {option:value} );

        ObjID = self.__Core.ExporterAdd(NAME, opthash, DEFUSER);
        if not ObjID:
            print "Error while load Exporter %s"%NAME;
            return(False);
        if not self.__AliasTable.Add(ALIAS,ObjID):
            print "Bad alias %s"%ALIAS;
            self.__ExporterDel(ObjID);
            return(False);
        return(False);
        
    def do_rm(self, Alias):
        """ Stop, unload and remove a server\n   USEAGE: rm ALIAS"""
        if not Alias or Alias == '':
            print "USEAGE: rm ALIAS";
            return(False);
        ID = self.__AliasTable.GetID(Alias);
        if not ID:
            print "No alias %s defined"%Alias;
            return(False);
        if not self.__Core.ExporterDel(ID):
            print "Error while remove exporter %s"%Alias;
            return(False);
        self.__AliasTable.DelID(ID);
        return(False);








def GetValue(Name, Default = ''):
    if Default:
        prompt = "%s [%s]> "%(Name, Default);
    else:
        prompt = "%s> "%Name;

    sys.stdout.write(prompt);
    Value = sys.stdin.readline();
    if Value.strip() == '':
        return(Default)
    return(Value.strip());
    
