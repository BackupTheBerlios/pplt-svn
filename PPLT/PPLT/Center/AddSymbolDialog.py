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
from ModusBox import ModusBox;
import PPLT;
import os;


class SelectSlotDialog(wx.Dialog):
	def __init__(self, parent, PPLTSys):
		wx.Dialog.__init__(self, parent, -1, "Select DeviceSlot",size=(250,200));
		
		self.__PPLTSys = PPLTSys;
		
		icondir = PPLT.Config().GetIconPath();
		self.__IL = wx.ImageList(16,16);
		bmp = wx.Bitmap(os.path.normpath(icondir+"/device.xpm"));
		if not bmp:
			bmp = wx.NullBitmap;
		self.__DeviceIcon = self.__IL.Add(bmp);
		bmp = wx.Bitmap(os.path.normpath(icondir+"/class.xpm"));
		if not bmp:
			bmp = wx.NullBitmap;
		self.__NSIcon = self.__IL.Add(bmp);
		bmp = wx.Bitmap(os.path.normpath(icondir+"/slot.xpm"));
		if not bmp:
			bmp = wx.NullBitmap;
		self.__SlotIcon = self.__IL.Add(bmp);
		bmp = wx.Bitmap(os.path.normpath(icondir+"/slot-range.xpm"));
		if not bmp:
			bmp = wx.NullBitmap;
		self.__SlotRIcon = self.__IL.Add(bmp);


		sizer = wx.BoxSizer(wx.VERTICAL);
		
		styleflags = wx.TR_HIDE_ROOT|wx.TR_NO_LINES|wx.TR_TWIST_BUTTONS|wx.TR_HAS_BUTTONS;
		if wx.Platform == "__WXMSW__":
			styleflags = wx.TR_NO_LINES|wx.TR_HAS_BUTTONS;
			
		self.__Tree = wx.TreeCtrl(self, -1, style = styleflags);
		
		self.__Tree.SetImageList(self.__IL);
		self.__ROOT = self.__Tree.AddRoot("Devices");
		self.__Tree.SetPyData(self.__ROOT,(0, None, None));
		sizer.Add(self.__Tree, 3, wx.EXPAND|wx.ALL,3);

		self.__HelpText = wx.TextCtrl(self, -1, size=(250,-1), style=wx.TE_MULTILINE);
		self.__HelpText.SetEditable(False);
		sizer.Add(self.__HelpText, 1, wx.EXPAND|wx.ALL, 3);

		self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelect, self.__Tree);
		self.__Tree.Bind(wx.EVT_LEFT_DCLICK, self.OnDClick);

		self.SetSizer(sizer);
		sizer.Fit(self);

		self.__AddDevices();




	def OnSelect(self, event):
		item = event.GetItem();
		(iden, data, info) = self.__Tree.GetPyData(item);
		if iden == 1:
			txt = info.GetDescription();
			if txt:
				self.__HelpText.Clear();
				self.__HelpText.SetValue(txt);
		elif iden == 4:
			(fqdn, dev, ns, name) = data;
			txt = info.GetSlotRangeDescription(ns,name);
			if txt:
				self.__HelpText.Clear();
				self.__HelpText.SetValue(txt);
		elif iden == 3:
			(fqdn, dev, ns, name) = data;
			txt = info.GetSlotDescription(ns,name);
			if txt:
				self.__HelpText.Clear();
				self.__HelpText.SetValue(txt);
			
	def OnDClick(self, event):
		pt = event.GetPosition();
		(item,flags) = self.__Tree.HitTest(pt);
		if not item:
			return(None);
		
		(iden, data, info) = self.__Tree.GetPyData(item);
		if iden in (0,1,2):
			if self.__Tree.IsExpanded(item):
				self.__Tree.Collapse(item);
			else:
				self.__Tree.Expand(item);
		if not iden in (3,4):
			return(None);
		(fqdn, dev, ns, slot) = data

		if iden == 4:		#if slotrange: ask for spec. slot
			dlg = wx.TextEntryDialog(self, "Enter expl. slot name or addr.:","Slot...");
			if not dlg.ShowModal()==wx.ID_OK:
				return(None);
			slot = dlg.GetValue();

		self.RETURN = ("%s::%s::%s"%(dev, ns, slot),info.GetSlotType(ns,slot));
		self.EndModal(wx.ID_OK);
	
	def __AddDevices(self):
		devlst = self.__PPLTSys.ListDevices();
		for dev in devlst:
			item = self.__Tree.AppendItem(self.__ROOT,dev);
			self.__Tree.SetItemImage(item, self.__DeviceIcon, wx.TreeItemIcon_Normal);
			self.__Tree.SetItemImage(item, self.__DeviceIcon, wx.TreeItemIcon_Expanded);
			fqdn = self.__PPLTSys.GetFQDeviceName(dev);
			info = self.__PPLTSys.GetDeviceInfo(fqdn);
			self.__Tree.SetPyData(item, (1, fqdn, info));
			self.__AddNameSpaces(item, dev, fqdn, info);

	def __AddNameSpaces(self, pitem, dev, fqdn, info):
		nslst = info.GetNameSpaces();
		for ns in nslst:
			item = self.__Tree.AppendItem(pitem, ns);
			self.__Tree.SetItemImage(item, self.__NSIcon, wx.TreeItemIcon_Normal);
			self.__Tree.SetItemImage(item, self.__NSIcon, wx.TreeItemIcon_Expanded);
			self.__Tree.SetPyData(item, (2, None, info));
			self.__AddSlots(item, fqdn, dev, ns, info);
			self.__AddSlotRanges(item, fqdn, dev, ns, info);

	def __AddSlots(self, pitem, fqdn, dev, ns, info):
		slst = info.GetSlots(ns);
		for s in slst:
			item = self.__Tree.AppendItem(pitem, s);
			self.__Tree.SetItemImage(item, self.__SlotIcon, wx.TreeItemIcon_Normal);
			self.__Tree.SetItemImage(item, self.__SlotIcon, wx.TreeItemIcon_Expanded);
			self.__Tree.SetPyData(item, (3,(fqdn, dev, ns, s),info));
			
	def __AddSlotRanges(self, pitem, fqdn, dev, ns, info):
		slst = info.GetSlotRanges(ns);
		for s in slst:
			item = self.__Tree.AppendItem(pitem, s);
			self.__Tree.SetItemImage(item, self.__SlotRIcon, wx.TreeItemIcon_Normal);
			self.__Tree.SetItemImage(item, self.__SlotRIcon, wx.TreeItemIcon_Expanded);
			self.__Tree.SetPyData(item, (4,(fqdn, dev, ns, s),info));




