#!/usr/bin/python
from distutils.core import setup;



Stuff = ["UserDB.xml", "PPLT.conf", "help-en.htb", "help-en.chm", 
         "help-de.chm", "help-de.htb"];

Icons = ['icons/help.xpm', 'icons/device_add.xpm', 'icons/server_add.xpm', 
         'icons/quit.xpm', 'icons/ok.xpm', 'icons/ok_up.xpm', 
         'icons/ok_uperr.xpm', 'icons/err.xpm', 'icons/not.xpm', 
         'icons/PPLTSessionFile.ico', 'icons/PPLT.ico', 'icons/proxy.xpm', 
         'icons/user.xpm', 'icons/group.xpm', 'icons/superuser.xpm', 
         'icons/class.xpm', 'icons/device.xpm', 'icons/folder.xpm', 
         'icons/folder2.xpm', 'icons/pack_add.xpm', 'icons/server.xpm', 
         'icons/slot-range.xpm', 'icons/slot.xpm', 'icons/symbol.xpm', 
         'icons/info.xpm', 'icons/new.xpm', 'icons/load.xpm', 
         'icons/saveas.xpm', 'icons/save.xpm'];

Examples = ['examples/Random-JVisuServer.psf','examples/Random-WebServer.psf'];


# --- Modulelists ---
PPLTMods      = ["Modules/ftp/PPLTModules/AGILENT_5462X-0.3.xml", 
                 "Modules/ftp/PPLTModules/GSMMobilePhone-0.3.xml",
                 "Modules/ftp/PPLTModules/JVisuServer-0.3.xml",
                 "Modules/ftp/PPLTModules/Panasonic_FPWEB-0.3.xml",
                 "Modules/ftp/PPLTModules/Panasonic_FPX-0.3.xml",
                 "Modules/ftp/PPLTModules/PPLTWebServer-0.3.xml",
                 "Modules/ftp/PPLTModules/RandomGenerator-0.3.xml",
                 "Modules/ftp/PPLTModules/SIMATIC_S7_200-0.3.xml",
                 "Modules/ftp/PPLTModules/SimpleExportServer-0.3.xml"];

CoreInterface = ["Modules/ftp/CoreModules/SendMail.zip",
                 "Modules/ftp/CoreModules/Socket.zip",
                 "Modules/ftp/CoreModules/UniSerial.zip",
                 "Modules/ftp/CoreModules/WGet.zip"];

CoreTransport  = ["Modules/ftp/CoreModules/MEWCOM-TL.zip",
                  "Modules/ftp/CoreModules/PPI.zip",
                  "Modules/ftp/CoreModules/ReadLine.zip"];
                 
CoreDevice    = ["Modules/ftp/CoreModules/5462X.zip",
                 "Modules/ftp/CoreModules/A200.zip",
                 "Modules/ftp/CoreModules/GSM.zip",
                 "Modules/ftp/CoreModules/MEWCOM-CL.zip",
                 "Modules/ftp/CoreModules/S7.zip"];

CoreDebug     = ["Modules/ftp/CoreModules/HexDump.zip",
                 "Modules/ftp/CoreModules/Random.zip",
                 "Modules/ftp/CoreModules/Statistic.zip",
                 "Modules/ftp/CoreModules/Echo.zip",
                 "Modules/ftp/CoreModules/testLock.zip",
                 "Modules/ftp/CoreModules/Null.zip"];

CoreExport    = ["Modules/ftp/CoreModules/JVisu.zip",
                 "Modules/ftp/CoreModules/PPLTWeb.zip",
                 "Modules/ftp/CoreModules/SimpleExport.zip"];



setup(name = "PPLT",
      version="0.9.0",
      description="PPLT a free framework for master-slave communication.",
      author="Hannes Matuschek",
      author_email="hmatuschek@gmx.net",
      url='http://pplt.berlios.de',

      packages=['pyDCPU',
                'PPLT',
                'PPLT.ModSrc',
                'PPLT.Center'],

      scripts =["Scripts/PPLTMod.py","Scripts/PPLTC.py","PPLT_PostInstall.py"],

      data_files = [('PPLT', Stuff),
                    ('PPLT/icons', Icons),
                    ('PPLT/de/LC_MESSAGES', ['I18N/de/PPLT.mo']),
                    ('PPLT/examples', Examples),
                    ('PPLT/PPLTMods', PPLTMods),
                    ('PPLT/CoreMods/Master/Interface', CoreInterface),
                    ('PPLT/CoreMods/Master/Transport', CoreTransport),
                    ('PPLT/CoreMods/Master/Device',    CoreDevice),
                    ('PPLT/CoreMods/Master/Debug',     CoreDebug),
                    ('PPLT/CoreMods/Export',           CoreExport)],

      long_description="""
PPLT is a framework for master-slave based communication.

Until now there are plugins (modules) for the Siemens SIAMTIC S7-200 over PPI, 
Panasonic/NAiS FP0 and FP2, Siemens (maybe other GSM compatible) mobile phone
and Agilent oscilloscope of the 5462x series.""",

      classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: X11 Applications',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Manufacturing',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Natural Language :: German',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Topic :: Education',
        'Topic :: Communications',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Libraries',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces'
    ]);
