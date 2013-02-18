# -*- coding: utf-8 -*-

import wx
import wx.lib.agw.hypertreelist as HTL
import wx.lib.mixins.listctrl as listmix
import wx.grid as gridlib
import sys
import os
import configobj
from math import ceil

import menues
import settings
from preferences.frames import PreferencesDialog
from lib.ui import PersistentFrame
import resources

_ = wx.GetTranslation

class MainFrame(PersistentFrame):
    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition, size=(800, 600), style=wx.DEFAULT_FRAME_STYLE, name='MainFrame'):
        super(MainFrame, self).__init__(parent, id, title, pos, size, style, name)
        
        self.SetMinSize((800, 600))
        self.navigation = NavigationPanel(self)
        self.view_panel = ViewPanel(self)
        menues.MainMenu(self)

        self.__DoLayout()
        self.__EventHandlers()
        
    def OnExit(self, event):
        self.Close()
        
    def __OnResize(self, event):
        if self.view_panel.mode in menues.GALLERIES:
            self.view_panel.Freeze()
            width = self.ClientSize[0] - self.navigation.MinWidth 
            newcols = width / self.view_panel.item_size
            if newcols != self.view_panel.gallery.cols_best_amount:
                self.view_panel.gallery.cols_best_amount = newcols
                self.view_panel.gallery.Reset()        
            self.view_panel.WidthCorrection()
            self.view_panel.Thaw()
        else:
            width = self.ClientSize[0] - self.navigation.MinWidth 
            self.view_panel.SetSizeHints(width, self.ClientSize[1])
        event.Skip()

    def OnAbout(self, event):
        info = wx.AboutDialogInfo()
        desc = ["\n{0}\n".format(_("A program for collectors!")),
                "{0}: (%s, %s)".format(_("Platform Info")),
                "{0}: {1}".format(_("License"), "LGPL")]
        desc = "\n".join(desc)
        py_version = [sys.platform, ", python ", sys.version.split()[0]]
        py_version = "".join(py_version)
        platform = list(wx.PlatformInfo[1:])
        platform[0] += (" " + wx.VERSION_STRING)
        wx_info = ", ".join(platform)
        info.SetName(_("Caps Navigator"))
        info.SetVersion("4.0.0")
        info.SetCopyright("{0} (C) {1}".format(_("Copyright"), _("Art Zhitnik")))
        info.SetDescription(desc % (py_version, wx_info))
        wx.AboutBox(info)
        
    def OnPreferences(self, event):
        preferences = PreferencesDialog(self)
        preferences.CenterOnParent() 
        preferences.ShowModal() 
        
    def __OnClose(self, event):
        self.config['frames']['mainframe_view_mode'] = self.view_panel.mode        
        event.Skip()
        
    def __EventHandlers(self):
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnPreferences, id=wx.ID_PREFERENCES)  
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT) 
        self.Bind(wx.EVT_SIZE, self.__OnResize)
        self.Bind(wx.EVT_CLOSE, self.__OnClose)    
        
    def __DoLayout(self):
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.navigation, 1, wx.EXPAND)
        hsizer.Add(self.view_panel, 0)        
        self.SetSizer(hsizer)
        
class NavigationPanel(wx.Panel):
    def __init__(self, parent):
        super(NavigationPanel, self).__init__(parent)        
        
        self.SetMinSize((200, 0))        
        
        self.__MakeControls()
        self.__DoLayout()
        self.__EventHandlers()   
        
    def __OnToolbarPushed(self, event): 
        if event.GetId() == menues.ID_FILTER:                                  
            panelparent = self.tree.GetParent()
            panelsizer = panelparent.GetSizer()
            panelparent.Freeze()            
            panelsizer.Detach(self.tree)
            self.tree.Destroy()
            del self.tree
            self.tree = MainTree(self, check_boxes=event.Checked())
            panelsizer.Add(self.tree, 1, wx.EXPAND)
            panelsizer.Layout()    
            panelparent.Thaw()  
            
        event.Skip()
        
    def __MakeControls(self):
        self.toolbar = menues.MainTreeToolbar(self)
        self.tree = MainTree(self)
    
    def __DoLayout(self):
        hsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer.Add(self.toolbar, 0, wx.EXPAND) 
        hsizer.AddSpacer(3)
        hsizer.Add(self.tree, 1, wx.EXPAND) 
        self.SetSizer(hsizer)
        
    def __EventHandlers(self):
        self.Bind(wx.EVT_TOOL, self.__OnToolbarPushed)
        
