import wx;
import traceback;

#CHANGELOG:
# 2006-03-29:
#   * Now the tracebach is printed into a
#     scrolled text-window
class ErrorMessageDialog(wx.Dialog):
    def __init__(self, parent, message, title):
        trace = traceback.format_exc();
        wx.Dialog.__init__(self, parent, title=title);
        
        hbox     = wx.BoxSizer(wx.HORIZONTAL);

        icon     = wx.StaticBitmap(self, bitmap=wx.ArtProvider.GetBitmap(wx.ART_ERROR, size=(64,64)));
        hbox.Add(icon, 0, wx.ALL|wx.CENTRE, 10);
        
        box      = wx.BoxSizer(wx.VERTICAL);
        
        text     = self.CreateTextSizer(message);
        box.Add(text, 0, wx.GROW|wx.CENTRE|wx.ALL, 10);
        
        hl1 = wx.StaticLine(self);
        box.Add(hl1, 0, wx.GROW|wx.CENTRE|wx.BOTTOM, 5);

        tracewin = wx.TextCtrl(self, value=trace, style=wx.TE_MULTILINE|wx.TE_DONTWRAP, size=(300, 100));
        tracewin.SetEditable(False);
        box.Add(tracewin, 0, wx.CENTRE|wx.LEFT|wx.RIGHT, 5);
        
        hl2 = wx.StaticLine(self);
        box.Add(hl2, 0, wx.GROW|wx.CENTRE|wx.TOP|wx.BOTTOM, 5);

        buttons  = self.CreateStdDialogButtonSizer(wx.OK);
        box.Add(buttons, 0, wx.ALIGN_RIGHT|wx.ALL, 5);

        hbox.Add(box, 1, wx.GROW);
        self.SetSizer(hbox);
        hbox.Fit(self);

def ErrorMessage(parent, message, title):
    dlg = ErrorMessageDialog(parent, message, title);
    dlg.ShowModal();
    dlg.Destroy();
    return;
 
