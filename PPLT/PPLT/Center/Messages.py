import wx;
import traceback;

def ErrorMessage(parent, message, title):
    message +="\n\nTraceback:\n"+traceback.format_exc();
    dlg = wx.MessageDialog(parent, message, title, wx.OK|wx.ICON_ERROR);
    dlg.ShowModal();
    dlg.Destroy();
    return;
 
