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
#   2005-05-27:
#       Release as version 0.2.0 (alpha)

import wx;
import logging;
import sys;
import string;
from DeviceSelectionDialog import DeviceSelectionDialog;
from DeviceParameterDialog import DeviceParameterDialog;
import PPLT;
import os;
import Messages;

class DevicePanel(wx.ListCtrl):
    def __init__(self, parent, PPLTSys):
        wx.ListCtrl.__init__(self, parent, -1,
                                style=wx.LC_REPORT|
                                        wx.LC_HRULES|
                                        wx.BORDER_SUNKEN|
                                        wx.LC_SINGLE_SEL);
        conf = PPLT.Config();

        self.__PPLTSys = PPLTSys;
        self.__Logger = logging.getLogger("PPLT");
        self.Fit();
        self.InsertColumn(0,_("Alias"));
        self.InsertColumn(1,_("FQDN"),width=200);
        self.InsertColumn(2,_("Parameter"),width=300);

        self.__IL = wx.ImageList(16,16);
        bmp = wx.Bitmap(os.path.normpath(conf.GetBasePath()+"/icons/device.xpm"));
        if not bmp:
            bmp = wx.NullBitmap;
        self.__DevImg = self.__IL.Add(bmp);
        self.SetImageList(self.__IL, wx.IMAGE_LIST_SMALL);

        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick);

        self.Build();


    def Build(self):
        #self.ClearAll();
        devlst = self.__PPLTSys.ListDevices();
        for dev in devlst:
            fqdn = self.__PPLTSys.GetFQDeviceName(dev);
            para = self.__PPLTSys.GetDeviceParameters(dev);
            index = self.InsertImageStringItem(sys.maxint, dev, self.__DevImg);
            self.SetStringItem(index, 1, fqdn);
            self.SetStringItem(index, 2, ParaToString(para));

    def Clean(self):
        self.DeleteAllItems();

    def OnAddDevice(self, event):
        self.__Logger.debug(_("Add device..."));
        ret = LoadADevice(self, self.__PPLTSys);
        if ret:
            (Alias, DevName, Paras) = ret;
            index = self.InsertImageStringItem(sys.maxint, Alias,self.__DevImg);
            self.SetStringItem(index, 1, DevName);
            self.SetStringItem(index, 2, Paras);
    
    def OnDelDevice(self,event):
        item = self.GetFocusedItem();
        alias = self.GetItemText(item);
        try: self.__PPLTSys.UnLoadDevice(alias);
        except Exception,e:
            err = _("Unable to unload device %s.\n Message: %s")%(alias, str(e));
            Messages.ErrorMessage(self, err, _("Unable to unload device."));
            return;
        self.DeleteItem(item);

    def OnRightClick(self, event):
        pt = event.GetPosition();
        (item, flag) = self.HitTest(pt);
        if item == -1:
            menu = DeviceMenu(self);
            self.PopupMenu(menu,pt);
            menu.Destroy();
        else:
            self.Select(item);
            menu = DeviceCtxMenu(self);
            self.PopupMenu(menu,pt);
            menu.Destroy();
    

def LoadADevice(parent, PPLTSys):
    dlg = DeviceSelectionDialog(parent, PPLTSys);
    ret = dlg.ShowModal();
    if ret != wx.ID_OK: return(None);
    DevName = dlg.SelectedDevice;
    dlg.Destroy();
    #print "Selected Device: %s"%DevName;
    
    dlg = DeviceParameterDialog(parent, DevName, PPLTSys);
    ret = dlg.ShowModal();
    if not ret == wx.ID_OK: return(None);
    Alias = dlg.Alias.GetValue();
    Vals  = dlg.Values;
    dlg.Destroy();

    #print "%s as %s : %s"%(DevName, Alias, str(vals))
    try:PPLTSys.LoadDevice(DevName, Alias, Vals);
    except Exception, e:
        err = _("Error while load device %s.\n Message: %s")%(DevName,str(e));
        Messages.ErrorMessage(parent, err, _("Unable to load device."));
        return None;
    return( (Alias, DevName, ParaToString(Vals)) );


def ParaToString(para):
    keys = para.keys();
    keys.sort();
    lst = [];
    for key in keys: lst.append("%s=%s"%(key,para[key]));
    return(string.join(lst, ", "));


class DeviceMenu(wx.Menu):
    def __init__(self, parent):
        self.__ADD_ID = wx.NewId();
        wx.Menu.__init__(self);
        item = wx.MenuItem(self, self.__ADD_ID, _("Add Device"));
        self.AppendItem(item);
        self.Bind(wx.EVT_MENU, parent.OnAddDevice, id=self.__ADD_ID);

class DeviceCtxMenu(wx.Menu):
    def __init__(self, parent):
        self.__DEL_ID = wx.NewId();
        wx.Menu.__init__(self);
        item = wx.MenuItem(self, self.__DEL_ID, _("Del Device"));
        self.AppendItem(item);
        self.Bind(wx.EVT_MENU, parent.OnDelDevice, id=self.__DEL_ID);

