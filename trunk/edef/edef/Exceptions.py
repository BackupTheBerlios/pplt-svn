""" Here are all exceptions defined. """

# ########################################################################## #
# Exceptions.py
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



class edefBaseException(Exception):
    """ This is the base-exception for all I{edef}-exceptions. 
        The constructor will also log each exception raised. """
    def __init__(self, msg=""):
        logger = logging.getLogger("edef")
        logger.exception(msg)
        Exception.__init__(self, msg)
    

class ModuleImportError(edefBaseException):
    """ The exception will be raies by the L{Importer} if something goes wrong
        while importing modules. """
    pass
