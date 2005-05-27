import wx;
import logging;
import sys;

class MyLogger(logging.Handler):
	def __init__(self, LogTextCtrl):
		logging.Handler.__init__(self);
		self.__TxtCtrl = LogTextCtrl;

	def emit(self, record):
		level  = record.levelno;
		leveln = record.levelname;
		if level < 20:
			self.__TxtCtrl.SetDefaultStyle(wx.TextAttr(wx.LIGHT_GREY));
		elif level < 30:
			self.__TxtCtrl.SetDefaultStyle(wx.TextAttr(wx.BLACK));
		elif level < 40:
			self.__TxtCtrl.SetDefaultStyle(wx.TextAttr(wx.BLUE));
		elif level >= 40:
			self.__TxtCtrl.SetDefaultStyle(wx.TextAttr(wx.RED));
		else:
			self.__TxtCtrl.SetDefaultStyle(wx.TextAttr(wx.BLACK));
		self.__TxtCtrl.SetInsertionPoint(0);
		self.__TxtCtrl.WriteText("%s: %s\n"%(leveln, record.getMessage()) );


class LogWindow(wx.TextCtrl):
	def __init__(self, parent, ID, PPLTSys):
		wx.TextCtrl.__init__(self, parent, ID, value="", style=wx.TE_MULTILINE, size=(-1,35));
		self.SetEditable(False);
		self.__Logger = logging.getLogger("PPLT");
		logger = MyLogger(self);
		self.__Logger.addHandler(logger);
		self.__Logger.info("PPLT Center Start...");
