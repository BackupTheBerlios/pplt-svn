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
#vim:set expandtab:set ts=4:set ai:
#ChangeLog:
#   2005-05-27:
#       Release as version 0.2.0 (alpha)

import wx;
import wx.wizard;
import PPLT;
from LoadBitmaps import LoadBitmaps;

class ReposDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, "Add repositority");



class ReposSelection(wx.wizard.WizardPageSimple):
    def __init__(self, parent):
        wx.wizard.WizardPageSimple.__init__(self,parent);
        Config = PPLT.Config();

	
        txt = "Select now the module repositority you want to use for Update or Install";
    
        vbox = wx.BoxSizer(wx.VERTICAL);

        label = wx.StaticText(self, -1, "Select Repositority");
        label.SetFont(wx.Font(18,wx.SWISS,wx.NORMAL, wx.BOLD))
        vbox.Add(label, 0, wx.ALIGN_CENTER|wx.ALL, 3);
        
        hline = wx.StaticLine(self, -1);
        vbox.Add(hline, 0, wx.EXPAND|wx.ALL,5);
        
        label = wx.StaticText(self, -1, txt);
        vbox.Add(label, 0, wx.ALL, 3);

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        rList = wx.ListCtrl(self, -1, size=(-1,100));
        rList.InsertColumn(0,"Repositority");
        hbox.Add(rList, 1, wx.ALL|wx.EXPAND , 3);
        box = wx.BoxSizer(wx.VERTICAL);
        addB = wx.Button(self, -1, "+", size=(30,30), style=wx.NO_BORDER);
        delB = wx.Button(self, -1, "-", size=(30,30), style=wx.NO_BORDER);
        box.Add(addB, 0, wx.ALL, 3);
        box.Add(delB, 0, wx.ALL, 3);
        hbox.Add(box, 0, wx.ALL|wx.ALIGN_CENTER, 3);
        vbox.Add(hbox,2, wx.BOTTOM|wx.EXPAND, 17);
       
        
        self.SetSizer(vbox)


class MainApp(wx.App):
    def OnInit(self):
        pix = LoadBitmaps(PPLT.Config().GetBasePath()+"/icons/");
        myWiz = wx.wizard.Wizard(None, -1, "Module (Un)Install/Update", pix.get("ModInstWiz"));
        page1 = ReposSelection(myWiz);
        
        myWiz.FitToPage(page1);
        myWiz.RunWizard(page1);
        return False;


app = MainApp(False);
app.MainLoop();

