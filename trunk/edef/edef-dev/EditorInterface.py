

class eDevEditorInterface:
    _d_is_modified = False
    _d_uri = None
    
    def __init__(self, is_modified=False, uri=None):
        self._d_is_modified = is_modified
        self._d_uri = uri

    def isModified(self): return self._d_is_modified
    def setModified(self, state=True): self._d_is_modified = state

    def getURI(self): return self._d_uri
    def setURI(self, uri): self._d_uri = uri

