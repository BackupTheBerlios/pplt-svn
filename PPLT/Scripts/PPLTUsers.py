import logging;
import sys;
import wx;
import wx.lib.rcsizer as rcs;
import os.path;

import pyDCPU.UserDB;
import PPLT;



def CreateLogger():
   logger = logging.getLogger('PPLT')
   hdlr = logging.StreamHandler(sys.stdout)
   formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
   hdlr.setFormatter(formatter)
   logger.addHandler(hdlr)
   logger.setLevel(logging.DEBUG)
   return(logger);


def LoadUserDB(FileName):
   logger = logging.getLogger('PPLT');
   UserDB = pyDCPU.UserDB.UserDB(logger, FileName);
   return(UserDB);


def createTree(Tree, DB, PItem, PGroup):
    superuser = DB.GetSuperUser();
    groups = PGroup.ListSubGroups();
    for name in groups:
        group = DB.GetGroupByName(name);
        item = Tree.AppendItem(PItem, name);
        Tree.SetPyData(item, group);
        Tree.SetItemImage(item, 2);
        createTree(Tree, DB, item, group);
        
    users = PGroup.ListMembers();
    for name in users:
        user = DB.GetUserByName(name);
        item = Tree.AppendItem(PItem, name);
        Tree.SetPyData(item, user);
        if name == superuser:
            Tree.SetItemImage(item,3);
            Tree.SuperUserItem = item;
        else:
            Tree.SetItemImage(item,1);
    return(None);

        
def createImageList(path):
    filelist = ['root.xpm','user.xpm','group.xpm','superuser.xpm'];
    il = wx.ImageList(16,16);
    for filename in filelist:
        bm = wx.EmptyBitmap(16,16);
        fullname = os.path.normpath(path+'/'+filename)
        bm.LoadFile(fullname, wx.BITMAP_TYPE_XPM);
        il.Add(bm);
    return( il );   



class CreateErrorInfo(wx.MessageDialog):
    def __init__(self, parent, text):
        wx.MessageDialog.__init__(self, parent, text, 'Error', wx.OK|wx.ICON_ERROR);



class CreateMemberDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title);
        self.Name = '';
        self.Pass1 = '';
        self.Pass2 = '';
        
        sizer = wx.BoxSizer(wx.VERTICAL);

        box = rcs.RowColSizer();

        label = wx.StaticText(self,-1,'Username: ');
        box.Add(label, row=1, col=1, flag=wx.ALIGN_CENTER);
        text = wx.TextCtrl(self, -1, "", size=(120,-1), style=wx.SIMPLE_BORDER);
        text.Bind(wx.EVT_TEXT, self.UpdateName);
        box.Add(text, row=1, col=2);


        label = wx.StaticText(self,-1,'Password: ');
        box.Add(label, row=2, col=1, flag=wx.ALIGN_CENTER);
        self.text1 = wx.TextCtrl(self, -1, "", size=(120,-1), style=wx.TE_PASSWORD|wx.SIMPLE_BORDER);
        self.text1.Bind(wx.EVT_TEXT, self.UpdatePass1);
        box.Add(self.text1, row=2, col=2);

        label = wx.StaticText(self,-1,'Re-Type:  ');
        box.Add(label, row=3, col=1, flag=wx.ALIGN_CENTER);
        self.text2 = wx.TextCtrl(self, -1, "", size=(120,-1), style=wx.TE_PASSWORD|wx.SIMPLE_BORDER);
        self.text2.Bind(wx.EVT_TEXT, self.UpdatePass2);
        box.Add(self.text2, row=3, col=2);
        
        sizer.Add(box, 1, wx.RIGHT, 10);

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM, 5)

        box = wx.BoxSizer(wx.HORIZONTAL);
        self.ok = wx.Button(self, wx.ID_OK, " Ok ");
        box.Add(self.ok, 0, wx.ALIGN_CENTRE|wx.ALL, 5);
        ca = wx.Button(self, wx.ID_CANCEL, ' Cancel ');
        box.Add(ca, 0, wx.ALIGN_CENTRE|wx.ALL, 5);
        sizer.Add(box, 0, wx.ALIGN_CENTRE|wx.ALL, 0);
        
        self.SetSizer(sizer);
        self.SetAutoLayout(True);
        sizer.Fit(self);

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
        text = wx.StaticText(self, -1, 'Group Name: ');
        box.Add(text, 0, wx.ALIGN_CENTER|wx.RIGHT|wx.LEFT, 3);
        input = wx.TextCtrl(self, -1, "", size=(120,-1), style=wx.SIMPLE_BORDER);
        input.Bind(wx.EVT_TEXT, self.UpdateName);
        box.Add(input, 0, wx.ALIGN_CENTER|wx.RIGHT|wx.LEFT, 3);
        sizer.Add(box, 0, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 5);

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM, 2)

        box = wx.BoxSizer(wx.HORIZONTAL);
        ok = wx.Button(self, wx.ID_OK, " Ok ");
        box.Add(ok, 0, wx.ALIGN_CENTRE|wx.ALL, 5);
        ca = wx.Button(self, wx.ID_CANCEL, ' Cancel ');
        box.Add(ca, 0, wx.ALIGN_CENTRE|wx.ALL, 5);
        sizer.Add(box, 0, wx.ALIGN_CENTRE|wx.ALL, 0);
        
        self.SetSizer(sizer);
        self.SetAutoLayout(True);
        sizer.Fit(self);        
        
    def UpdateName(self, event):
        self.Name = event.GetString();



