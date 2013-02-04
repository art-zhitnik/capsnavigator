# -*- coding: utf-8 -*-

import wx
import os
import configobj

from frames import MainFrame
from splash.frames import MySplashScreen
import settings

_ = wx.GetTranslation
        
class App(wx.App):
    def OnInit(self):
        self.__InitDirs()
        self.__SetupLocale()
        MySplashScreen(None)
                  
        self.frame = MainFrame(None, title=_("Caps Navigator"))
        self.SetTopWindow(self.frame)        
        return True
    
    def __InitDirs(self):
        paths = wx.StandardPaths_Get()
        app_data_dir = paths.GetUserDataDir()
        if not os.path.exists(app_data_dir):
            os.mkdir(app_data_dir)
            
    def __SetupLocale(self):
        config_path = wx.StandardPaths_Get().GetUserDataDir()
        config = configobj.ConfigObj(os.path.join(config_path, 'config.ini'))        
        current_lang = wx.LANGUAGE_DEFAULT
        if config.has_key('preferences') and config['preferences'].has_key('main'):
            canonical_name = config['preferences']['main'].get('language')
            for lang in settings.LANGS.values():
                lanf_info = wx.Locale.GetLanguageInfo(lang)
                if lanf_info.CanonicalName == canonical_name:           
                    current_lang = lang
                    break
        self.locale = wx.Locale(current_lang)

if __name__ == '__main__':
    app = App(False)         
    app.frame.Show()    
    app.MainLoop()