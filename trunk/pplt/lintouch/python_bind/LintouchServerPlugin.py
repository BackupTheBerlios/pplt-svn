""" This class defines the lsp class which represents the lintouch server 
    plugin. The user have to override the run() method to provide the server 
    behavior. Several methods and attributes defines the interface to
    lintouch. """

    
class LintouchServerPlugin:
    _d_plugin   = None
    _d_varset   = None

    def __init__(self, varset, plugin):
        """ This constructor can be overridden, but this constructor should 
            allways be called! The parameter varset specifies the variable 
            table for the plugin. This is a string->variable map. The plugin 
            specifies an instance of lsp_core_plugin a wrapper to the C struct
            of a lsp "class". """
        self._d_plugin = plugin
        self._d_varset = varset

    def run(self):
        """ This method should be overridden to implement the server-script. 
            this method should never return unless the self.should_run() 
            method returns false. """
        pass

    def should_run():
        """ This method will return True unless the plugin is unloaded! """
        pass
                


