import wx
from cursor_connect     import getBitmap as getConnectBitmap
from cursor_move        import getBitmap as getMoveBitmap
from cursor_no_connect  import getBitmap as getNoConnectBitmap
from cursor_no_move     import getBitmap as getNoMoveBitmap


def getConnectCursor():
    mask = wx.Mask(getConnectBitmap())
    std_cursor = wx.StockCursor(wx.CURSOR_ARROW)
    std_cursor.SetMask(mask)
    return std_cursor

def getNoConnectCursor():
    mask = wx.Mask(getNoConnectBitmap())
    std_cursor = wx.StockCursor(wx.CURSOR_ARROW)
    std_cursor.SetMask(mask)
    return std_cursor

def getDragCursor():
    mask = wx.Mask(getMoveBitmap())
    std_cursor = wx.StockCursor(wx.CURSOR_ARROW)
    std_cursor.SetMask(mask)
    return std_cursor

def getNoDragCursor():
    mask = wx.Mask(getConnectBitmap())
    std_cursor = wx.StockCursor(wx.CURSOR_ARROW)
    std_cursor.SetMask(mask)
    return std_cursor


