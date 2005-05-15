import wx;
import logging;
import sys;
import string;
from DeviceSelectionDialog import DeviceSelectionDialog;
from DeviceParameterDialog import DeviceParameterDialog;

class DevicePanel(wx.ListCtrl):
	def __init__(self, parent, PPLTSys):
		wx.ListCtrl.__init__(self, parent, -1,
								style=wx.LC_REPORT|
										wx.LC_HRULES|
										wx.BORDER_SUNKEN|
										wx.LC_SINGLE_SEL);
		self.__PPLTSys = PPLTSys;
		self.__Logger = logging.getLogger("PPLT");
		self.Fit();
		self.InsertColumn(0,"Alias");
		self.InsertColumn(1,"FQDN",width=150);
		self.InsertColumn(2,"Parameter",width=200);

	def OnAddDevice(self, event):
		self.__Logger.debug("Add device...");
		ret = LoadADevice(self, self.__PPLTSys);
		if ret:
			(Alias, DevName, Paras) = ret;
			index = self.InsertStringItem(sys.maxint, Alias);
			self.SetStringItem(index, 1, DevName);
			self.SetStringItem(index, 2, Paras);

	
def LoadADevice(parent, PPLTSys):
	dlg = DeviceSelectionDialog(parent, PPLTSys);
	ret = dlg.ShowModal();
	if ret != wx.ID_OK:
		return(None);
	DevName = dlg.SelectedDevice;
	dlg.Destroy();
	#print "Selected Device: %s"%DevName;
	
	dlg = DeviceParameterDialog(parent, DevName, PPLTSys);
	ret = dlg.ShowModal();
	if not ret == wx.ID_OK:
		return(None);
	Alias = dlg.Alias.GetValue();
	Vals  = dlg.Values;
	dlg.Destroy();

	#print "%s as %s : %s"%(DevName, Alias, str(vals))
	if PPLTSys.LoadDevice(DevName, Alias, Vals):
		return( (Alias, DevName, ParaToString(Vals)) );
	return(None);


def ParaToString(para):
	keys = para.keys();
	keys.sort();
	lst = [];
	for key in keys:
		lst.append("%s=%s"%(key,para[key]));
	return(string.join(lst, ", "));
