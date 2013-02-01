# -*- coding: utf-8 -*-

import wx

from menues import MainMenu

_ = wx.GetTranslation

class MainFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE, name="MainFrame"):
        super(MainFrame, self).__init__(parent, id, title, pos, size, style, name)
        
        self.panel = wx.Panel(self)        
        MainMenu(self)             
        
        self.panel.BackgroundColour = wx.GREEN
        self.__DoLayout()               
        
    def __DoLayout(self):
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.AddSpacer(200)
        hsizer.Add(self.panel, 1, wx.EXPAND) 
        self.SetSizer(hsizer)       
    
if __name__ == "__main__":
    class TestApp(wx.App):
        def OnInit(self):
            self.frame = MainFrame(None)
            self.SetTopWindow(self.frame)
            self.frame.Show()
            return True
    test_app = TestApp(False)
    test_app.MainLoop()