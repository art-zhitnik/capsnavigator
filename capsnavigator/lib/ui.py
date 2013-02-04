# -*- coding: utf-8 -*-

import wx
import configobj
import os
    
import settings

class PersistentFrame(wx.Frame):
    """
    Base class for frames that store their position and size in config file  
    """
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs) 
        config_path = wx.StandardPaths_Get().GetUserDataDir()
        self.config = configobj.ConfigObj(os.path.join(config_path, 'config.ini'))     
        wx.CallAfter(self.RestoreState)
        self.Bind(wx.EVT_CLOSE, self._OnClose)
        self.Bind(wx.EVT_SIZE, self._OnResize)
        self.Bind(wx.EVT_MOVE_END, self._OnMove)
        
    def _OnClose(self, event):
        maximized = self.IsMaximized()       
        if not self.config.has_key('frames'):
            self.config['frames'] = {}
        self.config['frames']['{0}_pos'.format(self.Name.lower())] = repr(self.actual_position)
        self.config['frames']['{0}_size'.format(self.Name.lower())] = repr(self.actual_size)
        self.config['frames']['{0}_maximized'.format(self.Name.lower())] = repr(maximized)
        self.config.write()
        event.Skip()
        
    def _OnResize(self, event):
        if hasattr(self, 'actual_size') and not self.IsMaximized():
            self.actual_size = self.GetSize()
        event.Skip()
        
    def _OnMove(self, event):
        if hasattr(self, 'actual_position') and not self.IsMaximized():
            self.actual_position = self.GetPosition()
        event.Skip()
        
    def RestoreState(self):
        if not self.config.has_key('frames'):
            self.config['frames'] = {}             
        position = self.config['frames'].get('{0}_pos'.format(self.Name.lower()), repr(wx.DefaultPosition))
        size = self.config['frames'].get('{0}_size'.format(self.Name.lower()), repr(wx.DefaultSize))
        maximized = self.config['frames'].get('{0}_maximized'.format(self.Name.lower()), repr(True))
        self.actual_position = eval(position)
        self.actual_size = eval(size)
        maximized = eval(maximized)
        self.SetPosition(self.actual_position)
        self.SetSize(self.actual_size)
        if maximized:
            self.Maximize() 