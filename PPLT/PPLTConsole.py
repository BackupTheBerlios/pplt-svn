#!/usr/bin/python

import pyDCPU;
import cmd;
import PPLT;
import sys;
import os.path;


class CommandShell(cmd.Cmd):
    def __init__(self):
        """ PPLT-Base-Console """
        cmd.Cmd.__init__(self);
        self.prompt = 'PPLT:> ';
        self.__Config = PPLT.Config();
        self.__Core = pyDCPU.Core(UserDBFile = self.__Config.GetUserDB(),
                                  LogLevel = self.__Config.GetLogLevel(),
                                  LogFile = None, #self.__Config.GetLogFile(),
                                  SysLog = self.__Config.GetSysLog(),
                                  ModuleDBFile = self.__Config.GetModuleDB());
        self.__UserDB = self.__Core.GetTheUserDB();
        self.__AliasTable = PPLT.AliasTable();

    def emptyline(self):
        pass;
        
    def do_exit(self, dummy = None):
        """ Exit."""
        return(True);
    
    def do_load(self, Project = None):
        """ load PROJECTFILE\n  Load a project from PROJECTFILE."""
        print "not implemented yet";
        return(False);

    def do_save(self, Project = None):
        """ save PROJECTFILE\n Save the current project to PROJECTFILE."""
        if not Project or Project == '':
            print "No filename given:\n USAGE: save FILENAME";
            return(False);
        if not self.__Core.SaveProjectToFile(Project):
            print "Error while save to file \"%s\""%str(Project);
        return(False);

    def do_userdb(self, dummy = None):
        """ Change to UserDB-Console."""
        shell = PPLT.UserShell(self.__Core.GetTheUserDB());
        shell.cmdloop();

    def do_symbol(self, dummy = None):
        """ Change to SymbolTree-Console."""
        sh = PPLT.SymbolShell(self.__Core, self.__AliasTable);
        sh.cmdloop();

    def do_master(self, dummy = None):
        """ Change to MasterTree-Console."""
        sh = PPLT.MasterShell(self.__Core, self.__AliasTable);
        sh.cmdloop();

#    def do_slavetree(self, dummy = None):
#        """ Change to SlaveTree-Console."""
#        pass;

    def do_server(self, dummy = None):
        """ Change to Server-Console."""
        sh = PPLT.ExportShell(self.__Core, self.__AliasTable);
        sh.cmdloop();
        return(False);
    
    def do_install(self, FileName):
        """ USAGE: install FILE\n  Install a module set from FILE."""
        PPLT.InstallSet(FileName,
                        self.__Config.GetModulePath(),
                        self.__Core);

#    def do_uninstall(self, Module = None):
#        """ USAGE: uninstall NAME\n  Uninstall the module NAME."""
#        print "not implemented yet."
#        return(False);


if __name__ == '__main__':
    sh = CommandShell();
    sh.cmdloop();

