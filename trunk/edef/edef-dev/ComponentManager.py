import edef

class ComponentManager:
    
    __metaclass__ = edef.Singleton
    def __init__(self):
        # FIXME find components
        # FIXME init components
        self._components = dict()

        from edef.dev.pyeditor import component as pyEditComponent
        from edef.dev.modeditor import component as modEditComponent
        from edef.dev.circuit import component as circEditComponent
        from edef.dev.eventmanager import component as evtManagerComponent

        self.initComponent("pyeditor", pyEditComponent )
        self.initComponent("modeditor", modEditComponent )
        self.initComponent("circuit", circEditComponent )
        self.initComponent("eventmanager", evtManagerComponent )

    def getComponent(self, name):
        return self._components[name]

    def initComponent(self, name, cls):
        if name in self._components: return
        self._components[name] = cls()



