#!/usr/bin/python


from distutils.core import setup

setup(  name = "pplt",
        version = "2.0a",
        description = """ Potsdamer Prozessleittechnik """,
        author = "Hannes Matuschek",
        author_email = "hmatuschek@gmx.net",
        url = "http://pplt.berlios.de",
        packages = ['pplt'],
        data_files = [('pplt', ['modules/debugging-modules.zip',
                                'modules/stream_reflection.xml',
                                'modules/stream_hexlify.xml',
                                'modules/stream_dump.xml',
                                'modules/sequence_reflection.xml']),
                      ('pplt/trex', ['trex/trex_assembly.xml',
                                     'trex/trex_module.xml'])])


