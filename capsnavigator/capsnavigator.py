# -*- coding: utf-8 -*-

import wx
import time
import os

from frames import MainFrame
from splash.frames import MySplashScreen 

_ = wx.GetTranslation
        
class App(wx.App):
    def OnInit(self):
        self.InitDirs()
        MySplashScreen(None)
                  
        self.frame = MainFrame(None, title=_("Caps Navigator"))
        self.SetTopWindow(self.frame)        
        return True
    
    def InitDirs(self):
        paths = wx.StandardPaths_Get()
        app_data_dir = paths.GetUserDataDir()
        if not os.path.exists(app_data_dir):
            os.mkdir(app_data_dir)

if __name__ == "__main__":
    app = App(False)         
    app.frame.Show()    
    app.MainLoop()