class PropertyDialog(wx.Dialog):
	def __init__(self, Parent, slot, Type, PPLTSys):
		self.__PPLTSys = PPLTSys;
		self.__Slot = slot;

		wx.Dialog.__init__(self, Parent, -1, "Properties of %s"%slot);

		self.__VBox = wx.BoxSizer(wx.VERTICAL);
		
		tmp = wx.StaticText(self,-1,"Name: ");
		self.__Name = wx.TextCtrl(self, -1);
		self.__Name.SetValue("Name");
		box = wx.BoxSizer(wx.HORIZONTAL);
		box.Add(tmp,1,wx.ALIGN_CENTER);
		box.Add(self.__Name,2,wx.GROW|wx.ALIGN_RIGHT);
		self.__VBox.Add(box,0,wx.GROW|wx.ALL,1);

		self.__VBox.Add(wx.StaticLine(self,-1,style=wx.HORIZONTAL),0,wx.GROW|wx.TOP|wx.BOTTOM,2);

		self.__Modus = ModusBox(self, self.__PPLTSys);
		self.__VBox.Add(self.__Modus,0,wx.ALL|wx.GROW,1);
		
		self.__VBox.Add(wx.StaticLine(self,-1,style=wx.HORIZONTAL),0,wx.GROW|wx.TOP|wx.BOTTOM,2);

		tmp = wx.StaticText(self, -1, "Type: ");
		self.__Type = wx.ComboBox(self, -1, choices=["Bool","Byte","Word","DWord","Float","Double","String"]);
		if Type:
			self.__Type.SetValue(str(Type));
		box = wx.BoxSizer(wx.HORIZONTAL);
		box.Add(tmp,1,wx.ALIGN_CENTER);
		box.Add(self.__Type,2,wx.ALIGN_RIGHT|wx.GROW);
		self.__VBox.Add(box,0,wx.GROW|wx.ALL,1);
		
		tmp = wx.StaticText(self, -1, "Refresh: ");
		self.__Rate = wx.TextCtrl(self, -1, "0.5");
		box = wx.BoxSizer(wx.HORIZONTAL);
		box.Add(tmp,1,wx.ALIGN_CENTER);
		box.Add(self.__Rate,2,wx.ALIGN_RIGHT|wx.GROW);
		self.__VBox.Add(box,0,wx.GROW|wx.ALL,1);

		self.__VBox.Add(wx.StaticLine(self,-1,style=wx.HORIZONTAL),0,wx.GROW|wx.TOP|wx.BOTTOM,2);

		self.__OK = wx.Button(self,wx.ID_OK, " OK ");
		self.__CANCEL = wx.Button(self, wx.ID_CANCEL, " Cancel ");
		box = wx.BoxSizer(wx.HORIZONTAL);
		box.Add(self.__OK);
		box.Add(self.__CANCEL);
		self.__VBox.Add(box,0,wx.TOP,5);

		self.SetSizer(self.__VBox);
		self.__VBox.Fit(self);


	def GetName(self):
		return(self.__Name.GetValue());
	def GetSlot(self):
		return(self.__Slot);
	def GetType(self):
		return(self.__Type.GetValue());
	def GetRate(self):
		return(self.__Rate.GetValue());
	def GetModus(self):
		return("%o"%self.__Modus.GetModus());
	def GetOwner(self):
		return(self.__Modus.Owner.GetValue());
	def GetGroup(self):
		return(self.__Modus.Group.GetValue());
