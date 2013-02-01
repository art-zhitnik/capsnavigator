# -*- coding: utf-8 -*-

import wx

from resources import logo

_ = wx.GetTranslation

class MySplashScreen(wx.SplashScreen):
    def __init__(self, parent=None):
        wx.SplashScreen.__init__(self, logo.getBitmap(), wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT, 2000, parent)
        
        self.BackgroundColour = wx.WHITE        
        self.text = wx.StaticText(self, label=_("A program for collectors!"), style=wx.TE_CENTER)
        self.text.Font = wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD)
        rect = self.GetClientRect()
        new_size = (rect.width, self.text.Size[1] + 5)
        self.text.SetSize(new_size)
        self.SetSize((rect.width, rect.height + self.text.Size[1]))
        self.text.SetPosition((0, rect.height))        
                                        
        #wx.Yield()       

if __name__ == "__main__":
    class TestApp(wx.App):
        def OnInit(self):
            self.frame = MySplashScreen(None)
            self.SetTopWindow(self.frame)
            self.frame.Show()
            return True
    test_app = TestApp(False)
    test_app.MainLoop()