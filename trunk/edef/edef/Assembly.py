from Module import DynamicModule, InputWrapper
from Output import ValueOutput


class Assembly(DynamicModule):
    _d_module_table = None
    _d_io_list = None

    def __init__(self, module_table, io_list):
        DynamicModule.__init__(self)
        self._d_module_table = module_table
        self._d_io_list = io_list
        self._d_logger.debug("Instance Assembly with modules (%s) and IOs (%s)"%(module_table, io_list))


    def create_input(self, name):
        if not name in self._d_io_list.keys():
            raise Exception("Unkown input %s"%name)
        return InputWrapper(self, name)


    def create_output(self, name):
        if not name in self._d_io_list.keys():
            raise Exception("Output \"%s\" not in list! %s"%(name,self._d_io_list.keys()))
        # create output            
        out = ValueOutput()
        # find redirection
        (alias, oname) = self._d_io_list[name].split(".",2)
        mod = self._d_module_table[alias]
        mout = getattr(mod, oname)
        # add my output as input to redirection
        mout += out
        return out


    def input_dispacher(self, name, value, kwargs=None):
        # find redirection
        (alias, iname) = self._d_io_list[name].split(".",2)
        mod = self._d_module_table[alias]
        mod_in = getattr(mod, iname)
        mod_in(value)
        
