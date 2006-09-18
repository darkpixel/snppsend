# -*- coding: UTF-8 -*-

import wx

class SNPPWindow(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.label_1 = wx.StaticText(self, -1, "MENUBAR GOES HERE RETARD!")
        self.receivers = wx.ListBox(self, -1, choices=["darkpixel", "dorko", "maven", "dip", "", "", "", ""], style=wx.LB_MULTIPLE)
        self.message = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_WORDWRAP)
        self.label_2 = wx.StaticText(self, -1, "STATUSBAR GOES HERE MORON!")

        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        self.SetTitle("frame_1")
        self.receivers.SetSelection(0)

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.label_1, 0, wx.ADJUST_MINSIZE, 0)
        sizer_3.Add(self.receivers, 0, wx.EXPAND|wx.FIXED_MINSIZE, 0)
        sizer_3.Add(self.message, 0, wx.EXPAND, 0)
        sizer_2.Add(sizer_3, 1, wx.EXPAND, 0)
        sizer_2.Add(self.label_2, 0, wx.ADJUST_MINSIZE, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        sizer_1.SetSizeHints(self)
        self.Layout()

# end of class SNPPWindow


