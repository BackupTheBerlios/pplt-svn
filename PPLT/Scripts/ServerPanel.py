import wx;
import logging;
import sys;
import string;
from ServerSelectionDialog import ServerSelectionDialog;
from ServerParameterDialog import ServerParameterDialog;

class ServerPanel(wx.ListCtrl):
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
		self.InsertColumn(1,"FQSN",width=100);
		self.InsertColumn(2,"DefaultUser");
		self.InsertColumn(3,"Parameter",width=200);

	def OnAddServer(self, event):
		self.__Logger.debug("Add Server...");
		ret = LoadAServer(self, self.__PPLTSys);
		if ret:
			(Alias, SrvName, DefUser, Paras) = ret;
			index = self.InsertStringItem(sys.maxint, Alias);
			self.SetStringItem(index, 1, SrvName);
			self.SetStringItem(index, 2, DefUser);
			self.SetStringItem(index, 3, Paras);


	
def LoadAServer(parent, PPLTSys):
	dlg = ServerSelectionDialog(parent, PPLTSys);
	ret = dlg.ShowModal();
	if ret != wx.ID_OK:
		return(None);
	SrvName = dlg.SelectedServer;
	dlg.Destroy();
	#print "Selected Server: %s"%SrvName;
	
	dlg = ServerParameterDialog(parent, SrvName, PPLTSys);
	ret = dlg.ShowModal();
	if not ret == wx.ID_OK:
		return(None);
	Alias = dlg.Alias.GetValue();
	DefUser = dlg.DefUser.GetValue();
	Vals  = dlg.Values;
	dlg.Destroy();

	#print "%s as %s(%s) : %s"%(SrvName, Alias, DefUser,str(Vals))
	if PPLTSys.LoadServer(SrvName, Alias, DefUser, Vals):
		return( (Alias, SrvName, DefUser, ParaToString(Vals)) );
	return(None);


def ParaToString(para):
	keys = para.keys();
	keys.sort();
	lst = [];
	for key in keys:
		lst.append("%s=%s"%(key,para[key]));
	return(string.join(lst, ", "));