class MainTree(HTL.HyperTreeList):    
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.NO_BORDER,\
                 agwStyle=wx.TR_HAS_BUTTONS | wx.TR_HAS_VARIABLE_ROW_HEIGHT | wx.TR_HIDE_ROOT | HTL.TR_NO_HEADER,\
                 log=None, check_boxes=False):
        HTL.HyperTreeList.__init__(self, parent, id, pos, size, style, agwStyle)
        
        self.__SetupExtraStyle()
        self.__EventHandlers()        
        
        self.AddColumn("Main column")
        self.AddColumn("Amount", flag=wx.ALIGN_CENTER)
        self.SetMainColumn(0)
        
        _program_dir = os.path.split(__file__)[0] 
        il = wx.ImageList(24, 16)
        il.Add(wx.Bitmap(os.path.join(_program_dir, '../design/rus24x16.png'), wx.BITMAP_TYPE_PNG))
        il.Add(wx.Bitmap(os.path.join(_program_dir, '../design/ukr24x16.png'), wx.BITMAP_TYPE_PNG))
        self.AssignImageList(il)        
        
        self.root = self.AddRoot("Root")        
        self.locations = self.AppendItem(self.root, _("Location"))
        self.ct_type = check_boxes and 1 or 0
       
        self.AddCountry(self.locations, "Russia", 0) 
        self.AddCountry(self.locations, "Ukraine", 1)
        self.AddCountry(self.locations, "Unknown")     
        
        self.SelectItem(self.locations)
        self.Expand(self.locations)
        
    def AddCountry(self, node, text, flag=None):
        item = self.AppendItem(node, text, ct_type=self.ct_type)
        if flag is not None:            
            self.SetItemImage(item, flag, which=wx.TreeItemIcon_Normal)
             
    def __OnResize(self, event):        
        width = self.Parent.GetSize()[0] - 3
        column0_new_width = width * 0.8
        column1_new_width = width * 0.2
        if column1_new_width != self.GetColumnWidth(0):
            self.SetColumnWidth(0, column0_new_width)
            self.SetColumnWidth(1, column1_new_width)
        event.Skip()
        
    def __SetupExtraStyle(self):
        self.SetBuffered(True)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

    def __EventHandlers(self):
        self.Bind(wx.EVT_SIZE, self.__OnResize)
        
class ViewPanel(wx.Panel):
    def __init__(self, parent):
        super(ViewPanel, self).__init__(parent, style=wx.NO_FULL_REPAINT_ON_RESIZE)        
        
        config_path = wx.StandardPaths_Get().GetUserDataDir()
        self.mode = int(parent.config['frames'].get('mainframe_view_mode', menues.ID_SMALL_VIEW))
        self.item_size = settings.ITEM_SIZES.get(self.mode, 0)
                
        self.__MakeControls()
        self.__DoLayout()
        self.__EventHandlers()  
        
    def WidthCorrection(self):
        """
            Correct panel width according to appearance of the vertical scroll bar of the gallery.
            Dirty hack, but gallery.HasScrollbar() doesn't work.
        """
        _galleryrows_forecast = float(self.Parent.ClientSize[1] - self.toolbar.Size[1] - 2) / self.item_size
        if _galleryrows_forecast < self.gallery.table.rows:
            _scrollbar_correction = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
        else:
            _scrollbar_correction = 0
        self.SetSizeHints(self.gallery.cols_best_amount * self.item_size + _scrollbar_correction + 3, self.Parent.ClientSize[1])   
        
    def __OnToolbarPushed(self, event):
        evt_id = event.GetId()
        self.Freeze()
        self._vsizer = self.GetSizer()
        if self.mode in menues.GALLERIES:
            self._vsizer.Detach(self.gallery)        
            self.gallery.Destroy()           
            del self.gallery
        elif self.mode == menues.ID_LIST_VIEW:
            self._vsizer.Detach(self.list_view)        
            self.list_view.Destroy()           
            del self.list_view  
        self.mode = evt_id
        if settings.ITEM_SIZES.has_key(evt_id):            
            self.item_size = settings.ITEM_SIZES[evt_id]
            self.gallery = GallaryView(self, self.item_size)            
            self._vsizer.Add(self.gallery, 1, wx.EXPAND)                                                
            self._vsizer.Layout()           
            self.gallery.Reset() 
            self.WidthCorrection()
        elif evt_id == menues.ID_LIST_VIEW:
            self.list_view = ListView(self)
            self._vsizer.Add(self.list_view, 1, wx.EXPAND)                                                
            self._vsizer.Layout()           
        self.Parent.Sizer.Layout()           
        self.Thaw()
        event.Skip()
                
    def __MakeControls(self):
        self.toolbar = menues.MainViewToolbar(self, self.mode)
        if self.mode in menues.GALLERIES:
            self.gallery = GallaryView(self, self.item_size)
        else:
            self.list_view = ListView(self) 
    
    def __DoLayout(self):
        self._vsizer = wx.BoxSizer(wx.VERTICAL)
        self._vsizer.Add(self.toolbar, 0, wx.EXPAND) 
        self._vsizer.AddSpacer(3) 
        _current_view_control = hasattr(self, 'gallery') and self.gallery or self.list_view       
        self._vsizer.Add(_current_view_control, 1, wx.EXPAND) 
        self.SetSizer(self._vsizer)
        
    def __EventHandlers(self):
        self.Bind(wx.EVT_TOOL, self.__OnToolbarPushed)        
        
