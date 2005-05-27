import wx;
from ToolMenu import ToolMenu;
from NoteBook import NoteBook;

class MainPanel(wx.Panel):
	def __init__(self, Parent, PPLTSys):
		wx.Panel.__init__(self, Parent, -1);
		
		self.__HBox = wx.BoxSizer(wx.VERTICAL);
		self.__NoteBook = NoteBook(self, -1, PPLTSys);
#		self.__ToolBar = ToolMenu(self, PPLTSys);
		
		self.__HBox.Add(self.__NoteBook,1,wx.GROW);#, 5, wx.GROW);
#		self.__HBox.Add(self.__ToolBar,1,wx.GROW);#, 0, wx.ALIGN_RIGHT,3);
		
		self.SetSizer(self.__HBox);
		
