

class eDevEditorInterface:
    _d_is_modified = False
    _d_uri = None
    
    def __init__(self, parent, is_modified=False, uri=None):
        self._d_is_modified = is_modified
        self._d_uri = uri
        self._parent = parent
        self._title = "TITLE"

    def isModified(self): return self._d_is_modified
    def setModified(self, state=True): self._d_is_modified = state

    def getURI(self): return self._d_uri
    def setURI(self, uri): self._d_uri = uri

    def setTitle(self, title):
        self._title = title
        self._parent.setPageTitleByURI(self.getURI(), title)

    def getTitle(self):
        return self._title