class ViewData(gridlib.PyGridTableBase):
    def __init__(self, item_size):
        gridlib.PyGridTableBase.__init__(self)       
            
        _program_dir = os.path.split(__file__)[0] 
        self.data = list()
        for fn in os.listdir(os.path.join(_program_dir, '../design/caps')):
            path = os.path.join(_program_dir, '../design/caps', fn)
            self.data.append(path)           
              
        self.item_size = item_size         
        self.cols = 0
        self.rows = 0       
        
    def ResetView(self, grid):
        grid.BeginBatch()        
        if self.cols > grid.cols_best_amount:
            msg = gridlib.GridTableMessage(self, gridlib.GRIDTABLE_NOTIFY_COLS_DELETED, grid.cols_best_amount, self.cols - grid.cols_best_amount)
            self.GetView().ProcessTableMessage(msg)
        elif self.cols < grid.cols_best_amount:
            msg = gridlib.GridTableMessage(self, gridlib.GRIDTABLE_NOTIFY_COLS_INSERTED, self.cols, grid.cols_best_amount - self.cols)
            self.GetView().ProcessTableMessage(msg)            
        self.cols = grid.cols_best_amount        
        if self.cols:
            rows_best_amount = ceil(float(len(self.data)) / self.cols)
        else:
            rows_best_amount = 0 
        if self.rows > rows_best_amount:
            msg = gridlib.GridTableMessage(self, gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED, rows_best_amount, self.rows - rows_best_amount)
            self.GetView().ProcessTableMessage(msg)
        elif self.rows < rows_best_amount:
            msg = gridlib.GridTableMessage(self, gridlib.GRIDTABLE_NOTIFY_ROWS_INSERTED, self.rows, rows_best_amount - self.rows)
            self.GetView().ProcessTableMessage(msg) 
        self.rows = rows_best_amount            
        grid.EndBatch()                
        
        msg = gridlib.GridTableMessage(self, gridlib.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
        grid.ProcessTableMessage(msg) 

    def GetAttr(self, row, col, kind):
        attr = gridlib.GridCellAttr() 
        attr.SetReadOnly(True)
        return attr
        
    def GetNumberRows(self):
        return self.rows        

    def GetNumberCols(self):
        return self.cols     

    def IsEmptyCell(self, row, col):
        return False

    def GetValue(self, row, col):
        return ''
    
    def GetRawValue(self, row, col):  
        return False

    def SetValue(self, row, col, value):
        return None
        
class GallaryView(gridlib.Grid):
    def __init__(self, parent, item_size):
        gridlib.Grid.__init__(self, parent, -1, style=wx.SIMPLE_BORDER)    

        self.item_size = item_size
        self.__Appearance()        
        self.table = ViewData(item_size)
        self.SetTable(self.table, True)
        self.cols_best_amount = (self.Parent.Parent.ClientSize[0] - self.Parent.Parent.navigation.MinWidth) / item_size

    def __Appearance(self):
        self.HideRowLabels()
        self.HideColLabels()          
        self.SetDefaultEditor(None)
        self.DefaultRowSize = self.item_size
        self.DefaultColSize = self.item_size 
        self.DisableDragRowSize()
        self.DisableDragColSize()
        self.SetDefaultCellBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE))
        self.ClearBackground()
        self.DefaultRenderer = ItemPictureRenderer(self.item_size)
        
    def Reset(self):
        self.table.ResetView(self)           
    
