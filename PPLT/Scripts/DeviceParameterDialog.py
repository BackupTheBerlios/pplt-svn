import wx;

class DeviceParameterDialog(wx.Dialog):
	def __init__(self, parent, DevName, PPLTSys):
		self.__PPLTSys = PPLTSys;
		wx.Dialog.__init__(self, parent, -1, "Setup %s"%DevName);
		self.__DevName = DevName,
		self.__Info = self.__PPLTSys.GetDeviceInfo(DevName);
		self.__Parameters = {};
		self.Values = {};

		self.__MySizer = wx.BoxSizer(wx.VERTICAL);
		
		label = wx.StaticText(self, -1, "Alias: ");
		self.Alias =  wx.TextCtrl(self, -1, "DevName");
		box   = wx.BoxSizer(wx.HORIZONTAL);
		box.Add(label, 1, wx.ALIGN_LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM,4);
		box.Add(self.Alias, 0, wx.ALIGN_RIGHT|wx.LEFT, 3);
		self.__MySizer.Add(box, 0, wx.ALL|wx.GROW, 3);
	
		varlist = self.__Info.GetRequiredVariableNames();
		for var in varlist:
			self.__AddEntry(var);

		ok = wx.Button(self, wx.ID_OK," OK ");
		ca = wx.Button(self, wx.ID_CANCEL, " Cancel ");
		box = wx.BoxSizer(wx.HORIZONTAL);
		box.Add(ok, 0, wx.ALIGN_LEFT|wx.RIGHT|wx.LEFT, 2);
		box.Add(ca, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.LEFT,2);
		self.__MySizer.Add(box, 0, wx.ALL|wx.GROW, 3);

		self.Bind(wx.EVT_BUTTON, self.OnOK, ok);

		self.SetSizer(self.__MySizer);
		self.__MySizer.Fit(self);


	def __AddEntry(self, var):
		defval = self.__Info.GetVariableDefaultValue(var);
		helptxt= self.__Info.GetVariableDescription(var);
		if not defval:
			defval = "";

		label  = wx.StaticText(self, -1, var+": ");
		txt    = wx.TextCtrl(self, -1, defval);
		if helptxt:
			txt.SetToolTipString(helptxt);
		box    = wx.BoxSizer(wx.HORIZONTAL);
		box.Add(label, 1, wx.ALIGN_LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 4);
		box.Add(txt, 0, wx.ALIGN_RIGHT|wx.LEFT, 3);

		self.__MySizer.Add(box, 0, wx.ALL|wx.GROW, 3);
		self.__Parameters.update( {var:txt} );

	
	def OnOK(self, event):
		self.Values = {};
		for var in self.__Parameters.keys():
			val = self.__Parameters[var].GetValue();
			self.Values.update( {var:val} );
		self.EndModal(wx.ID_OK);

