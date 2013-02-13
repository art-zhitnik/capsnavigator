# -*- coding: utf-8 -*-

import wx

import menues

_ = wx.GetTranslation

LANGS = {"Default": wx.LANGUAGE_DEFAULT,
         u"English": wx.LANGUAGE_ENGLISH,
         u"Русский": wx.LANGUAGE_RUSSIAN}

ITEM_SIZES = {menues.ID_SMALL_VIEW: 80,
              menues.ID_MEDIUM_VIEW: 120,
              menues.ID_BIG_VIEW: 160}