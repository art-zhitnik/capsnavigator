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
        if not self.config.has_key('frames'):
            self.config['frames'] = {}
        wx.CallAfter(self.RestoreState)
        self.__EventHandlers()
        
    def __OnClose(self, event):
        maximized = self.IsMaximized()       
        self.config['frames']['{0}_pos'.format(self.Name.lower())] = repr(self.actual_position)
        self.config['frames']['{0}_size'.format(self.Name.lower())] = repr(self.actual_size)
        self.config['frames']['{0}_maximized'.format(self.Name.lower())] = repr(maximized)
        try:
            self.config.write()
        except IOError:
            print "Can't save config!"
        event.Skip()
        
    def __OnResize(self, event):
        if hasattr(self, 'actual_size') and not self.IsMaximized():
            self.actual_size = self.GetSize().Get()
        event.Skip()
        
    def __OnMove(self, event):
        if hasattr(self, 'actual_position') and not self.IsMaximized():
            self.actual_position = self.GetPosition().Get()
        event.Skip()
        
    def RestoreState(self):
        if not self.config.has_key('frames'):
            self.config['frames'] = {}             
        position = self.config['frames'].get('{0}_pos'.format(self.Name.lower()), repr(wx.DefaultPosition.Get()))
        size = self.config['frames'].get('{0}_size'.format(self.Name.lower()), repr(wx.DefaultSize.Get()))
        maximized = self.config['frames'].get('{0}_maximized'.format(self.Name.lower()), repr(True))
        self.actual_position = eval(position)
        self.actual_size = eval(size)
        maximized = eval(maximized)
        self.SetPosition(self.actual_position)
        self.SetSize(self.actual_size)
        if maximized:
            self.Maximize() 
            
    def __EventHandlers(self):
        self.Bind(wx.EVT_CLOSE, self.__OnClose)
        self.Bind(wx.EVT_SIZE, self.__OnResize)
        self.Bind(wx.EVT_MOVE, self.__OnMove)     