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
from ModusBox import ModusBox;


class SetPropertyDialog(wx.Dialog):
    def __init__(self, parent, PPLTSys, owner, group, modus):
        wx.Dialog.__init__(self, parent, -1, _("Properties"));
        
        sizer = wx.BoxSizer(wx.VERTICAL);
        
        self.__modbox = ModusBox(self, PPLTSys, owner, group, modus);
        sizer.Add(self.__modbox, 0, wx.EXPAND|wx.ALL, 3);
        
        ok = wx.Button(self, wx.ID_OK, _("OK"));
        ca = wx.Button(self, wx.ID_CANCEL, _("Cancel"));
        box = wx.BoxSizer(wx.HORIZONTAL);
        box.Add(ca, 1, wx.ALL|wx.ALIGN_LEFT, 3);
        box.Add(ok, 1, wx.ALL|wx.ALIGN_RIGHT, 3);
        sizer.Add(box, 1, wx.GROW|wx.ALIGN_CENTER);

        self.Bind(wx.EVT_KEY_UP, self.OnKey);

        self.SetSizer(sizer);
        sizer.Fit(self);

    def OnOK(self, event):
        self.EndModal(wx.ID_OK);

    def OnKey(self, event):
        if event.GetKeyCode() == wx.WXK_RETURN:
            self.EndModal(wx.ID_OK);
        elif event.GetKeyCode() == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_CANCEL);

    def GetModus(self):
        return("%o"%self.__modbox.GetModus());
    def GetName(self):
        return(self.Name.GetValue());
    def GetOwner(self):
        return(self.__modbox.Owner.GetValue());
    def GetGroup(self):
        return(self.__modbox.Group.GetValue());



