# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Aug  8 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class flashWin
###########################################################################

class flashWin ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"RT Flash", pos = wx.DefaultPosition, size = wx.Size( 500,255 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVECAPTION ) )

		self.m_menubar = wx.MenuBar( 0 )
		self.m_menu_file = wx.Menu()
		self.m_menuItem_exit = wx.MenuItem( self.m_menu_file, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_file.Append( self.m_menuItem_exit )

		self.m_menubar.Append( self.m_menu_file, u"File" )

		self.m_menu_help = wx.Menu()
		self.m_menuItem_homePage = wx.MenuItem( self.m_menu_help, wx.ID_ANY, u"Home Page", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_help.Append( self.m_menuItem_homePage )

		self.m_menuItem_aboutAuthor = wx.MenuItem( self.m_menu_help, wx.ID_ANY, u"About Author", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_help.Append( self.m_menuItem_aboutAuthor )

		self.m_menuItem_revisionHistory = wx.MenuItem( self.m_menu_help, wx.ID_ANY, u"Revision History", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_help.Append( self.m_menuItem_revisionHistory )

		self.m_menubar.Append( self.m_menu_help, u"Help" )

		self.SetMenuBar( self.m_menubar )

		bSizer_win = wx.BoxSizer( wx.VERTICAL )

		wSizer_func = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		bSizer_setup = wx.BoxSizer( wx.VERTICAL )

		sbSizer_setup = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, wx.EmptyString ), wx.VERTICAL )

		self.m_staticText_mcuDevice = wx.StaticText( sbSizer_setup.GetStaticBox(), wx.ID_ANY, u"i.MX RT Device:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_mcuDevice.Wrap( -1 )

		sbSizer_setup.Add( self.m_staticText_mcuDevice, 0, wx.ALL, 5 )

		m_choice_mcuDeviceChoices = [ u"i.MXRT1015", u"i.MXRT102x", u"i.MXRT105x", u"i.MXRT106x", u"i.MXRT1064 SIP" ]
		self.m_choice_mcuDevice = wx.Choice( sbSizer_setup.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 180,-1 ), m_choice_mcuDeviceChoices, 0 )
		self.m_choice_mcuDevice.SetSelection( 2 )
		sbSizer_setup.Add( self.m_choice_mcuDevice, 0, wx.ALL, 5 )

		self.m_staticText_usbPort = wx.StaticText( sbSizer_setup.GetStaticBox(), wx.ID_ANY, u"Download Port:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_usbPort.Wrap( -1 )

		sbSizer_setup.Add( self.m_staticText_usbPort, 0, wx.ALL, 5 )

		self.m_textCtrl_usbPort = wx.TextCtrl( sbSizer_setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 180,-1 ), 0 )
		sbSizer_setup.Add( self.m_textCtrl_usbPort, 0, wx.ALL, 5 )


		bSizer_setup.Add( sbSizer_setup, 1, wx.EXPAND, 5 )


		wSizer_func.Add( bSizer_setup, 1, wx.EXPAND, 5 )

		bSizer_flash = wx.BoxSizer( wx.VERTICAL )

		sbSizer_flash = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, wx.EmptyString ), wx.VERTICAL )

		self.m_staticText_appPath = wx.StaticText( sbSizer_flash.GetStaticBox(), wx.ID_ANY, u"Application Image File(.sb):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_appPath.Wrap( -1 )

		sbSizer_flash.Add( self.m_staticText_appPath, 0, wx.ALL, 5 )

		self.m_filePicker_appPath = wx.FilePickerCtrl( sbSizer_flash.GetStaticBox(), wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.Size( 260,-1 ), wx.FLP_DEFAULT_STYLE )
		sbSizer_flash.Add( self.m_filePicker_appPath, 0, wx.ALL, 5 )

		self.m_button_allInOneAction = wx.Button( sbSizer_flash.GetStaticBox(), wx.ID_ANY, u"All-In-One Action", wx.DefaultPosition, wx.Size( 120,40 ), 0 )
		self.m_button_allInOneAction.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		sbSizer_flash.Add( self.m_button_allInOneAction, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		bSizer_flash.Add( sbSizer_flash, 1, wx.EXPAND, 5 )


		wSizer_func.Add( bSizer_flash, 1, wx.EXPAND, 5 )

		wSizer_info = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		self.m_staticText_costTime = wx.StaticText( self, wx.ID_ANY, u" 00:00:00", wx.DefaultPosition, wx.Size( 45,-1 ), 0 )
		self.m_staticText_costTime.Wrap( -1 )

		wSizer_info.Add( self.m_staticText_costTime, 0, wx.ALL, 5 )

		self.m_gauge_action = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 335,20 ), wx.GA_HORIZONTAL )
		self.m_gauge_action.SetValue( 100 )
		wSizer_info.Add( self.m_gauge_action, 0, wx.ALL, 5 )

		self.m_bitmap_nxp = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 80,30 ), 0 )
		wSizer_info.Add( self.m_bitmap_nxp, 0, wx.ALL, 5 )


		wSizer_func.Add( wSizer_info, 1, wx.EXPAND, 5 )


		bSizer_win.Add( wSizer_func, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer_win )
		self.Layout()
		self.m_statusBar = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.callbackClose )
		self.Bind( wx.EVT_MENU, self.callbackExit, id = self.m_menuItem_exit.GetId() )
		self.Bind( wx.EVT_MENU, self.callbackShowHomePage, id = self.m_menuItem_homePage.GetId() )
		self.Bind( wx.EVT_MENU, self.callbackShowAboutAuthor, id = self.m_menuItem_aboutAuthor.GetId() )
		self.Bind( wx.EVT_MENU, self.callbackShowRevisionHistory, id = self.m_menuItem_revisionHistory.GetId() )
		self.m_choice_mcuDevice.Bind( wx.EVT_CHOICE, self.callbackSetMcuDevice )
		self.m_filePicker_appPath.Bind( wx.EVT_FILEPICKER_CHANGED, self.callbackChangedAppFile )
		self.m_button_allInOneAction.Bind( wx.EVT_BUTTON, self.callbackAllInOneAction )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def callbackClose( self, event ):
		event.Skip()

	def callbackExit( self, event ):
		event.Skip()

	def callbackShowHomePage( self, event ):
		event.Skip()

	def callbackShowAboutAuthor( self, event ):
		event.Skip()

	def callbackShowRevisionHistory( self, event ):
		event.Skip()

	def callbackSetMcuDevice( self, event ):
		event.Skip()

	def callbackChangedAppFile( self, event ):
		event.Skip()

	def callbackAllInOneAction( self, event ):
		event.Skip()


