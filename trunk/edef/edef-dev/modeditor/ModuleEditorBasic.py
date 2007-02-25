import sys
import wx
import xml.dom.minidom
import xml.xpath
from ListCtrl import eDevListCtrl
from Model import eDevModel
from Tools import GetXMLContent
import Events
import Tools

class eDevModDescriptionListCtrl(eDevListCtrl):
    
    def __init__(self, parent, ID):
        eDevListCtrl.__init__(self, parent, ID,
                              wx.LC_REPORT|wx.LC_EDIT_LABELS|wx.LC_SINGLE_SEL,
                              ["Lang","Description"])

        self.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.onEndEditLabel)


    def onEndEditLabel(self, evt):
        if evt.IsEditCancelled() or evt.GetLabel() == "":
            evt.Veto()
            return
        
        if not evt.GetColumn() == 0:
            evt.Skip()
            return

        item = -1
        while 1:
            item = self.GetNextItem(item, wx.LIST_NEXT_BELOW)
            if item == -1: break
            if self.GetItemText(item) == evt.GetLabel():
                evt.Veto()
                return
        evt.Skip()

    
    def AddNew(self):
        idx = self.InsertStringItem(sys.maxint, " ")
        self.SetStringItem(idx, 1, " ")
        self.EnsureVisible(idx)
        self.EditLabel(idx) #FIXME idx != itemID

    
    def DeleteSelected(self):
        if self.selectedItem<0: return
        self.DeleteItem(self.selectedItem)
        self.selectedItem = -1

    def ToXML(self, dom):
        node_list = []
        item = -1
        while 1:
            item = self.GetNextItem(item, wx.LIST_NEXT_BELOW)
            if item == -1: break
            lang = self.GetItemText(item).strip()
            titem = self.GetItem(item, 1)
            text = titem.GetText().strip()
            dec = dom.createElement("Description")
            dec.setAttribute("lang", lang)
            txt = dom.createTextNode(text)
            dec.appendChild(txt)
            node_list.append(dec)
        return node_list

