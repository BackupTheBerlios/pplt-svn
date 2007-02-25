#!/usr/bin/python


from distutils.core import setup

setup(  name = "edef",
        version = "0.1a",
        description = """ NOT SET YET """,
        author = "Hannes Matuschek",
        author_email = "hmatuschek@gmx.net",
        url = "http://pplt.berlios.de",
        packages = ['edef',
                    'edef-dev', 'edef-dev.pyeditor', 'edef-dev.modeditor',
                                'edef-dev.circuit', 'edef-dev.shell',
                                'edef-dev.bitmaps', 'edef-dev.cursors'])


