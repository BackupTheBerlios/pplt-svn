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
# 2005-08-25:
#	Add proxy feature.
#	Layoutfix (CreateMemberDialog)
# 2005-05-27:
#	Release as version 0.2.0 (alpha)

import wx;
import wx.lib.rcsizer as rcs;


class CreateMemberDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title);
        self.Name = '';
        self.Pass1 = '';
        self.Pass2 = '';
        
        sizer = wx.BoxSizer(wx.VERTICAL);

        box = wx.BoxSizer(wx.HORIZONTAL);
        label = wx.StaticText(self,-1,_('Username: '));
        text = wx.TextCtrl(self, -1, "", size=(120,-1), style=wx.SIMPLE_BORDER);
        text.Bind(wx.EVT_TEXT, self.UpdateName);
        box.Add(label, 1, wx.ALIGN_CENTER);
        box.Add(text, 2, wx.EXPAND);
        sizer.Add(box, 0, wx.EXPAND|wx.ALL,2);

        box = wx.BoxSizer(wx.HORIZONTAL);
        label = wx.StaticText(self,-1,_('Password: '));
        self.text1 = wx.TextCtrl(self, -1, "", size=(120,-1), style=wx.TE_PASSWORD|wx.SIMPLE_BORDER);
        self.text1.Bind(wx.EVT_TEXT, self.UpdatePass1);
        box.Add(label, 1, wx.ALIGN_CENTER);
        box.Add(self.text1, 2, wx.EXPAND);
        sizer.Add(box, 0, wx.EXPAND|wx.ALL,2);

        box = wx.BoxSizer(wx.HORIZONTAL);
        label = wx.StaticText(self,-1,_('Re-Type:  '));
        self.text2 = wx.TextCtrl(self, -1, "", size=(120,-1), style=wx.TE_PASSWORD|wx.SIMPLE_BORDER);
        self.text2.Bind(wx.EVT_TEXT, self.UpdatePass2);
        box.Add(label, 1, wx.ALIGN_CENTER);
        box.Add(self.text2, 2, wx.EXPAND);
        sizer.Add(box, 0, wx.EXPAND|wx.ALL,2);

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM, 5)

        box = wx.BoxSizer(wx.HORIZONTAL);
        self.ok = wx.Button(self, wx.ID_OK, _(" Ok "));
        ca = wx.Button(self, wx.ID_CANCEL, _(' Cancel '));
        box.Add(self.ok, 0, wx.ALIGN_CENTRE|wx.ALL, 3);
        box.Add(ca, 0, wx.ALIGN_CENTRE|wx.ALL, 3);
        sizer.Add(box, 0, wx.ALIGN_CENTRE|wx.GROW);

        self.Bind(wx.EVT_KEY_UP, self.OnKey);

        self.SetSizer(sizer);
        self.SetAutoLayout(True);
        sizer.Fit(self);

    def OnKey(self, event):
        if event.GetKeyCode() == wx.WXK_RETURN:
            self.EndModal(wx.ID_OK);
        elif event.GetKeyCode() == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_CANCEL);

    def UpdateName(self, event):
        self.Name = event.GetString();
    def UpdatePass1(self, event):
        self.Pass1 = event.GetString();
        self.UpdateColors();
    def UpdatePass2(self, event):
        self.Pass2 = event.GetString();
        self.UpdateColors();
    def UpdateColors(self):
        if self.Pass1 != self.Pass2:
            self.text1.SetOwnBackgroundColour(wx.RED);
            self.text2.SetOwnBackgroundColour(wx.RED);
            self.text1.Refresh();
            self.text2.Refresh();
            self.ok.Enable(False);
        else:
            self.text1.SetOwnBackgroundColour(wx.WHITE);
            self.text2.SetOwnBackgroundColour(wx.WHITE);
            self.text1.Refresh();
            self.text2.Refresh();
            self.ok.Enable(True);



class CreateGroupDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title);

        self.Name = '';

        sizer = wx.BoxSizer(wx.VERTICAL);

        box = wx.BoxSizer(wx.HORIZONTAL);
        text = wx.StaticText(self, -1, _('Group Name: '));
        input = wx.TextCtrl(self, -1, "", size=(120,-1), style=wx.SIMPLE_BORDER);
        input.Bind(wx.EVT_TEXT, self.UpdateName);
        box.Add(text, 1, wx.ALIGN_CENTER);
        box.Add(input, 2, wx.EXPAND);
        sizer.Add(box, 0, wx.EXPAND|wx.ALL, 3);

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM, 2)

        box = wx.BoxSizer(wx.HORIZONTAL);
        ok = wx.Button(self, wx.ID_OK, _(" Ok "));
        box.Add(ok, 1, wx.ALIGN_CENTRE|wx.ALL, 3);
        ca = wx.Button(self, wx.ID_CANCEL, _(' Cancel '));
        box.Add(ca, 1, wx.ALIGN_CENTRE|wx.ALL, 3);
        sizer.Add(box, 1, wx.ALIGN_CENTRE|wx.GROW);

        self.Bind(wx.EVT_KEY_UP, self.OnKey);

        self.SetSizer(sizer);
        self.SetAutoLayout(True);
        sizer.Fit(self);

    def UpdateName(self, event):
        self.Name = event.GetString();

    def OnKey(self, event):
        if event.GetKeyCode() == wx.WXK_RETURN:
            self.EndModal(wx.ID_OK);
        elif event.GetKeyCode() == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_CANCEL);