class ItemPictureRenderer(gridlib.PyGridCellRenderer):
    def __init__(self, item_size):
        gridlib.PyGridCellRenderer.__init__(self)
        
        self.item_size = item_size                 
        _sel_color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HOTLIGHT) 
        _sel_color.Set(_sel_color.red, _sel_color.green, _sel_color.blue, 92)
        self.sel_brush = wx.Brush(_sel_color)
        self.sel_pen = wx.Pen(_sel_color)        
        _bg_color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE) 
        self.bg_brush = wx.Brush(_bg_color)
        self.bg_pen = wx.Pen(_bg_color)

    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        data_index = grid.table.cols * row + col
        if data_index < len(grid.table.data):             
            bmp = wx.Bitmap(grid.table.data[data_index], wx.BITMAP_TYPE_JPEG)        
            image = wx.ImageFromBitmap(bmp)
            image = image.Scale(self.item_size, self.item_size, wx.IMAGE_QUALITY_HIGH)
            bmp = wx.BitmapFromImage(image)                       
            dc.DrawBitmap(bmp, rect.x, rect.y)
            if isSelected:
                try:
                    dc = wx.GCDC(dc)
                except:
                    pass
                else:         
                    dc.SetPen(self.sel_pen)
                    dc.SetBrush(self.sel_brush)
                    dc.DrawRectangleRect(rect)
        else:
            dc.SetPen(self.bg_pen)
            dc.SetBrush(self.bg_brush)
            dc.DrawRectangleRect(rect)
            
class ListViewCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        
class ListView(wx.Panel, listmix.ColumnSorterMixin):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)
        
        self.il = wx.ImageList(16, 16)        
        self.up = self.il.Add(resources.filter_up.GetBitmap())
        self.dn = self.il.Add(resources.filter_down.GetBitmap())
        self.list = ListViewCtrl(self, -1, style=wx.LC_REPORT | wx.SIMPLE_BORDER | wx.LC_EDIT_LABELS | wx.LC_SORT_ASCENDING)
        self.list.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        
        i = 0
        _program_dir = os.path.split(__file__)[0] 
        self.itemDataMap = {}
        for fn in os.listdir(os.path.join(_program_dir, '../design/caps')):            
            self.itemDataMap[i] = (fn, "Line {0}".format(i+1))
            i += 1            
        self.PopulateList()
            
        listmix.ColumnSorterMixin.__init__(self, 3)
        self.__DoLayout()

    def __DoLayout(self):
        sizer = wx.BoxSizer(wx.VERTICAL) 
        sizer.Add(self.list, 1, wx.EXPAND)
        self.SetSizer(sizer)        
        self.SetAutoLayout(True)

    def PopulateList(self):
        info = wx.ListItem()
        info.m_mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
        info.m_image = -1
        info.m_format = 0
        info.m_text = "File name"
        self.list.InsertColumnInfo(0, info)
        info.m_text = "Column 2"
        self.list.InsertColumnInfo(1, info) 
        for k, v in self.itemDataMap.items():
            index = self.list.InsertStringItem(sys.maxint, v[0])
            self.list.SetStringItem(index, 1, v[1])
            self.list.SetItemData(index, k)
        self.list.SetColumnWidth(0, 100)
        self.list.SetColumnWidth(1, wx.LIST_AUTOSIZE)        
        self.currentItem = 0
        
    def GetListCtrl(self):
        return self.list

    def GetSortImages(self):
        return (self.dn, self.up)
             
if __name__ == '__main__':
    class TestApp(wx.App):
        def OnInit(self):
            self.frame = MainFrame(None)
            self.SetTopWindow(self.frame)
            self.frame.Show()
            return True
    test_app = TestApp(False)
    test_app.MainLoop()