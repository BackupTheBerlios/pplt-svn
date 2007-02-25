import wx
import sys
import xml.dom.minidom
import xml.xpath
from ListCtrl import eDevListCtrl
from ModuleEditorBasic import eDevModDescriptionListCtrl
from DescriptionDialog import eDevDescriptionDialog
from Tools import GetXMLContent
import Events

class eDevModuleListCtrl(eDevListCtrl):

    def __init__(self, parent, ID):
        eDevListCtrl.__init__(self, parent, ID,
                              wx.LC_REPORT|wx.LC_EDIT_LABELS|wx.LC_SINGLE_SEL,
                              ['Python Module'])
        
        self.setColumnWidth([wx.LIST_AUTOSIZE])
        self.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.onEndLabelEdit)

    def onEndLabelEdit(self, evt):
        if evt.IsEditCancelled() or evt.GetLabel() == "":
            evt.Veto()
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
        idx = self.InsertStringItem(sys.maxint, "")
        self.EnsureVisible(idx)
        self.EditLabel(idx) #FIXME idx != itemID ?
    
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
            pyname = self.GetItemText(item).strip()
            if pyname:
                node = dom.createElement("PyModule")
                tnode = dom.createTextNode(pyname)
                node.appendChild(tnode)
                node_list.append(node)
        return node_list



class eDevParameterListCtrl(eDevListCtrl):
    def __init__(self, parent, ID):
        eDevListCtrl.__init__(self, parent, ID,
                              wx.LC_REPORT|wx.LC_EDIT_LABELS|wx.LC_SINGLE_SEL,
                              ["Name", "Default", "Descriptions"])
        
        self.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT, self.onStartEditLabel)
        self.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.onEndEditLabel)
        
        self.setColumnWidth([120,80,wx.LIST_AUTOSIZE])

    def onStartEditLabel(self, evt):
        if evt.GetColumn() == 2:
            evt.Veto()
            dlg = eDevDescriptionDialog(self, -1, "Edit description of Parameter %s"%self.GetItemText(evt.GetIndex()),
                                    self.getItemData(evt.GetIndex()))
            if wx.ID_OK == dlg.ShowModal():
                descs = dlg.getDescriptions()
                self.setItemData(evt.GetIndex(), descs)
                self.SetStringItem(evt.GetIndex(), 2, ", ".join(descs.keys()))
                event = Events.ModifiedEvent(Events._event_modified, self.GetId())
                self.GetEventHandler().ProcessEvent(event)
            dlg.Destroy()
        else: evt.Skip()

    def onEndEditLabel(self, evt):
        if evt.IsEditCancelled() or evt.GetLabel() == "":
            evt.Veto()
            return
        if evt.GetColumn() != 0:
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
        idx = self.InsertStringItem(sys.maxint, "")
        self.SetStringItem(idx, 1, "")
        self.SetStringItem(idx, 2, "")
        self.setItemData(idx, dict())
        self.EnsureVisible(idx)
        self.EditLabel(idx) #FIXME idx != itemID

    def DelSelected(self):
        if self.selectedItem < 0: return
        self.DeleteItem(self.selectedItem)
        self.selectedItem = -1
        self.delItemData(self.selectedItem)

    def ToXML(self, dom):
        node_list = []
        item = -1
        while 1:
            item = self.GetNextItem(item, wx.LIST_NEXT_BELOW)
            if item == -1: break
            name = self.GetItemText(item).strip()
            ditem = self.GetItem(item,1)
            descs = self.getItemData(item)
            default = ditem.GetText().strip()
            if not name: continue
            para = dom.createElement("Parameter")
            para.setAttribute("name",name)
            if default: para.setAttribute("default",default)
            for (lang, txt) in descs.items():
                if not lang.strip() or not txt.strip(): continue
                desc = dom.createElement("Description")
                desc.setAttribute("lang",lang)
                tnode = dom.createTextNode(txt)
                desc.appendChild(tnode)
                para.appendChild(desc)
            node_list.append(para)
        return node_list