class CreateProxyDialog(wx.Dialog):
	def __init__(self, parent, id, title, UserList):
		wx.Dialog.__init__(self, parent, id, title);
		self.Name = UserList[0];

		sizer = wx.BoxSizer(wx.VERTICAL);
		
		box = wx.BoxSizer(wx.HORIZONTAL);
		text = wx.StaticText(self, -1, _('User Name: '));
		Input = wx.ComboBox(self, -1, UserList[0], choices=UserList);
		Input.SetEditable(False);
		Input.Bind(wx.EVT_TEXT, self.UpdateName);
		box.Add(text, 1, wx.ALIGN_CENTER, 0);
		box.Add(Input, 2, wx.EXPAND, 0);
		sizer.Add(box, 0, wx.EXPAND|wx.ALL, 3);

		line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL);
		sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM, 2)

		box = wx.BoxSizer(wx.HORIZONTAL);
		ok = wx.Button(self, wx.ID_OK, _(" Ok "));
		box.Add(ok, 1, wx.ALIGN_CENTRE|wx.ALL, 3);
		ca = wx.Button(self, wx.ID_CANCEL, _(' Cancel '));
		box.Add(ca, 1, wx.ALIGN_CENTRE|wx.ALL, 3);
		sizer.Add(box, 1, wx.ALIGN_CENTRE|wx.GROW);

		self.Bind(wx.EVT_KEY_UP, self.OnKey);

		self.SetSizer(sizer);
		self.SetAutoLayout(True);
		sizer.Fit(self);

	def UpdateName(self, event):
		self.Name = event.GetString();

	def OnKey(self, event):
		if event.GetKeyCode() == wx.WXK_RETURN:
			self.EndModal(wx.ID_OK);
		elif event.GetKeyCode() == wx.WXK_ESCAPE:
			self.EndModal(wx.ID_CANCEL);



class PasswdDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title);
        self.Pass1 = '';
        self.Pass2 = '';
        
        sizer = wx.BoxSizer(wx.VERTICAL);

        box = wx.BoxSizer(wx.HORIZONTAL);
        label = wx.StaticText(self,-1,_('Password: '));
        self.text1 = wx.TextCtrl(self, -1, "", size=(120,-1), style=wx.TE_PASSWORD|wx.SIMPLE_BORDER);
        self.text1.Bind(wx.EVT_TEXT, self.UpdatePass1);
        box.Add(label, 1, wx.ALIGN_CENTER);
        box.Add(self.text1, 2, wx.EXPAND);
        sizer.Add(box, 0, wx.EXPAND|wx.ALL, 2);

        box = wx.BoxSizer(wx.HORIZONTAL);
        label = wx.StaticText(self,-1,_('Re-Type:  '));
        self.text2 = wx.TextCtrl(self, -1, "", size=(120,-1), style=wx.TE_PASSWORD|wx.SIMPLE_BORDER);
        self.text2.Bind(wx.EVT_TEXT, self.UpdatePass2);
        box.Add(label, 1, wx.ALIGN_CENTER);
        box.Add(self.text2, 2, wx.EXPAND);
        sizer.Add(box, 0, wx.EXPAND|wx.ALL, 2);

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM, 5)

        box = wx.BoxSizer(wx.HORIZONTAL);
        self.ok = wx.Button(self, wx.ID_OK, _(" Ok "));
        ca = wx.Button(self, wx.ID_CANCEL, _(' Cancel '));
        box.Add(self.ok, 1, wx.ALIGN_CENTRE|wx.ALL, 3);
        box.Add(ca, 1, wx.ALIGN_CENTRE|wx.ALL, 3);
        sizer.Add(box, 1, wx.ALIGN_CENTRE|wx.GROW);

        self.Bind(wx.EVT_KEY_UP, self.OnKey);

        self.SetSizer(sizer);
        self.SetAutoLayout(True);
        sizer.Fit(self);

    def OnKey(self, event):
        if event.GetKeyCode() == wx.WXK_RETURN:
            self.EndModal(wx.ID_OK);
        elif event.GetKeyCode() == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_CANCEL);
    def UpdatePass1(self, event):
        self.Pass1 = event.GetString();
        self.UpdateColors();
    def UpdatePass2(self, event):
        self.Pass2 = event.GetString();
        self.UpdateColors();
    def UpdateColors(self):
        if self.Pass1 != self.Pass2:
            self.text1.SetOwnBackgroundColour(wx.RED);
            self.text2.SetOwnBackgroundColour(wx.RED);
            self.text1.Refresh();
            self.text2.Refresh();
            self.ok.Enable(False);
        else:
            self.text1.SetOwnBackgroundColour(wx.WHITE);
            self.text2.SetOwnBackgroundColour(wx.WHITE);
            self.text1.Refresh();
            self.text2.Refresh();
            self.ok.Enable(True);






