# -*- coding: utf-8 -*-

import wx

from resources import filter_icon

_ = wx.GetTranslation

ID_FILTER = 10

class MainMenu(wx.MenuBar):
    def __init__(self, parent, *args, **kwargs):
        super(MainMenu, self).__init__(*args, **kwargs)
        
        self.filemenu = wx.Menu()
        self.filemenu.Append(wx.ID_EXIT)
        self.Append(self.filemenu, _("File")) 
        
        self.editmenu = wx.Menu()
        self.editmenu.Append(wx.ID_PREFERENCES)
        self.Append(self.editmenu, _("Edit")) 
        
        self.helpmenu = wx.Menu()
        self.helpmenu.Append(wx.ID_ABOUT)
        self.Append(self.helpmenu, _("Help")) 
        parent.SetMenuBar(self)  
        
class MainTreeToolbar(wx.ToolBar):
    def __init__(self, parent):
        super(MainTreeToolbar, self).__init__(parent=parent, style=wx.SIMPLE_BORDER)        
        self.AddStretchableSpace()
        self.SetToolBitmapSize((16, 16))
        filter_bmp = filter_icon.GetBitmap()
        self.AddCheckLabelTool(ID_FILTER, _("Filter"), filter_bmp, filter_bmp, _("Filter"))
        self.Realize()          