import wx;
import os;

def LoadBitmaps(path):
	bmps = {};

	tmp = wx.Bitmap(os.path.normpath(path+"/load.xpm"));
	if not tmp:
		tmp = wx.NullBitmap;
	bmps.update( {"Load":tmp} );

	tmp = wx.Bitmap(os.path.normpath(path+"/save.xpm"));
	if not tmp:
		tmp = wx.NullBitmap;
	bmps.update( {"Save":tmp} );
	
	tmp = wx.Bitmap(os.path.normpath(path+"/saveas.xpm"));
	if not tmp:
		tmp = wx.NullBitmap;
	bmps.update( {"SaveAs":tmp} );
	
	tmp = wx.Bitmap(os.path.normpath(path+"/pack_add.xpm"));
	if not tmp:
		tmp = wx.NullBitmap;
	bmps.update( {"PackAdd":tmp} );
	
	tmp = wx.Bitmap(os.path.normpath(path+"/pack_del.xpm"));
	if not tmp:
		tmp = wx.NullBitmap;
	bmps.update( {"PackDel":tmp} );

	return(bmps);
	
