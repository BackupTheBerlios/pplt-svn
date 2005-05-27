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
