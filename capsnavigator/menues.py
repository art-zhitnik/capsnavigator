# -*- coding: utf-8 -*-

import wx

_ = wx.GetTranslation

class MainMenu(wx.MenuBar):
    def __init__(self, parent, *args, **kwargs):
        super(MainMenu, self).__init__(*args, **kwargs)
        
        self.editmenu = wx.Menu()
        self.editmenu.Append(wx.ID_PREFERENCES)
        self.Append(self.editmenu, _("Edit")) 
        
        self.helpmenu = wx.Menu()
        self.helpmenu.Append(wx.ID_ABOUT)
        self.Append(self.helpmenu, _("Help")) 
        parent.SetMenuBar(self)            