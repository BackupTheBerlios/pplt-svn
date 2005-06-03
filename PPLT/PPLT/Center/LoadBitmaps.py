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
import os;

def LoadBitmaps(path):
	bmps = {};

	tmp = wx.Bitmap(os.path.normpath(path+"/new.xpm"));
	if not tmp:
		tmp = wx.NullBitmap;
	bmps.update( {"New":tmp} );

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
	
	tmp = wx.Bitmap(os.path.normpath(path+"/info.xpm"));
	if not tmp:
		tmp = wx.NullBitmap;
	bmps.update( {"Info":tmp} );
#	tmp = wx.Bitmap(os.path.normpath(path+"/pack_del.xpm"));
#	if not tmp:
#		tmp = wx.NullBitmap;
#	bmps.update( {"PackDel":tmp} );

	return(bmps);
	
