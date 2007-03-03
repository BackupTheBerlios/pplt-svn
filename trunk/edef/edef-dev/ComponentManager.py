import edef

class ComponentManager:
    
    __metaclass__ = edef.Singleton
    def __init__(self):
        # FIXME find components
        # FIXME init components
        self._components = dict()

        from edef.dev.pyeditor import component as pyEditComponent
        from edef.dev.modeditor import component as modEditComponent
        self.initComponent("pyeditor", pyEditComponent )
        self.initComponent("modeditor", modEditComponent )

    def getComponent(self, name):
        return self._components[name]

    def initComponent(self, name, cls):
        if name in self._components: return
        self._components[name] = cls()



