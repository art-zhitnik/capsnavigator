# -*- coding: utf-8 -*-

import wx

import resources

_ = wx.GetTranslation

ID_FILTER = 10
ID_SMALL_VIEW = 11
ID_MEDIUM_VIEW = 12
ID_BIG_VIEW = 13
ID_LIST_VIEW = 14
GALLERIES = (ID_SMALL_VIEW, ID_MEDIUM_VIEW, ID_BIG_VIEW)

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
        filter_bmp = resources.filter_icon.GetBitmap()
        self.AddCheckLabelTool(ID_FILTER, _("Filter"), filter_bmp, filter_bmp, _("Filter"))
        self.Realize()
        
class MainViewToolbar(wx.ToolBar):
    def __init__(self, parent):
        super(MainViewToolbar, self).__init__(parent=parent, style=wx.SIMPLE_BORDER)        
        self.AddStretchableSpace()
        self.SetToolBitmapSize((16, 16))
        bmp = resources.view_small_icon.GetBitmap()
        self.AddRadioLabelTool(ID_SMALL_VIEW, _("Small pictures gallery view"), bmp, bmp, _("Small pictures gallery view"))
        bmp = resources.view_medium_icon.GetBitmap()
        self.AddRadioLabelTool(ID_MEDIUM_VIEW, _("Medium pictures gallery view"), bmp, bmp, _("Medium pictures gallery view"))   
        bmp = resources.view_big_icon.GetBitmap()
        self.AddRadioLabelTool(ID_BIG_VIEW, _("Big pictures gallery view"), bmp, bmp, _("Big pictures gallery view"))  
        bmp = resources.view_list_icon.GetBitmap()
        self.AddRadioLabelTool(ID_LIST_VIEW, _("List view"), bmp, bmp, _("List view"))                  
        self.Realize()