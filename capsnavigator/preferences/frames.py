# -*- coding: utf-8 -*-

import wx
import wx.lib.scrolledpanel as scrolled
import wx.lib.langlistctrl as langlist
from wx.lib.art import flagart
from wx.combo import BitmapComboBox 

from resources import logo

_ = wx.GetTranslation

class PreferencesDialog(wx.Dialog):
    def __init__(self, parent):
        size = (500,400)
        wx.Dialog.__init__(self, parent, wx.ID_ANY, _("Preferences"), size=size, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)        
        self.SetMinSize(size)
        self.SetMaxSize((1000,720))  
        self.__MakeControls()
        self.__EventHandlers()
        self.__DoLayout()
        
    def __MakeControls(self):
        self.pages = Pages(self)
        self.save_btn = wx.Button(self, wx.ID_OK, label=_("Save")) 
        self.cancel_btn = wx.Button(self, wx.ID_CANCEL)    
        
    def __EventHandlers(self):
        self.save_btn.Bind(wx.EVT_BUTTON, self.OnSave)     
        
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
        
        self.EndModal(0)        

class Pages(wx.Notebook):
    def __init__(self, parent):
        super(Pages, self).__init__(parent)
        
        self.panel_preferences = PanelMainPreferences(self)        
        self.AddPage(self.panel_preferences, _("Main preferences"))
        
class PanelMainPreferences(scrolled.ScrolledPanel):
    def __init__(self, parent):
        super(PanelMainPreferences, self).__init__(parent)
        self.__MakeControls()
        self.__DoLayout()
        
    def __MakeControls(self):
        self.language_lbl = wx.StaticText(self, label="{0}:".format(_("Language")))
        self.language = LangCombo(self, 'en_GB')
    
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
    
    langs = {_("Default"): wx.LANGUAGE_DEFAULT,
             u"English": wx.LANGUAGE_ENGLISH,
             u"Русский": wx.LANGUAGE_RUSSIAN}
    
    def __init__(self, parent, value=""):
        super(LangCombo, self).__init__(parent)
                
        self.reverse_lookup = {}
        for lang_label, lang in LangCombo.langs.iteritems():
            lanf_info = wx.Locale.GetLanguageInfo(lang)
            l, cnt = lanf_info.CanonicalName.split('_')            
            if lang_label:
                bmp = flagart.catalog[cnt].getBitmap()
            else:
                bmp = flagart.catalog["BLANK"].getBitmap()
            self.Append(lang_label, bmp)
            if lang == wx.LANGUAGE_DEFAULT:
                reverse_index = ""
            else:
                reverse_index = lanf_info.CanonicalName
            self.reverse_lookup[reverse_index] = lang_label
        self.SetValue(value)
        
    def SetValue(self, value):
        new_value = ""
        if self.reverse_lookup.has_key(value):
            new_value = self.reverse_lookup[value]            
        super(LangCombo, self).SetValue(new_value)
        
    def GetValue(self):
        if LangCombo.langs.has_key(self.Value):
            if LangCombo[self.Value] != wx.LANGUAGE_DEFAULT:
                lanf_info = wx.Locale.GetLanguageInfo(LangCombo[self.Value])
                return lanf_info.CanonicalName
        return ""            
    
if __name__ == "__main__":
    class TestApp(wx.App):
        def OnInit(self):
            self.frame = PreferencesDialog(None)
            self.frame.ShowModal()
            self.frame.Destroy()
            return True
    test_app = TestApp(False)
    test_app.MainLoop()