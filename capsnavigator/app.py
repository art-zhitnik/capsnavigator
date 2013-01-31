# -*- coding: utf-8 -*-

import wx

from frames import MainFrame

_ = wx.GetTranslation

class App(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None, title=_("Caps Navigator"))
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True
    
if __name__ == "__main__":
    app = App(False)
    app.MainLoop()