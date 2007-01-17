import re

class InputWrapper:
    _d_callback = None
    _d_args     = None
    _d_name     = None

    def __init__(self, module, name, kwargs=None):
        self._d_callback    = module.input_dispacher
        self._d_args        = kwargs
        self._d_name        = name

    def __call__(self, value):
        return self._d_callback(self._d_name, value, self._d_args)




class DynamicModule:
    def __init__(self):
        pass

    def __getattr__(self, name):
        if re.match("^i_",name):
            return self.create_input(name)
        elif re.match("^o_",name):
            return self.create_output(name)
        else:
            raise AttributeError("Attribute %s not found"%name)

    
    def create_output(self, name):
        raise AttributeError("Attribute %s not found"%name)
    
    
    def create_input(self, name):
        raise AttributeError("Attribute %s not found"%name)

    
    def input_dispacher(self, name, kwargs=None):
        raise NotImplemented("The method input_dispacher have to be overridden!")
