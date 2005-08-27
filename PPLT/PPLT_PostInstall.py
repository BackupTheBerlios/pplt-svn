import sys;
import os;

def Install():
	sys.stdout.write("postInstallation...\n");
	PYTHONDIR = sys.exec_prefix;
	PYTHONWEXE= os.path.normpath(PYTHONDIR+'\pythonw.exe');
	PYTHONEXE = os.path.normpath(PYTHONDIR+'\python.exe');
	SCRIPTDIR = os.path.normpath(PYTHONDIR+"\Scripts");
	print "ScriptDir: %s"%SCRIPTDIR
	PROGRAMS  = get_special_folder_path("CSIDL_PROGRAMS");

	sys.stdout.write("Create .bat file...\n");
	PPLTCPY   = os.path.normpath(SCRIPTDIR+'\PPLTC.py');

	BAT_FILE  = os.path.normpath(SCRIPTDIR+'\PPLTC.BAT');
	BATCHCODE = "@echo off \nstart %s %s %%1\n"%(PYTHONWEXE,PPLTCPY);
	fp = file(BAT_FILE, 'w');
	fp.write(BATCHCODE);
	fp.flush();
	fp.close();
	file_created(BAT_FILE);

	BAT_FILE  = os.path.normpath(SCRIPTDIR+'\PPLTCDEBUG.BAT');
	BATCHCODE = "@echo off \n%s %s -v %%1\n"%(PYTHONEXE,PPLTCPY);
	fp = file(BAT_FILE, 'w');
	fp.write(BATCHCODE);
	fp.flush();
	fp.close();
	file_created(PPLTCBAT);
	
	sys.stdout.write("Create folder/shortcuts in start-menu...\n");
	FOLDER    = os.path.normpath(PROGRAMS+'\PPLT');
	os.mkdir(FOLDER);
	directory_created(FOLDER);

	SHORTCUT  = os.path.normpath(FOLDER+"\PPLTCenter");
	create_shortcut(PPLTCBAT, "PPLT Center", SHORTCUT);
	file_created(SHORTCUT);

	SHORTCUT  = os.path.normpath(FOLDER+"\PPLTCenter-debug");
	create_shortcut(PPLTCBAT, "PPLT Center (debug-mode)", SHORTCUT);
	file_created(SHORTCUT);

	sys.stdout.write("Done.\n");

def Remove():
	pass;









if len(sys.argv)<2:
	sys.stdout.write("Invalid call of postinstall script.\n");
	sys.exit();


MODUS = sys.argv[1];
if MODUS == "-install":
	Install();
elif MODUS == "-remove":
	Remove();
else:
	sys.stdout.write("Invalid command-line option: %s\n"%MODUS);
	sys.exit();
