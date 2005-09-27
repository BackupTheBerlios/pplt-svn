# ############################################################################ #
# This is part of the PPLT project. PPLT is a framework for industrial         # 
# communication.                                                               # 
# Copyright (C) 2003-2005 Hannes Matuschek <hmatuschek@gmx.net>                # 
#                                                                              # 
# This library is free software; you can redistribute it and/or                # 
# modify it under the terms of the GNU Lesser General Public                   # 
# License as published by the Free Software Foundation; either                 # 
# version 2.1 of the License, or (at your option) any later version.           # 
#                                                                              # 
# This library is distributed in the hope that it will be useful,              # 
# but WITHOUT ANY WARRANTY; without even the implied warranty of               # 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU             # 
# Lesser General Public License for more details.                              # 
#                                                                              # 
# You should have received a copy of the GNU Lesser General Public             # 
# License along with this library; if not, write to the Free Software          # 
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA    # 
# ############################################################################ # 

#ChangeLog:
# 2005-06-05:
#   * Fixed hidden root problem
# 2005-05-27:
#   Release as version 0.2.0 (alpha)

import wx;
import logging;
import sys;
import PPLT;
import os;


class DeviceSelectionDialog(wx.Dialog):
    def __init__(self, parent, PPLTSys):
        wx.Dialog.__init__(self, parent, -1, 
                            _("DeviceSelection"),
                            size = wx.Size(300,250));
        self.__PPLTSys = PPLTSys;
        
        sizer = wx.BoxSizer(wx.VERTICAL);

        self.__Tree = DeviceTree(self, PPLTSys);

        InitialHelpText = _("""Select a Device:
Above are all known devices are listed. Grouped by there class.
To see the content of a class please double-click the class.
To select a device, please double-click the device.
To see a short help-text for a device, single-click it.""")

        self.__Help = wx.TextCtrl(self, -1, size=(-1,70),style = wx.TE_MULTILINE);
        self.__Help.SetEditable(False);
        self.__Help.SetValue(InitialHelpText);

        sizer.Add(self.__Tree, 1, wx.ALIGN_CENTRE|wx.GROW, 3);
        sizer.Add(self.__Help, 0, wx.ALIGN_CENTRE|wx.GROW|wx.TOP, 3);

        box = wx.BoxSizer(wx.HORIZONTAL);
        ok = wx.Button(self, wx.ID_OK, "OK");
        ca = wx.Button(self, wx.ID_CANCEL, "Cancel");
        box.Add(ca, 1, wx.ALL|wx.ALIGN_LEFT, 3);
        box.Add(ok, 1, wx.ALL|wx.ALIGN_RIGHT, 3);
        sizer.Add(box, 0, wx.ALIGN_CENTER|wx.TOP|wx.GROW,5);

        self.SetSizer(sizer);
        self.SetAutoLayout(True);
        sizer.Fit(self.__Tree);

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelect, self.__Tree);
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnDClick, self.__Tree);
        self.Bind(wx.EVT_BUTTON, self.OnOK, id=wx.ID_OK);

        self.SelectedDevice = None;

    def OnSelect(self, event):
        item = event.GetItem();
        if not item:
            self.SelectedDevice = None;
            return(None);
        dat = self.__Tree.GetPyData(item);
        if dat:
            self.SelectedDevice = dat;
            self.__Help.Clear();
            info = self.__PPLTSys.GetDeviceInfo(dat);
            if info and info!="":
                txt = info.GetDescription();
                self.__Help.AppendText(txt);
        else: self.SelectedDevice = None;
        
    def OnDClick(self, event):
        item = event.GetItem();
        if item:
            dat = self.__Tree.GetPyData(item);
            if dat:
                self.SelectedDevice = dat;
                self.EndModal(wx.ID_OK);
                
    def OnOK(self, event):
        if self.SelectedDevice: self.EndModal(wx.ID_OK);




class DeviceTree(wx.TreeCtrl):
    def __init__(self, parent, PPLTSys):
        self.__PPLTSys = PPLTSys;
        styleflags = wx.TR_NO_LINES|wx.TR_HIDE_ROOT|wx.TR_TWIST_BUTTONS|wx.TR_HAS_BUTTONS;
#       if wx.Platform == "__WXMSW__":
#           styleflags = wx.TR_NO_LINES|wx.TR_HAS_BUTTONS;
            
        wx.TreeCtrl.__init__(self, parent, -1, style=styleflags);
    
        #store icons
        iconpath = PPLT.Config().GetBasePath()+"/icons";
        self.__IL = wx.ImageList(16,16);
        bmp = wx.Bitmap(os.path.normpath(iconpath+"/device.xpm"));
        if not bmp:
            bmp = wx.NullBitmap;
        self.__DevImg = self.__IL.Add(bmp);
        bmp = wx.Bitmap(os.path.normpath(iconpath+"/class.xpm"));
        if not bmp:
            bmp = wx.NullBitmap;
        self.__ClsImg = self.__IL.Add(bmp);
        self.SetImageList(self.__IL);
    
        self.__Root = self.AddRoot(_("Devices"));
#       self.SetPyData(self.__Root, None);

        self.__AddDevices(None, self.__Root);

    def __AddDevices(self, Class, PItem):
        classes = self.__PPLTSys.ListKnownDeviceClasses(Class);
        for cl in classes:
            item = self.AppendItem(PItem, cl);
            self.SetItemImage(item, self.__ClsImg, wx.TreeItemIcon_Normal);
            self.SetItemImage(item, self.__ClsImg, wx.TreeItemIcon_Expanded);
            self.SetPyData(item,None);
            if not Class:
                nclass = cl;
            else:
                nclass = "%s.%s"%(Class,cl);
            self.__AddDevices(nclass,item);
        devs = self.__PPLTSys.ListKnownDevices(Class);
        for dev in devs:
            item = self.AppendItem(PItem, dev);
            self.SetItemImage(item, self.__DevImg, wx.TreeItemIcon_Normal);
            self.SetItemImage(item, self.__DevImg, wx.TreeItemIcon_Normal);
            self.SetPyData(item, "%s.%s"%(Class,dev));

