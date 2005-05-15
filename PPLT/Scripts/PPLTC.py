#!/usr/bin/python
import wx;
import PPLT;
import NoteBook;
import LogWindow;

		


class MainFrame(wx.Frame):
	def __init__(self, parent, title,PPLTSys):
		wx.Frame.__init__(self, parent, -1, title,
							pos = wx.DefaultPosition,
							size = wx.DefaultSize,
							style = wx.DEFAULT_FRAME_STYLE);
		self.__PPLTSys = PPLTSys;

		self.__VBox = wx.SplitterWindow(self, -1);
		self.__NoteBook = NoteBook.NoteBook(self.__VBox, -1, self.__PPLTSys);
		self.__LogWindow = LogWindow.LogWindow(self.__VBox, -1, self.__PPLTSys);
		
		self.__VBox.SetMinimumPaneSize(20)
		self.__VBox.SplitHorizontally(self.__NoteBook, self.__LogWindow);
		self.__VBox.SetSashPosition(1000);

class Application(wx.App):
	def OnInit(self):
		self.__PPLTSys = PPLT.System();
		#self.__PPLTSys = None;
		frame = MainFrame(None,'PPLT Center',self.__PPLTSys);
		self.SetTopWindow(frame);
		frame.Show(True);
		return(True);

if __name__ == '__main__':
	app = Application();
	app.MainLoop();
		