class eDevModuleEditorBasic(wx.Panel):
    def __init__(self, parent, ID, dom):
        """ This Widget will emmit an "eDev_EVT_MODIFIED" event if one of the inputs are
            modified. """
        wx.Panel.__init__(self, parent, ID)
        
        self._d_dom = dom
        self._d_model = eDevModel()
        
        self._d_static_box = wx.StaticBox(self, ID, "BasicData")
        
        self._new_bmp = wx.ArtProvider_GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, (16,16))
        self._del_bmp = wx.ArtProvider_GetBitmap(wx.ART_DELETE, wx.ART_TOOLBAR, (16,16))
        
        box = wx.StaticBoxSizer(self._d_static_box, wx.VERTICAL)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        au_label = wx.StaticText(self, -1, "Author", style=wx.ALIGN_RIGHT)
        hbox.Add(au_label,1, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 3)
        author = xml.xpath.Evaluate("string(/Module/Author)",self._d_dom)
        if author: author = author.strip()
        else: author = ""
        self._author = wx.TextCtrl(self, -1, author)
        self.Bind(wx.EVT_TEXT, self.OnModified, self._author)
        hbox.Add(self._author, 5, wx.ALIGN_CENTER|wx.RIGHT, 5)
        
        ver_label = wx.StaticText(self, -1, "Version", style=wx.ALIGN_RIGHT)
        hbox.Add(ver_label, 1, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 3)
        version = xml.xpath.Evaluate("string(/Module/Version)", self._d_dom).strip()
        self._version = wx.TextCtrl(self, -1, version)
        self.Bind(wx.EVT_TEXT, self.OnModified, self._version)
        hbox.Add(self._version, 5, wx.ALIGN_CENTER)
        box.Add(hbox,0,wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND,5)
 
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        zip_label = wx.StaticText(self, -1, "Archive", style=wx.ALIGN_RIGHT)
        hbox.Add(zip_label,1, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 3)
        archives = self._d_model.openURI("zip://")
        for i in range(len(archives)):
            (proto, archives[i]) = Tools.splitURI(archives[i])
        archive = xml.xpath.Evaluate("string(/Module/Archive)", self._d_dom).strip()
        if not archive in archives: archives.append(archive)
        self._archive = wx.ComboBox(self, -1, archive, choices=archives)
        self.Bind(wx.EVT_TEXT, self.OnModified, self._archive)
        hbox.Add(self._archive, 5, wx.ALIGN_CENTER|wx.RIGHT, 5)
        
        class_label = wx.StaticText(self, -1, "Class", style=wx.ALIGN_RIGHT)
        hbox.Add(class_label, 1, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 3)
        classname = xml.xpath.Evaluate("string(/Module/Class)",self._d_dom).strip()
        self._class = wx.TextCtrl(self, -1, classname)
        self.Bind(wx.EVT_TEXT, self.OnModified, self._class)
        hbox.Add(self._class, 5, wx.ALIGN_CENTER)
        box.Add(hbox,0,wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5)
      
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        desc_label = wx.StaticText(self, -1, "Module description(s)")
        hbox.Add(desc_label,1, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.TOP,5)
        self._del_descr = wx.BitmapButton(self, -1, self._del_bmp, style=wx.NO_BORDER)
        hbox.Add(self._del_descr,0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        self._add_descr = wx.BitmapButton(self, -1, self._new_bmp, style=wx.NO_BORDER)
        hbox.Add(self._add_descr,0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        box.Add(hbox, 0, wx.LEFT|wx.TOP|wx.RIGHT|wx.ALIGN_LEFT|wx.EXPAND, 5)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self._desc_list = eDevModDescriptionListCtrl(self, -1)
        descs = xml.xpath.Evaluate("/Module/Description", self._d_dom)
        for desc in descs:
            lang = desc.getAttribute("lang")
            txt = GetXMLContent(desc)
            idx  =  self._desc_list.InsertStringItem(sys.maxint, lang)
            self._desc_list.SetStringItem(idx, 1, txt)
        self._desc_list.setColumnWidth([50,wx.LIST_AUTOSIZE])
        self.Bind(Events.EVT_MODIFIED, self.OnModified, self._desc_list)
        hbox.Add(self._desc_list, 1, wx.ALIGN_CENTER|wx.EXPAND|wx.LEFT,5)
        box.Add(hbox, 0, wx.LEFT|wx.BOTTOM|wx.RIGHT|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5)
        
        self.Bind(wx.EVT_BUTTON, self.OnAddDescription, self._add_descr)
        self.Bind(wx.EVT_BUTTON, self.OnDelDescription, self._del_descr)
        self.Bind(wx.EVT_BUTTON, self.OnModified, self._add_descr)
        self.Bind(wx.EVT_BUTTON, self.OnModified, self._del_descr)
        self.SetSizer(box)

    def OnAddDescription(self, evt):
        self._desc_list.AddNew()
        evt.Skip()
    
    def OnDelDescription(self, evt):
        self._desc_list.DeleteSelected()
        evt.Skip()

    def OnModified(self, event):
        #print "BASIC: emmit Modified event!"
        evt = Events.ModifiedEvent(Events._event_modified, self.GetId())
        self.GetEventHandler().ProcessEvent(evt)
        event.Skip()

    
    def ToXML(self, mod):
        #save Author:
        node_list = []
        author = self._author.GetValue()
        if author.strip() != "":
            elm = mod.createElement("Author")
            txt = mod.createTextNode(author.strip())
            elm.appendChild(txt)
            node_list.append(elm)
        
        #save Version:
        version = self._version.GetValue()
        elm = mod.createElement("Version")
        txt = mod.createTextNode(version.strip())
        elm.appendChild(txt)
        node_list.append(elm)
        
        #save Archive:
        archive = self._archive.GetValue()
        elm = mod.createElement("Archive")
        txt = mod.createTextNode(archive.strip())
        elm.appendChild(txt)
        node_list.append(elm)

        #save Class
        cls = self._class.GetValue()
        elm = mod.createElement("Class")
        txt = mod.createTextNode(cls.strip())
        elm.appendChild(txt)
        node_list.append(elm)
        #save descriptions:
        node_list += self._desc_list.ToXML(mod)
        
        return node_list
