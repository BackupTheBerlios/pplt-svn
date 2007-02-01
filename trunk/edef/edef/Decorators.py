""" Decoratros are used to specify the I{type} of an input. 
    
    Normally an imput would be something callable. Like a function or class 
    implementing the __call__ method. To enable the output to check the "type"
    of an input added to it, this decorators are used. Decorate your input 
    with one of this to avoid warning of the outputs that no type is 
    specified. """


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


