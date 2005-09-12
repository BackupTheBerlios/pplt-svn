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
        vbox.Add(label, 0);

        self.SetSizer(vbox)        

class MainApp(wx.App):
    def OnInit(self):
        myWiz = wx.wizard.Wizard(None, -1, "Module (Un)Install/Update");
        page1 = ReposSelection(myWiz);
        myWiz.RunWizard(page1);
        self.ExitMainLoop();
        return False;


app = MainApp(False);
app.MainLoop();

