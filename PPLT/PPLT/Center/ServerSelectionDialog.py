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
import logging;
import sys;
import PPLT;
import os;


class ServerSelectionDialog(wx.Dialog):
	def __init__(self, parent, PPLTSys):
		wx.Dialog.__init__(self, parent, -1, 
							"ServerSelection",
							size = wx.Size(300,250));
		self.__PPLTSys = PPLTSys;
		
		sizer = wx.BoxSizer(wx.VERTICAL);

		self.__Tree = ServerTree(self, PPLTSys);

		self.__Help = wx.TextCtrl(self, -1, style = wx.TE_MULTILINE);
		self.__Help.SetEditable(False);

		sizer.Add(self.__Tree, 1, wx.ALIGN_CENTRE|wx.GROW, 3);
		sizer.Add(self.__Help, 0, wx.ALIGN_CENTRE|wx.GROW|wx.TOP, 3);

		self.SetSizer(sizer);
		self.SetAutoLayout(True);
		sizer.Fit(self.__Tree);

		self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelect, self.__Tree);
		self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnDClick, self.__Tree);


	def OnSelect(self, event):
		item = event.GetItem();
		if item:
			dat = self.__Tree.GetPyData(item);
			if dat:
				self.__Help.Clear();
				info = self.__PPLTSys.GetServerInfo(dat);
				if info:
					txt = info.GetDescription();
					self.__Help.AppendText(txt);
		
	def OnDClick(self, event):
		item = event.GetItem();
		if item:
			dat = self.__Tree.GetPyData(item);
			if dat:
				self.SelectedServer = dat;
				self.EndModal(wx.ID_OK);


class ServerTree(wx.TreeCtrl):
	def __init__(self, parent, PPLTSys):
		self.__PPLTSys = PPLTSys;
		styleflags=wx.TR_NO_LINES|wx.TR_TWIST_BUTTONS|wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT;
		if wx.Platform == "__WXMSW__":
			styleflags=wx.TR_NO_LINES|wx.TR_HAS_BUTTONS;
			
		wx.TreeCtrl.__init__(self, parent, -1, style=styleflags);
		
		#store icons
		iconpath = PPLT.Config().GetIconPath();
		self.__IL = wx.ImageList(16,16);
		bmp = wx.Bitmap(os.path.normpath(iconpath+"/server.xpm"));
		if not bmp:
			bmp = wx.NullBitmap;
		self.__SrvImg = self.__IL.Add(bmp);
		bmp = wx.Bitmap(os.path.normpath(iconpath+"/class.xpm"));
		if not bmp:
			bmp = wx.NullBitmap;
		self.__ClsImg = self.__IL.Add(bmp);
		self.SetImageList(self.__IL);
		
		self.__Root = self.AddRoot("SDB");
		self.SetPyData(self.__Root, None);

		self.__AddServers(None, self.__Root);

	def __AddServers(self, Class, PItem):
		classes = self.__PPLTSys.ListKnownServerClasses(Class);
		for cl in classes:
			item = self.AppendItem(PItem, cl);
			self.SetItemImage(item, self.__ClsImg, wx.TreeItemIcon_Normal);
			self.SetItemImage(item, self.__ClsImg, wx.TreeItemIcon_Expanded);
			self.SetPyData(item,None);
			if not Class:
				nclass = cl;
			else:
				nclass = "%s.%s"%(Class,cl);
			self.__AddServers(nclass,item);
		srvs = self.__PPLTSys.ListKnownServers(Class);
		for srv in srvs:
			item = self.AppendItem(PItem, srv);
			self.SetItemImage(item, self.__SrvImg, wx.TreeItemIcon_Normal);
			self.SetItemImage(item, self.__SrvImg, wx.TreeItemIcon_Expanded);
			self.SetPyData(item, "%s.%s"%(Class,srv));

