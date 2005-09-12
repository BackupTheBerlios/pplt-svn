#!/usr/bin/python
from distutils.core import setup;

setup(name = "PPLT",
      version="0.3.2",
      description="PPLT a free industrial communication framework",
      author="Hannes Matuschek",
      author_email="hmatuschek@gmx.net",
      url='http://pplt.berlios.de',

      packages=['pyDCPU',
                'pyDCPU.UserDB',
                'pyDCPU.Modules',
                'PPLT',
                'PPLT.Center'],

      scripts =["Scripts/PPLTModInstall.py","Scripts/PPLTC.py","PPLT_PostInstall.py"],

      data_files = [('PPLT',["UserDB.xml","PPLT.conf"]),
                    ('PPLT/icons',['icons/PPLTSessionFile.ico',
                                   'icons/PPLT.ico',
                                   'icons/proxy.xpm',
                                   'icons/user.xpm',
                                   'icons/group.xpm',
                                   'icons/superuser.xpm',
                                   'icons/class.xpm',
                                   'icons/device.xpm',
                                   'icons/folder.xpm',
                                   'icons/folder2.xpm',
                                   'icons/pack_add.xpm',
                                   'icons/server.xpm',
                                   'icons/slot-range.xpm',
                                   'icons/slot.xpm',
                                   'icons/symbol.xpm',
                                   'icons/info.xpm',
                                   'icons/new.xpm',
                                   'icons/load.xpm',
                                   'icons/saveas.xpm',
                                   'icons/save.xpm']),
                    ('PPLT/de/LC_MESSAGES',['I18N/de/PPLT.mo']),
                    ('PPLT/examples',['examples/Random-JVisuServer.psf','examples/Random-WebServer.psf'])],

      long_description="""PPLT is an industrial communication framework.

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
