# -*- coding: utf-8 -*-

import wx
import time

from frames import MainFrame
from splash.frames import MySplashScreen 

_ = wx.GetTranslation

class App(wx.App):
    def OnInit(self): 
        spash_screen = MySplashScreen(None)
        spash_screen.Show()
        spash_screen.Refresh()
                  
        self.frame = MainFrame(None, title=_("Caps Navigator"))
        self.SetTopWindow(self.frame)        
        return True
    
if __name__ == "__main__":
    app = App(False)         
    app.frame.Show()    
    app.MainLoop()