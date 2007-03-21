#!/usr/bin/python
from distutils.core import setup


long_desc = """ 
edef is a simple discrete event simulation framework. It can
handle simple logic circuits but also more complex autoregressive 
processes and digital controller circuits. 

There is a GUI application that itegrates a development environment for this
framwork and a circuit editor. """


clsfy = ["Development Status :: 3 - Alpha",
         "Environment :: Win32 (MS Windows)",
         "Environment :: X11 Applications",
         "Intended Audience :: Developers",
         "Intended Audience :: Education",
         "Intended Audience :: Science/Research",
         "License :: OSI Approved :: GNU General Public License (GPL)",
         "Operating System :: OS Independent",
         "Programming Language :: Python",
         "Topic :: Education",
         "Topic :: Scientific/Engineering"]

setup(  name = "edef",
        version = "0.1dev",
        description = "A simple discrete event simulation with GUI.",
        long_description = long_desc,
        author = "Hannes Matuschek",
        author_email = "hmatuschek@gmail.com",
        
        url = "http://edef.sourceforge.net",
        
        classifiers = clsfy,

        packages = ['edef',
                    'edef.dev', 'edef.dev.pyeditor', 'edef.dev.modeditor',
                                'edef.dev.circuit', 'edef.dev.shell',
                                'edef.dev.bitmaps', 'edef.dev.cursors',
                                'edef.dev.eventmanager'],
        package_dir = {"edef.dev":"edef-dev"},
        
		scripts=['edef-dev.py'],

        package_data = {"edef": ["Module-1.0.xsd"]},
		
        data_files = [("share/edef", ["modules/logic.AND.xml","modules/logic.OR.xml",
                                      "modules/logic.NOT.xml","modules/logic.IDT.xml",
                                      "modules/logic.trigger.xml","modules/logic.gui.button.xml",
                                      "modules/logic.gui.lamp.xml", "modules/logic.XOR.xml",
                                      "modules/random.generator.xml",
                                      "modules/random.randomize.xml"]),
                      ("share/edef", ["modules/logic-modules.zip",
                                      "modules/gui-modules.zip",
                                      "modules/random-modules.zip"])])


