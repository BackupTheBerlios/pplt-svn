""" Decoratros are used to specify the I{type} of an input. 
    
    Normally an imput would be something callable. Like a function or class 
    implementing the __call__ method. To enable the output to check the "type"
    of an input added to it, this decorators are used. Decorate your input 
    with one of this to avoid warning of the outputs that no type is 
    specified. """


# ########################################################################## #
# Decorators.py
#
# 2007-01-18
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

# FIXME: These decorators are not usable with edef-dev!

def BoolDecorator(f):
    def _wrapper(*args):
        if len(args) == 1: return f( bool(args[0]) )
        if len(args) == 2: return f( args[0], bool(args[1]) )
    _wrapper.dec_type_name = "bool"
    return _wrapper

def IntegerDecorator(f):
    def _wrapper(*args):
        if len(args) == 1: return f( int(args[0]) )
        if len(args) == 2: return f( args[0], int(args[1]) )
    _wrapper.dec_type_name = "int"
    return _wrapper

def FloatDecorator(f):
    def _wrapper(*args):
        if len(args) == 1: return f( float(args[0]) )
        if len(args) == 2: return f( args[0], float(args[1]) )
    _wrapper.dec_type_name = "float"
    return _wrapper

def ComplexDecorator(f):
    def _wrapper(*args):
        if len(args) == 1: return f( complex(args[0]) )
        if len(args) == 2: return f( args[0], complex(args[1]) )
    _wrapper.dec_type_name = "complex"
    return _wrapper

def StringDecorator(f):
    def _wrapper(*args):
        if len(args) == 1: return f( str(args[0]) )
        if len(args) == 2: return f( args[0], str(args[1]) )
    _wrapper.dec_type_name = "str"
    return _wrapper

def StreamDecorator(f):
    def _wrapper(*args):
        if len(args) == 1: return f( str(args[0]) )
        if len(args) == 2: return f( args[0], str(args[1]) )
    _wrapper.dec_type_name = "stream"
    return _wrapper

#FIXME build some frame-types (BoolSeqDecorator,...)


