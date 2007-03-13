""" This package contains the edef-core library. """
#FIXME complete documentation:
#   * important classes
#   * examples
#   * licence

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
