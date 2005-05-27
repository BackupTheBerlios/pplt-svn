import wx;
from ModusBox import ModusBox;


class SetPropertyDialog(wx.Dialog):
	def __init__(self, parent, PPLTSys, owner, group, modus):
		wx.Dialog.__init__(self, parent, -1, "Properties");
		
		sizer = wx.BoxSizer(wx.VERTICAL);
		
		self.__modbox = ModusBox(self, PPLTSys, owner, group, modus);
		sizer.Add(self.__modbox, 0, wx.EXPAND|wx.ALL, 3);
		
		ok = wx.Button(self, wx.ID_OK, " Ok ");
		ca = wx.Button(self, wx.ID_CANCEL, " Cancel ");
		box = wx.BoxSizer(wx.HORIZONTAL);
		box.Add(ok, 0, wx.ALL, 2);
		box.Add(ca, 0, wx.ALL, 2);
		sizer.Add(box, 0, wx.ALL, 3);

		self.SetSizer(sizer);
		sizer.Fit(self);

	def OnOK(self, event):
		self.EndModal(wx.ID_OK);

	def GetModus(self):
		return("%o"%self.__modbox.GetModus());
	def GetName(self):
		return(self.Name.GetValue());
	def GetOwner(self):
		return(self.__modbox.Owner.GetValue());
	def GetGroup(self):
		return(self.__modbox.Group.GetValue());



