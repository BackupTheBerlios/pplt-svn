import wx;
from ModusBox import ModusBox;


class AddFolderDialog(wx.Dialog):
	def __init__(self, parent, PPLTSys, PPath):
		wx.Dialog.__init__(self, parent, -1, "Add Folder");
		
		sizer = wx.BoxSizer(wx.VERTICAL);
		
		label = wx.StaticText(self, -1, "Name: ");
		self.Name = wx.TextCtrl(self, -1, "Name");
		box = wx.BoxSizer(wx.HORIZONTAL);
		box.Add(label,1,wx.ALIGN_CENTER);
		box.Add(self.Name,3,wx.EXPAND);
		sizer.Add(box,0,wx.EXPAND|wx.ALL,3);
	
		self.__modbox = ModusBox(self, PPLTSys);
		sizer.Add(self.__modbox,0,wx.EXPAND|wx.ALL,3);
		
		ok = wx.Button(self, wx.ID_OK, " Ok ");
		ca = wx.Button(self, wx.ID_CANCEL, " Cancel ");
		box = wx.BoxSizer(wx.HORIZONTAL);
		box.Add(ok);
		box.Add(ca);
		sizer.Add(box, 0, wx.ALL, 3);

		self.SetSizer(sizer);
		sizer.Fit(self);

	def OnOK(self, event):
		self.EndModal(wx.ID_OK);

	def GetModus(self):
		return(self.__modbox.GetModus());
	def GetName(self):
		return(self.Name.GetValue());
	def GetOwner(self):
		return(self.__modbox.Owner.GetValue());
	def GetGroup(self):
		return(self.__modbox.Group.GetValue());



