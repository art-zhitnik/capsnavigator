# -*- coding: utf-8 -*-

import wx
import wx.lib.scrolledpanel as scrolled
from wx.lib.art import flagart
from wx.combo import BitmapComboBox 
import configobj
import os
    
if __name__ == '__main__':
    import capsnavigator.settings as settings
else:
    import settings

_ = wx.GetTranslation

class PreferencesDialog(wx.Dialog):
    def __init__(self, parent):
        size = (500, 400)
        wx.Dialog.__init__(self, parent, wx.ID_ANY, _("Preferences"), size=size, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)        
        self.SetMinSize(size)
        self.SetMaxSize((1000, 720))
        self.modified = False 
        config_path = wx.StandardPaths_Get().GetUserDataDir()
        self.config = configobj.ConfigObj(os.path.join(config_path, 'config.ini'))
        if not self.config.has_key('preferences'):
            self.config['preferences'] = {}
            self.modified = True
        self.__MakeControls()
        self.__EventHandlers()
        self.__DoLayout()
        
    def __MakeControls(self):
        self.pages = Pages(self)
        self.save_btn = wx.Button(self, wx.ID_OK, label=_("Save")) 
        self.cancel_btn = wx.Button(self, wx.ID_CANCEL)            
         
    def __EventHandlers(self):
        self.save_btn.Bind(wx.EVT_BUTTON, self.OnSave)
        self.cancel_btn.Bind(wx.EVT_BUTTON, self.OnClose)
        self.Bind(wx.EVT_TEXT, self.OnChange) 
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
    def __DoLayout(self):
        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(self.save_btn)
        btnsizer.AddButton(self.cancel_btn)
        btnsizer.Realize()
        msizer = wx.BoxSizer(wx.VERTICAL)
        msizer.Add(self.pages, 1, wx.ALL | wx.EXPAND)
        msizer.Add(btnsizer, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        self.SetSizer(msizer)
        
    def OnSave(self, event):
        self.config.write()
        self.EndModal(0) 
        
    def OnClose(self, event):
        if self.modified and wx.MessageBox(_("Are you sure you want to exit preferences without saving?"), style=wx.CENTER | wx.ICON_WARNING | wx.OK | wx.CANCEL | wx.CANCEL_DEFAULT) == wx.CANCEL:
            if isinstance(event.EventObject, wx.Dialog):
                event.Veto()
        else:
            self.modified = False
            event.Skip()
        
    def OnChange(self, event):
        param = event.EventObject.GetName()
        section = event.EventObject.Parent.GetName()
        value = event.EventObject.GetValue()
        self.config['preferences'][section][param] = value
        self.modified = True
        event.Skip()

class Pages(wx.Notebook):
    def __init__(self, parent):
        super(Pages, self).__init__(parent)        
        self.panel_preferences = PanelMainPreferences(self, name='main')
        self.AddPage(self.panel_preferences, _("Main preferences"))
        
class PanelMainPreferences(scrolled.ScrolledPanel):
    def __init__(self, parent, name):
        super(PanelMainPreferences, self).__init__(parent, name=name)
        preferences = self.GrandParent.config['preferences']
        if not preferences.has_key(name):
            preferences[name] = {}
        self.cfg = preferences[name]
        self.__MakeControls()
        self.__DoLayout()
        
    def __MakeControls(self):
        self.language_lbl = wx.StaticText(self, label="{0}:".format(_("Language")))        
        self.language = LangCombo(self, 'language', self.cfg.get('language', ''))
    
    def __DoLayout(self):
        sizer = wx.FlexGridSizer(cols=2, vgap=8, hgap=8)
        sizer.AddGrowableCol(1, 1)
        sizer.Add(self.language_lbl, 0, wx.ALIGN_CENTER)
        sizer.Add(self.language, 1)
        self.SetSizer(sizer)
        
class LangCombo(BitmapComboBox):
    """
    Combobox with available translations and flags
    """
    
    def __init__(self, parent, name, value=""):
        super(LangCombo, self).__init__(parent, name=name)
                
        self.reverse_lookup = {}
        for lang_label, lang in settings.LANGS.iteritems():
            lanf_info = wx.Locale.GetLanguageInfo(lang)
            l, cnt = lanf_info.CanonicalName.split('_')            
            if lang_label:
                bmp = flagart.catalog[cnt].getBitmap()
            else:
                bmp = flagart.catalog['BLANK'].getBitmap()
            self.Append(lang_label, bmp)
            if lang == wx.LANGUAGE_DEFAULT:
                reverse_index = ''
            else:
                reverse_index = lanf_info.CanonicalName
            self.reverse_lookup[reverse_index] = lang_label
        self.SetValue(value)
        
    def SetValue(self, value):
        new_value = ''
        if self.reverse_lookup.has_key(value):
            new_value = self.reverse_lookup[value]            
        super(LangCombo, self).SetValue(new_value)
        
    def GetValue(self):
        if settings.LANGS.has_key(self.Value):
            if settings.LANGS[self.Value] != wx.LANGUAGE_DEFAULT:
                lanf_info = wx.Locale.GetLanguageInfo(settings.LANGS[self.Value])
                return lanf_info.CanonicalName
        return ''            
    
if __name__ == '__main__':
    class TestApp(wx.App):
        def OnInit(self):
            self.frame = PreferencesDialog(None)
            self.frame.ShowModal()
            self.frame.Destroy()
            return True
    test_app = TestApp(False)
    test_app.MainLoop()