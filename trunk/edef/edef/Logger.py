""" The L{Logger} class can be used to setup the logging system. """
    
# ########################################################################## #
# Importer.py
#
# 2007-01-24
# Copyright 2007 Hannes Matuschek
# hmatuschek@gmx.net
# ########################################################################## #
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# ########################################################################## #


import logging
import sys


class Logger:
    """ This class can be used to setup the logger. Specify the logging level
        and also the output file. """
    def __init__(self, level=logging.WARNING, output=sys.stderr):
        """ The contructor. The contructor take two optional areuments. The 
            first C{level} specifies the logging-level for the root-logger. 
            This should be one of ALL, DEBUG, INFO, WARNING, ERROR of the 
            logging python-module. By default the level C{logging.WARNING} is
            used. The argument output specifies an open stream type used to 
            write the messages into. By default sys.stderr is used. """
        # FIXME If output is string: interpret as logfile-name 
        # FIXME If output if file-object: use this to log
        
        # get root-logger:
        logger = logging.getLogger("edef")
        logger.setLevel(level)

        # set output:
        hdl = logging.StreamHandler(output)
        hdl.setFormatter(logging.Formatter("%(levelname)-8s %(filename)s:%(lineno)d %(message)s"))
        logger.addHandler(hdl)
