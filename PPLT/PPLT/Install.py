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
    print "Install %s to %s"%(FileName,dirname);
    if not os.path.isdir(dirname):
        os.makedirs(dirname,0755);
    shutil.copy(FileName, dirname+'/'+Name+'.zip');
    return(True);

def InstallSet(FileName, ModulePath):
    doc = xml.dom.minidom.parse(FileName);
    modlist = doc.getElementsByTagName('Install');

    zipdir = os.path.dirname(os.path.abspath(FileName));
    
    for mod in modlist:
        fname = os.path.join(zipdir,mod.getAttribute('file'));
        name = mod.getAttribute('as');
        group = mod.getAttribute('in');
        if not InstallFile(fname, name, group, ModulePath):
           print "Error while install %s"%name;
    return(True);
        