class MainTree(wx.TreeCtrl):
    def __init__(self, parent, id, pos, size, style, userdb):
        wx.TreeCtrl.__init__(self, parent, id, pos, size, style);

        self.UserDB = userdb;
        self.SuperUserItem = None;
        
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)

        self.ID_Create_Member = wx.NewId();
        self.ID_Delete_Member = wx.NewId();
        self.ID_Create_Group  = wx.NewId();
        self.ID_Delete_Group  = wx.NewId();
        self.ID_Set_SuperUser = wx.NewId();

        self.Bind(wx.EVT_MENU, self.CreateMember, id=self.ID_Create_Member);
        self.Bind(wx.EVT_MENU, self.DeleteMember, id=self.ID_Delete_Member);
        self.Bind(wx.EVT_MENU, self.CreateGroup,  id=self.ID_Create_Group);
        self.Bind(wx.EVT_MENU, self.DeleteGroup,  id=self.ID_Delete_Group);
        self.Bind(wx.EVT_MENU, self.SetSuperUser, id=self.ID_Set_SuperUser);
        
    def OnRightClick(self, event):
        pt = event.GetPosition();
        self.selitem, flag = self.HitTest(pt);

        if not self.selitem:        # if right-click on nothing
            return(None);

        self.obj = self.GetPyData(self.selitem);
        menu = wx.Menu();
        
        if isinstance(self.obj, pyDCPU.UserDB.User):
            menu.Append(self.ID_Delete_Member, 'Delete');
            menu.Append(self.ID_Set_SuperUser, 'Become Superuser');
        
        if isinstance(self.obj, pyDCPU.UserDB.Group):
            menu.Append(self.ID_Delete_Group, 'Delete');
            menu.Append(self.ID_Create_Group , 'Add SubGroup');
            menu.Append(self.ID_Create_Member, 'Add Member');

        if isinstance(self.obj, pyDCPU.UserDB.UserDB):
            menu.Append(self.ID_Create_Group, 'Add Group');
