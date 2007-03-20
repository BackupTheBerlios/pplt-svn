""" This package contains the edef-core library. """

# FIXME complete documentation:
#   * important classes
#   * examples

# ########################################################################## #
# __init__.py
#
# 2007-03-16
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


from Output import BaseOutput
from Output import ValueOutput, StreamOutput, FrameOutput
from Output import BoolOutput, IntegerOutput, FloatOutput, ComplexOutput
from Output import StringOutput, BoolSeqOutput, IntegerSeqOutput
from Output import FloatSeqOutput, ComplexSeqOutput
from Importer import Importer
from EventManager import EventManager
from Logger import Logger
from Module import InputWrapper, DynamicModule
from Decorators import BoolDecorator, IntegerDecorator, FloatDecorator
from Decorators import ComplexDecorator, StringDecorator, StreamDecorator
from Singleton import Singleton

# Test only:
from Decorators import BoolDecorator
from ModuleMeta import AssemblyMeta
