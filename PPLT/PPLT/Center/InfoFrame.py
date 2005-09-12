import wx;
import PPLT;

class InfoFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, _("PPLT Info"));

        box = wx.BoxSizer(wx.VERTICAL);
        name = wx.StaticText(self,-1,"PPLT Center");
        font = wx.Font(20,wx.SWISS,wx.NORMAL,wx.NORMAL);
        name.SetFont(font);
        name.SetSize(name.GetBestSize());
        box.Add(name, 0, wx.ALIGN_CENTER|wx.TOP|wx.RIGHT|wx.LEFT, 10);
        vers = wx.StaticText(self,-1,"(%s)"%PPLT.__version__);
        box.Add(vers, 0, wx.ALIGN_CENTER|wx.BOTTOM,4);

        txt = wx.StaticText(self,-1,_("http://pplt.berlios.de\nby Hannes Matuschek <hmatuschek@gmx.net>"),style=wx.ALIGN_CENTRE);
        box.Add(txt, 0, wx.ALIGN_CENTER|wx.BOTTOM,10);

        txt = wx.StaticText(self,-1,_(
"""PPLT Center demonstrate the functionality of the PPLT library.  
At first create some users and change the password of the 
superuser.Then load one or two devices, create symbols, that
are attached to the devices and at least start a server.
                   If you missing menus: try right-click.\n"""),style=wx.ALIGN_LEFT);
        box.Add(txt, 0, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT,10);
    
        txt = wx.StaticText(self,-1,"Have a lot of fun...\nHannes Matuschek",style=wx.ALIGN_RIGHT);
        box.Add(txt,0,wx.GROW,0);
        self.SetSizer(box);
        box.Fit(self);