#            menu.Append(db_info, 'Info');

        self.PopupMenu(menu,pt);
        menu.Destroy();

    def CreateMember(self, event):
        dialog = CreateMemberDialog(self, -1, 'Create a Member in group %s'%self.obj.GetName());
        ret = dialog.ShowModal();
        if ret == wx.ID_OK:
            name = dialog.Name;
            pass1 = dialog.Pass1;
            pass2 = dialog.Pass2;
            if pass2 != pass1:
                info = CreateErrorInfo(self, "Passwords are different!");
                info.ShowModal();
                info.Destroy();
                return(None);
            if not self.UserDB.CreateMember(self.obj.GetName(), name, pass1, None, True):
                info = CreateErrorInfo(self, "Error while create Member %s"%name);
                info.ShowModal();
                info.Destroy();
                return(None);
            user = self.UserDB.GetUserByName(name);
            item = self.AppendItem(self.selitem, name);
            self.SetPyData(item, user);
            self.SetItemImage(item, 1);
        dialog.Destroy();

    def DeleteMember(self, event):
        name = self.obj.GetName();
        group = self.UserDB.GetGroupByUserName(name);
        groupname = group.GetName();
        if not self.UserDB.DeleteMember(groupname, name):
            info = CreateErrorInfo(self, "Error while delete user %s.\n Maybe it is the superuser."%name);
            info.ShowModal();
            info.Destroy();
            return(None);
        self.Delete(self.selitem);
        
    def CreateGroup(self, event):
        dialog = CreateGroupDialog(self, -1, 'Create a Group');

        ret = dialog.ShowModal();
        if ret == wx.ID_CANCEL:
            dialog.Destroy();
            return(None);
        name = dialog.Name;
        dialog.Destroy();
        
        if isinstance(self.obj, pyDCPU.UserDB.Group):
            groupname = self.obj.GetName();
        else:
            groupname = None;

        if not self.UserDB.CreateGroup(groupname, name):
            info = CreateErrorInfo(self, "Error while create group %s"%name);
            info.ShowModal();
            info.Destroy();
            return(None);
        
        group = self.UserDB.GetGroupByName(name);
        item = self.AppendItem(self.selitem, name);
        self.SetPyData(item, group);
        self.SetItemImage(item, 2);

    def DeleteGroup(self, event):
        name = self.obj.GetName();
        if not self.UserDB.DeleteGroup(name):
            info = CreateErrorInfo(self, "Error while delete group %s!\n Maybe it is not empty..."%name);
            info.ShowModal();
            info.Destroy();
            return(None);
        self.Delete(self.selitem);

    def SetSuperUser(self, event):
        oldsu = self.UserDB.GetSuperUser();
        newsu = self.obj.GetName();
        self.SetItemImage(self.SuperUserItem,1);
        self.SuperUserItem = self.selitem;
        self.SetItemImage(self.SuperUserItem,3);
        self.UserDB.SetSuperUser(newsu);


class MainFrame(wx.Frame):
   def __init__(self, parent, title):
      wx.Frame.__init__(self, parent, -1, title,
                        pos = wx.DefaultPosition, size = wx.DefaultSize,
                        style = wx.DEFAULT_FRAME_STYLE);

      self.Logger = CreateLogger();
      Config = PPLT.Config();
      self.UserDB = pyDCPU.UserDB.UserDB(self.Logger, Config.GetUserDB());

      self.myTree = MainTree(self, 1, wx.DefaultPosition, wx.DefaultSize,
                             wx.TR_HAS_BUTTONS|wx.TR_TWIST_BUTTONS, self.UserDB);


      self.ImageList = createImageList(Config.GetIconPath());
      self.myTree.SetImageList(self.ImageList);    
      
      self.RootItem = self.myTree.AddRoot('User DataBase');
      self.myTree.SetPyData(self.RootItem, self.UserDB);
      self.myTree.SetItemImage(self.RootItem, 0);
      
      groups = self.UserDB.ListSubGroups();
      for name in groups:
          group = self.UserDB.GetGroupByName(name);
          item = self.myTree.AppendItem(self.RootItem, name);
          self.myTree.SetPyData(item, group);
          self.myTree.SetItemImage(item, 2);
          createTree(self.myTree, self.UserDB, item, group);

      self.myTree.Show(True);
       

class MainApp(wx.App):
   def OnInit(self):
      frame = MainFrame(None, 'User-DataBase Editor');
      self.SetTopWindow(frame);
      frame.Show(True);
      return(True);




if __name__ == '__main__':
   app = MainApp();
   app.MainLoop();