class eDevModuleEditorRequire(wx.Panel):

    def __init__(self, parent, ID, xml_dom):
        wx.Panel.__init__(self, parent, ID)
        self._d_dom = xml_dom
        self._d_static_box = wx.StaticBox(self, -1, "Requirements")
        self._new_bmp = wx.ArtProvider_GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, (16,16))
        self._del_bmp = wx.ArtProvider_GetBitmap(wx.ART_DELETE, wx.ART_TOOLBAR, (16,16))
        
        box = wx.StaticBoxSizer(self._d_static_box, wx.VERTICAL)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        desc_label = wx.StaticText(self, -1, "Reqiured Python Modules")
        hbox.Add(desc_label,1, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.TOP)
        self._del_mod = wx.BitmapButton(self, -1, self._del_bmp, style=wx.NO_BORDER)
        hbox.Add(self._del_mod,0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        self._add_mod = wx.BitmapButton(self, -1, self._new_bmp, style=wx.NO_BORDER)
        hbox.Add(self._add_mod, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        self.Bind(wx.EVT_BUTTON, self.OnDelModule, self._del_mod)
        self.Bind(wx.EVT_BUTTON, self.OnAddModule, self._add_mod)
        self.Bind(wx.EVT_BUTTON, self.OnModified, self._del_mod)
        self.Bind(wx.EVT_BUTTON, self.OnModified, self._add_mod)
        box.Add(hbox, 0, wx.LEFT|wx.TOP|wx.RIGHT|wx.ALIGN_LEFT|wx.EXPAND, 5)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self._py_list = eDevModuleListCtrl(self, -1)
        mods = xml.xpath.Evaluate("/Module/Requires/PyModule", self._d_dom)
        for mod in mods:
            name = GetXMLContent(mod)
            self._py_list.InsertStringItem(sys.maxint, name)
        self.Bind(Events.EVT_MODIFIED, self.OnModified, self._py_list)
        hbox.Add(self._py_list, 1, wx.ALIGN_CENTER|wx.EXPAND|wx.LEFT,5)
        box.Add(hbox, 0, wx.LEFT|wx.BOTTOM|wx.RIGHT|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        desc_label = wx.StaticText(self, -1, "Parameters")
        hbox.Add(desc_label,1, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.TOP,5)
        self._del_param = wx.BitmapButton(self, -1, self._del_bmp, style=wx.NO_BORDER)
        hbox.Add(self._del_param,0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        self._add_param = wx.BitmapButton(self, -1, self._new_bmp, style=wx.NO_BORDER)
        hbox.Add(self._add_param, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        self.Bind(wx.EVT_BUTTON, self.onDelParam, self._del_param)
        self.Bind(wx.EVT_BUTTON, self.OnModified, self._del_param)
        self.Bind(wx.EVT_BUTTON, self.onAddParam, self._add_param)
        self.Bind(wx.EVT_BUTTON, self.OnModified, self._add_param)
        box.Add(hbox, 0, wx.LEFT|wx.TOP|wx.RIGHT|wx.ALIGN_LEFT|wx.EXPAND, 5)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self._para_list = eDevParameterListCtrl(self, -1)
        params = xml.xpath.Evaluate("/Module/Requires/Parameter", self._d_dom)
        for param in params:
            name = param.getAttribute("name")
            default = param.getAttribute("default")
            descs = xml.xpath.Evaluate("/Module/Requires/Parameter[@name='%s']/Description"%name, self._d_dom)
            desc_list = {}
            for desc in descs:
                lang = desc.getAttribute('lang')
                txt  = GetXMLContent(desc)
                desc_list[lang] = txt
            idx = self._para_list.InsertStringItem(sys.maxint, name)
            self._para_list.SetStringItem(idx, 1, default)
            self._para_list.SetStringItem(idx, 2, ", ".join(desc_list.keys()))
            self._para_list.setItemData(idx, desc_list)
        self.Bind(Events.EVT_MODIFIED, self.OnModified, self._para_list)
        hbox.Add(self._para_list, 1, wx.ALIGN_CENTER|wx.EXPAND|wx.LEFT,5)
        box.Add(hbox, 0, wx.LEFT|wx.BOTTOM|wx.RIGHT|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5)
        

        self.SetSizer(box)

    def OnDelModule(self, evt):
        self._py_list.DeleteSelected()
    def OnAddModule(self, evt):
        self._py_list.AddNew()
    def onDelParam(self, evt):
        self._para_list.DelSelected()
    def onAddParam(self, evt):
        self._para_list.AddNew()


    def OnModified(self, event):
        #print "REQUIRES: emmit Modified event!"
        evt = Events.ModifiedEvent(Events._event_modified, self.GetId())
        self.GetEventHandler().ProcessEvent(evt)
        event.Skip()


    def ToXML(self, dom):
        req = dom.createElement("Require")

        node_list = self._py_list.ToXML(dom)
        node_list += self._para_list.ToXML(dom)
        for node in node_list: req.appendChild(node)
        return [req]
