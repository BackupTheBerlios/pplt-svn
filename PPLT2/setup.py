#!/usr/bin/python


from distutils.core import setup

setup(  name = "pplt",
        version = "2.0a",
        description = """ Potsdamer Prozessleittechnik """,
        author = "Hannes Matuschek",
        author_email = "hmatuschek@gmx.net",
        url = "http://pplt.berlios.de",
        packages = ['core'],
        package_dir = {'pplt':'core'},
        data_files = {'pplt': ['modules/*.zip','modules/*.xml'],
                      'pplt/trex': ['trex/*.xml']})


