import sys
import wx
import xml.dom.minidom
import xml.xpath
from ListCtrl import eDevListCtrl
from DescriptionDialog import eDevDescriptionDialog
from edef.dev.Tools import GetXMLContent
from edef.dev import Events

class eDevInputListCtrl(eDevListCtrl):
    def __init__(self, parent, ID):
        eDevListCtrl.__init__(self, parent, ID,
                              wx.LC_REPORT|wx.LC_EDIT_LABELS|wx.LC_SINGLE_SEL,
                              ["Name", "Type", "Pattern", "Descriptions"])

        self.setColumnWidth([120,50,100,wx.LIST_AUTOSIZE])
        
        self.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT, self.onStartEditLabel)
        self.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.onEndEditLabel)


    def onStartEditLabel(self, evt):
        if evt.GetColumn() == 3:
            evt.Veto()
            dlg = eDevDescriptionDialog(self, -1, "Edit description of input %s"%self.GetItemText(evt.GetIndex()),
                                    self.getItemData(evt.GetIndex()))
            if wx.ID_OK == dlg.ShowModal():
                descs = dlg.getDescriptions()
                self.setItemData(evt.GetIndex(), descs)
                self.SetStringItem(evt.GetIndex(), 3, ", ".join(descs.keys()))
                event = Events.ModifiedEvent(Events._event_modified, self.GetId())
                self.GetEventHandler().ProcessEvent(event)
            dlg.Destroy()
        else: evt.Skip()


    def onEndEditLabel(self, evt):
        if evt.IsEditCancelled():
            evt.Veto()
            return
        if evt.GetLabel() == "" and evt.GetColumn() == 0:
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
        self.SetStringItem(idx, 3, "")
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
            if not name: continue
            typ  = self.GetItem(item,1).GetText().strip()
            pat  = self.GetItem(item,2).GetText().strip()
            descs = self.getItemData(item)
            
            inp = dom.createElement("Input")
            inp.setAttribute("name",name)
            if typ: inp.setAttribute("type",typ)
            if pat: inp.setAttribute("pattern",pat)
            for (lang, txt) in descs.items():
                if not lang.strip() or not txt.strip(): continue
                desc = dom.createElement("Description")
                desc.setAttribute("lang",lang)
                tnode = dom.createTextNode(txt)
                desc.appendChild(tnode)
                inp.appendChild(desc)
            node_list.append(inp)
        return node_list



class eDevOutputListCtrl(eDevInputListCtrl):
    def onStartEditLabel(self, evt):
        if evt.GetColumn() == 3:
            evt.Veto()
            dlg = eDevDescriptionDialog(self, -1, "Edit description of output %s"%self.GetItemText(evt.GetIndex()),
                                    self.getItemData(evt.GetIndex()))
            if wx.ID_OK == dlg.ShowModal():
                descs = dlg.getDescriptions()
                self.setItemData(evt.GetIndex(), descs)
                self.SetStringItem(evt.GetIndex(), 3, ", ".join(descs.keys()))
                event = Events.ModifiedEvent(Events._event_modified, self.GetId())
                self.GetEventHandler().ProcessEvent(event)
            dlg.Destroy()
        else: evt.Skip()


    def ToXML(self, dom):
        node_list = []
        item = -1
        while 1:
            item = self.GetNextItem(item, wx.LIST_NEXT_BELOW)
            if item == -1: break
            name = self.GetItemText(item).strip()
            if not name: continue
            typ  = self.GetItem(item,1).GetText().strip()
            pat  = self.GetItem(item,2).GetText().strip()
            descs = self.getItemData(item)
            
            out = dom.createElement("Output")
            out.setAttribute("name",name)
            if typ: out.setAttribute("type",typ)
            if pat: out.setAttribute("pattern",pat)
            for (lang, txt) in descs.items():
                if not lang.strip() or not txt.strip(): continue
                desc = dom.createElement("Description")
                desc.setAttribute("lang",lang)
                tnode = dom.createTextNode(txt)
                desc.appendChild(tnode)
                out.appendChild(desc)
            node_list.append(out)
        return node_list



