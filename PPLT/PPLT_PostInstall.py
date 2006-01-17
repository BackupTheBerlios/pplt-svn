import sys
import os;

def ModifyRegistry(PPLTCenter, Icon):
    import _winreg;

    root_key            = _winreg.ConnectRegistry(None, _winreg.HKEY_CLASSES_ROOT);
    psf_key             = _winreg.SetValue(root_key, ".psf", _winreg.REG_SZ, "PPLT.Session");

    PPLT_Session_key    = _winreg.CreateKey(root_key, "PPLT.Session");
    _winreg.SetValue(root_key, "PPLT.Session", _winreg.REG_SZ, "PPLT Session File");

    DefaultIcon_key     = _winreg.CreateKey(PPLT_Session_key, "DefaultIcon");
    _winreg.SetValue(PPLT_Session_key, "DefaultIcon",  _winreg.REG_SZ, Icon);

    Shell_key           = _winreg.CreateKey(PPLT_Session_key, "Shell");
    open_key            = _winreg.CreateKey(Shell_key, "open");
    command_key         = _winreg.SetValue(open_key, "command",  _winreg.REG_SZ,'%s "%%1"'%PPLTCenter);



def Install():
    print("Post Installation...");
    PYTHONDIR = sys.exec_prefix;
    PYTHONWEXE= os.path.normpath(PYTHONDIR+'\pythonw.exe');
    PYTHONEXE = os.path.normpath(PYTHONDIR+'\python.exe');
    SCRIPTDIR = os.path.normpath(PYTHONDIR+"\Scripts");
    ICONPATH  = os.path.normpath(PYTHONDIR+"\PPLT\icons\PPLT.ico");
    ICONPATH2 = os.path.normpath(PYTHONDIR+"\PPLT\icons\PPLTSessionFile.ico");

    PROGRAMS  = get_special_folder_path("CSIDL_PROGRAMS");

    print("Create folder in start-menu...\n");
    FOLDER    = os.path.normpath(PROGRAMS+'\PPLT');
    try: os.mkdir(FOLDER);
    except: pass;
    directory_created(FOLDER);

    print("Create .bat file...\n");
    PPLTCPY   = os.path.normpath(SCRIPTDIR+'\PPLTC.py');
    PPLTModPy = os.path.normpath(SCRIPTDIR+'\PPLTMod.py');

    BAT_FILE  = os.path.normpath(SCRIPTDIR+'\PPLTC.BAT');
    PPLTCENTER = BAT_FILE;
    BATCHCODE = "@echo off \nstart %s %s %%1\n"%(PYTHONWEXE,PPLTCPY);
    fp = file(BAT_FILE, 'w');
    fp.write(BATCHCODE);
    fp.flush();
    fp.close();
    file_created(BAT_FILE);
    SHORTCUT  = os.path.normpath(FOLDER+"\PPLTCenter.lnk");
    create_shortcut(BAT_FILE, "PPLT Center", SHORTCUT, "", ".", ICONPATH);
    file_created(SHORTCUT);

    BAT_FILE  = os.path.normpath(SCRIPTDIR+'\PPLTCDEBUG.BAT');
    BATCHCODE = "@echo off \n%s %s -v %%1\nPAUSE\n"%(PYTHONEXE,PPLTCPY);
    fp = file(BAT_FILE, 'w');
    fp.write(BATCHCODE);
    fp.flush();
    fp.close();
    file_created(BAT_FILE);
    SHORTCUT  = os.path.normpath(FOLDER+"\PPLTCenter-debug.lnk");
    create_shortcut(BAT_FILE, "PPLT Center (debug-mode)", SHORTCUT, "", ".", ICONPATH);
    file_created(SHORTCUT);

#    BAT_FILE  = os.path.normpath(SCRIPTDIR+'\PPLTMOD.BAT');
#    BATCHCODE = "@echo off \n%s %s %%1\n"%(PYTHONWEXE,PPLTModPy);
#    fp = file(BAT_FILE, 'w');
#    fp.write(BATCHCODE);
#    fp.flush();
#    fp.close();
#    file_created(BAT_FILE);
#    SHORTCUT  = os.path.normpath(FOLDER+"\PPLTModuleManager.lnk");
#    create_shortcut(BAT_FILE, "PPLT Module Manager", SHORTCUT, "", ".", ICONPATH);
#    file_created(SHORTCUT);



    FOLDER2 = FOLDER+"\Examples";
    try:
        os.mkdir(FOLDER2);
        directory_created(FOLDER2);
    except:
        print "Error while create folder %s"%FOLDER2;
        FOLDER2 = None;
    
    if FOLDER2:
        create_shortcut(PYTHONDIR+"\PPLT\examples\Random-JVisuServer.psf", "PPLT Center example", FOLDER2+"\Random-JVisuServer.lnk", "", ".", ICONPATH2);
        file_created(FOLDER2+"\examples\Random-JVisuServer.lnk");
        create_shortcut(PYTHONDIR+"\PPLT\examples\Random-WebServer.psf", "PPLT Center example", FOLDER2+"\Random-WebServer.lnk", "", ".", ICONPATH2);
        file_created(FOLDER2+"\examples\Random-WebServer.lnk");
        
    print "Create registry keys...";
    try: ModifyRegistry(PPLTCENTER, ICONPATH2); 
    except: print "Error while create registry keys.";
        


    print("Done.");



def Remove():
    pass;









if len(sys.argv)<2:
    sys.exit();


MODUS = sys.argv[1];
if MODUS == "-install":
    Install();
elif MODUS == "-remove":
    Remove();
else:
    sys.exit();
