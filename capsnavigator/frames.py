# -*- coding: utf-8 -*-

import wx
import wx.lib.agw.hypertreelist as HTL
import sys

from menues import MainMenu, MainTreeToolbar, ID_FILTER
from preferences.frames import PreferencesDialog
from lib.ui import PersistentFrame

_ = wx.GetTranslation

class MainFrame(PersistentFrame):
    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition, size=(800, 600), style=wx.DEFAULT_FRAME_STYLE, name='MainFrame'):
        super(MainFrame, self).__init__(parent, id, title, pos, size, style, name)
        
        self.SetMinSize((800, 600))
        self.navigation = NavigationPanel(self)
        self.panel = wx.Panel(self)        
        MainMenu(self)
        
        self.panel.BackgroundColour = wx.LIGHT_GREY
        self.__DoLayout()
        self.__EventHandlers()
        
    def OnExit(self, event):
        self.Close()
        
    def OnAbout(self, event):
        info = wx.AboutDialogInfo()
        desc = ["\n{0}\n".format(_("A program for collectors!")),
                "{0}: (%s, %s)".format(_("Platform Info")),
                "{0}: {1}".format(_("License"), "LGPL")]
        desc = "\n".join(desc)
        py_version = [sys.platform, ", python ", sys.version.split()[0]]
        py_version = "".join(py_version)
        platform = list(wx.PlatformInfo[1:])
        platform[0] += (" " + wx.VERSION_STRING)
        wx_info = ", ".join(platform)
        info.SetName(_("Caps Navigator"))
        info.SetVersion("4.0.0")
        info.SetCopyright("{0} (C) {1}".format(_("Copyright"), _("Art Zhitnik")))
        info.SetDescription(desc % (py_version, wx_info))
        wx.AboutBox(info)
        
    def OnPreferences(self, event):
        preferences = PreferencesDialog(self)
        preferences.CenterOnParent() 
        preferences.ShowModal() 
        
    def __EventHandlers(self):
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnPreferences, id=wx.ID_PREFERENCES)  
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT) 
        
    def __DoLayout(self):
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.navigation, 1, wx.EXPAND)
        hsizer.Add(self.panel, 5, wx.EXPAND) 
        self.SetSizer(hsizer)
        
class NavigationPanel(wx.Panel):
    def __init__(self, parent):
        super(NavigationPanel, self).__init__(parent)        
               
        self.__MakeControls()
        self.__DoLayout()
        self.__EventHandlers()   
        
    def _OnToolbarPushed(self, event): 
        if event.GetId() == ID_FILTER:                                  
            panelparent = self.tree.GetParent()
            panelsizer = panelparent.GetSizer()
            panelparent.Freeze()            
            panelsizer.Detach(self.tree)
            self.tree.Destroy()
            del self.tree
            self.tree = MainTree(self, check_boxes=event.Checked())
            panelsizer.Add(self.tree, 1, wx.EXPAND)
            panelsizer.Layout()    
            panelparent.Thaw()  
            
        event.Skip()
        
    def __MakeControls(self):
        self.toolbar = MainTreeToolbar(self)
        self.tree = MainTree(self)
    
    def __DoLayout(self):
        hsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer.Add(self.toolbar, 0, wx.EXPAND) 
        hsizer.AddSpacer(3)
        hsizer.Add(self.tree, 1, wx.EXPAND) 
        self.SetSizer(hsizer)
        
    def __EventHandlers(self):
        self.Bind(wx.EVT_TOOL, self._OnToolbarPushed)
        
class MainTree(HTL.HyperTreeList):    
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.NO_BORDER,\
                 agwStyle=wx.TR_HAS_BUTTONS | wx.TR_HAS_VARIABLE_ROW_HEIGHT | wx.TR_HIDE_ROOT | HTL.TR_NO_HEADER,\
                 log=None, check_boxes=False):
        HTL.HyperTreeList.__init__(self, parent, id, pos, size, style, agwStyle)
        
        self.__SetupExtraStyle()
        self.__EventHandlers()        
        
        self.AddColumn("Main column")
        self.AddColumn("Amount", flag=wx.ALIGN_CENTER)
        self.SetMainColumn(0)
        
        il = wx.ImageList(24, 16)
        il.Add(wx.Bitmap('../design/rus24x16.png', wx.BITMAP_TYPE_PNG))
        il.Add(wx.Bitmap('../design/ukr24x16.png', wx.BITMAP_TYPE_PNG))
        self.AssignImageList(il)        
        
        self.root = self.AddRoot("Root")        
        self.locations = self.AppendItem(self.root, _("Location"))
        self.ct_type = check_boxes and 1 or 0
       
        self.AddCountry(self.locations, "Russia", 0) 
        self.AddCountry(self.locations, "Ukraine", 1)
        self.AddCountry(self.locations, "Unknown")     
        
        self.SelectItem(self.locations)
        self.Expand(self.locations)
        
    def AddCountry(self, node, text, flag=None):
        item = self.AppendItem(node, text, ct_type=self.ct_type)
        if flag is not None:            
            self.SetItemImage(item, flag, which=wx.TreeItemIcon_Normal)
             
    def _OnResize(self, event):        
        width = self.Parent.GetSize()[0] - 3
        column0_new_width = width * 0.8
        column1_new_width = width * 0.2
        if column1_new_width != self.GetColumnWidth(0):
            self.SetColumnWidth(0, column0_new_width)
            self.SetColumnWidth(1, column1_new_width)
        event.Skip()
        
    def __SetupExtraStyle(self):
        self.SetBuffered(True)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

    def __EventHandlers(self):
        self.Bind(wx.EVT_SIZE, self._OnResize)
        
if __name__ == '__main__':
    class TestApp(wx.App):
        def OnInit(self):
            self.frame = MainFrame(None)
            self.SetTopWindow(self.frame)
            self.frame.Show()
            return True
    test_app = TestApp(False)
    test_app.MainLoop()