class eDevModuleEditorProvide(wx.Panel):

    def __init__(self, parent, ID, xml_dom):
        wx.Panel.__init__(self, parent, ID)
        self._d_dom = xml_dom
        self._d_static_box = wx.StaticBox(self, -1, "Input/Output")
        self._new_bmp = wx.ArtProvider_GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, (16,16))
        self._del_bmp = wx.ArtProvider_GetBitmap(wx.ART_DELETE, wx.ART_TOOLBAR, (16,16))
        
        box = wx.StaticBoxSizer(self._d_static_box, wx.VERTICAL)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        desc_label = wx.StaticText(self, -1, "Inputs")
        hbox.Add(desc_label,1, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.TOP)
        self._del_in = wx.BitmapButton(self, -1, self._del_bmp, style=wx.NO_BORDER)
        hbox.Add(self._del_in, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        self._add_in = wx.BitmapButton(self, -1, self._new_bmp, style=wx.NO_BORDER)
        hbox.Add(self._add_in, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        self.Bind(wx.EVT_BUTTON, self.OnAddInput, self._add_in)
        self.Bind(wx.EVT_BUTTON, self.OnModified, self._add_in)
        self.Bind(wx.EVT_BUTTON, self.OnDelInput, self._del_in)
        self.Bind(wx.EVT_BUTTON, self.OnModified, self._del_in)
        box.Add(hbox, 0, wx.LEFT|wx.TOP|wx.RIGHT|wx.ALIGN_LEFT|wx.EXPAND, 5)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self._in_list = eDevInputListCtrl(self, -1)
        inps = xml.xpath.Evaluate("/Module/Provides/Input", self._d_dom);
        for inp in inps:
            name = inp.getAttribute("name")
            typ  = inp.getAttribute("type")
            pat  = inp.getAttribute("pattern")
            descs = xml.xpath.Evaluate("/Module/Provides/Input[@name='%s']/Description"%name, self._d_dom)
            desc_list = {}
            for desc in descs:
                lang = desc.getAttribute("lang")
                txt  = GetXMLContent(desc)
                desc_list[lang] = txt
            idx = self._in_list.InsertStringItem(sys.maxint, name)
            self._in_list.SetStringItem(idx, 1, typ)
            self._in_list.SetStringItem(idx, 2, pat)
            self._in_list.SetStringItem(idx, 3, ", ".join(desc_list.keys()))
            self._in_list.setItemData(idx, desc_list)
        self.Bind(Events.EVT_MODIFIED, self.OnModified, self._in_list)
        hbox.Add(self._in_list, 1, wx.ALIGN_CENTER|wx.EXPAND|wx.LEFT,5)
        box.Add(hbox, 0, wx.LEFT|wx.BOTTOM|wx.RIGHT|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        desc_label = wx.StaticText(self, -1, "Outputs")
        hbox.Add(desc_label,1, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.TOP,5)
        self._del_out = wx.BitmapButton(self, -1, self._del_bmp, style=wx.NO_BORDER)
        hbox.Add(self._del_out, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        self._add_out = wx.BitmapButton(self, -1, self._new_bmp, style=wx.NO_BORDER)
        hbox.Add(self._add_out, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        self.Bind(wx.EVT_BUTTON, self.OnDelOut, self._del_out)
        self.Bind(wx.EVT_BUTTON, self.OnModified, self._del_out)
        self.Bind(wx.EVT_BUTTON, self.OnAddOut, self._add_out)
        self.Bind(wx.EVT_BUTTON, self.OnModified, self._add_out)
        box.Add(hbox, 0, wx.LEFT|wx.TOP|wx.RIGHT|wx.ALIGN_LEFT|wx.EXPAND, 5)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self._out_list = eDevOutputListCtrl(self, -1)
        outs = xml.xpath.Evaluate("/Module/Provides/Output", self._d_dom);
        for out in outs:
            name = out.getAttribute("name")
            typ  = out.getAttribute("type")
            pat  = out.getAttribute("pattern")
            descs = xml.xpath.Evaluate("/Module/Provides/Output[@name='%s']/Description"%name, self._d_dom)
            desc_list = {}
            for desc in descs:
                lang = desc.getAttribute("lang")
                txt  = GetXMLContent(desc)
                desc_list[lang] = txt
            idx = self._out_list.InsertStringItem(sys.maxint, name)
            self._out_list.SetStringItem(idx, 1, typ)
            self._out_list.SetStringItem(idx, 2, pat)
            self._out_list.SetStringItem(idx, 3, ", ".join(desc_list.keys()))
            self._out_list.setItemData(idx, desc_list)
        self.Bind(Events.EVT_MODIFIED, self.OnModified, self._out_list)
        hbox.Add(self._out_list, 1, wx.ALIGN_CENTER|wx.EXPAND|wx.LEFT,5)
        box.Add(hbox, 0, wx.LEFT|wx.BOTTOM|wx.RIGHT|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5)

        self.SetSizer(box)


    def OnDelInput(self, evt):
        self._in_list.DelSelected()
    def OnAddInput(self, evt):
        self._in_list.AddNew()
    def OnDelOut(self, evt):
        self._out_list.DelSelected()
    def OnAddOut(self, evt):
        self._out_list.AddNew()

    def OnModified(self, event):
        #print "PROVIDES: emmit Modified event!"
        evt = Events.ModifiedEvent(Events._event_modified, self.GetId())
        self.GetEventHandler().ProcessEvent(evt)
        event.Skip()


    def ToXML(self, dom):
        pro = dom.createElement("Provides")

        node_list = self._in_list.ToXML(dom)
        node_list += self._out_list.ToXML(dom)

        for node in node_list: pro.appendChild(node)
        return [pro]
