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
#	2005-05-27:
#		Release as version 0.2.0 (alpha)

import wx;
import ServerPanel;
import DevicePanel;
import SymbolTreePanel;
import UserDBPanel;

class NoteBook(wx.Notebook):
	def __init__(self, parent, ID, PPLTSys):
		wx.Notebook.__init__(self, parent, ID);
		self.__PPLTSys = PPLTSys;
		
		self.__SrvPanel = ServerPanel.ServerPanel(self, self.__PPLTSys);
		self.__DevPanel = DevicePanel.DevicePanel(self, self.__PPLTSys);
		self.__SymPanel = SymbolTreePanel.SymbolTreePanel(self, self.__PPLTSys);
		self.__UDBPanel = UserDBPanel.UserDBPanel(self, self.__PPLTSys);

		self.AddPage(self.__DevPanel, _("Devices"));
		self.AddPage(self.__SymPanel, _("SymbolTree"));
		self.AddPage(self.__SrvPanel, _("Server"));
		self.AddPage(self.__UDBPanel, _("User DataBase"));

		self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick);

	def OnRightClick(self,event):
		pt = event.GetPosition();
		(tab, flag) = self.HitTest(pt);
		if tab >= 0:
			self.SetSelection(tab);
		if tab == 0:
			menu = DevicePanel.DeviceMenu(self.__DevPanel);
			self.PopupMenu(menu, pt);
			menu.Destroy();
		elif tab == 1:
			self.__SymPanel.Unselect();
			menu = SymbolTreePanel.CtxMenu(self.__SymPanel);
			self.PopupMenu(menu,pt);
			menu.Destroy();
		elif tab == 2:
			menu = ServerPanel.ServerMenu(self.__SrvPanel);
			self.PopupMenu(menu,pt);
			menu.Destroy();
		elif tab == 3:
			self.__UDBPanel.Unselect();
			menu = UserDBPanel.CtxMenu(self.__UDBPanel, None);
			self.PopupMenu(menu,pt);
			menu.Destroy();

	def Clean(self):
		self.__SrvPanel.Clean();
		self.__SymPanel.Clean();
		self.__DevPanel.Clean();
	
	def Build(self):
		self.__DevPanel.Build();
		self.__SymPanel.Build();
		self.__SrvPanel.Build();
		

