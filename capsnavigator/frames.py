# -*- coding: utf-8 -*-

import wx
import sys

from menues import MainMenu
from preferences.frames import PreferencesDialog

_ = wx.GetTranslation

class MainFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE, name='MainFrame'):
        super(MainFrame, self).__init__(parent, id, title, pos, size, style, name)
        
        self.panel = wx.Panel(self)        
        MainMenu(self)             
        
        self.panel.BackgroundColour = wx.GREEN
        self.__DoLayout()
        
        self.Bind(wx.EVT_MENU, self.OnPreferences, id=wx.ID_PREFERENCES)  
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)    
        
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
        
    def __DoLayout(self):
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.AddSpacer(200)
        hsizer.Add(self.panel, 1, wx.EXPAND) 
        self.SetSizer(hsizer)    
    
if __name__ == '__main__':
    class TestApp(wx.App):
        def OnInit(self):
            self.frame = MainFrame(None)
            self.SetTopWindow(self.frame)
            self.frame.Show()
            return True
    test_app = TestApp(False)
    test_app.MainLoop()