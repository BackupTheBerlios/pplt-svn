import xml.dom.minidom;
import os.path;
import zipfile;
import shutil;
import string;

""" This module install PPLT-Modules """

def InstallFile(FileName,Name,InGroup,ModulePath):
    if not os.path.exists(FileName):
        print "Error %s not found"%FileName;
        return(False);

    if not zipfile.is_zipfile(FileName):
        print "Invalid or damaged ZIP";
        return(False);

    grplst = InGroup.split('.');
    pathlst = [ModulePath];
    for item in grplst:
        if item != '':
            pathlst.append(item);

    dirname =  os.path.normpath(string.join(pathlst,'/'));
    print "Install to %s"%dirname;
    if not os.path.isdir(dirname):
        os.makedirs(dirname,0755);
    shutil.copy(FileName, dirname+'/'+Name+'.zip');
    return(True);

def InstallToDB(Name, Group, Core):
    tmp = Group.split('.');
    path = [];
    for item in tmp:
        if item != '':
            path.append(item);
    path.append(Name);
    FullName = string.join(path,'.');
    return(Core.ModInfoAddMod(FullName));

def InstallSet(FileName, ModulePath, Core):
    doc = xml.dom.minidom.parse(FileName);
    modlist = doc.getElementsByTagName('Install');

    zipdir = os.path.dirname(os.path.abspath(FileName));
    
    for mod in modlist:
        fname = os.path.join(zipdir,mod.getAttribute('file'));
        name = mod.getAttribute('as');
        group = mod.getAttribute('in');
        if InstallFile(fname, name, group, ModulePath):
           InstallToDB(name, group, Core);
    return(True);
        
