""" The C{Singleton} class will be used by the C{EventManager} to implement 
    the singleton pattern. The singleton pattern ensures that ther will be 
    only on instance of a class in an application. If the constructor is 
    called the first time, an instance will be created all the next time the
    constructor is called a reference to the instance will be returned. """

# ########################################################################## #
# Singleton.py
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



class Singleton(type):
    """ This class implement the singleton pattern for other classes. """
    def __init__(self, *args):
        type.__init__(self, *args)
        self._instance = None

    def __call__(self, *args):
        if self._instance is None:
            self._instance = type.__call__(self, *args)
        return self._instance

