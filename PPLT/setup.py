#!/usr/bin/python

from distutils.core import setup;

setup(name = "PPLT",
      version="0.1",
      description="PPLT a free industrial communication framework",
      author="Hannes Matuschek",
      author_email="hmatuschek@gmx.net",
      url='http://pplt.berlios.de',
      packages=['pyDCPU',
    		'pyDCPU.UserDB',
		'pyDCPU.Modules',
                'PPLT'],
      scripts =["PPLTConsole.py"],
      data_files = [('PPLT',['ModuleDB.xml',"UserDB.xml"])],
      long_description="PPLT is an industrial communication framework.",
      classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Lesser GNU Public License',
        'Natural Language :: English',
        'Natural Language :: German',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Topic :: Communications',
        'Topic :: Software Development :: Libraries',
    ]);
