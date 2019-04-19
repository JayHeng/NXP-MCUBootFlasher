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
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"RT Flash", pos = wx.DefaultPosition, size = wx.Size( 528,309 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		self.m_menubar = wx.MenuBar( 0 )
		self.m_menu_file = wx.Menu()
		self.m_menuItem_exit = wx.MenuItem( self.m_menu_file, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_file.Append( self.m_menuItem_exit )

		self.m_menubar.Append( self.m_menu_file, u"File" )

		self.m_menu_edit = wx.Menu()
		self.m_menubar.Append( self.m_menu_edit, u"Edit" )

		self.m_menu_view = wx.Menu()
		self.m_menu_language = wx.Menu()
		self.m_menuItem_english = wx.MenuItem( self.m_menu_language, wx.ID_ANY, u"English", wx.EmptyString, wx.ITEM_RADIO )
		self.m_menu_language.Append( self.m_menuItem_english )

		self.m_menuItem_chinese = wx.MenuItem( self.m_menu_language, wx.ID_ANY, u"Chinese", wx.EmptyString, wx.ITEM_RADIO )
		self.m_menu_language.Append( self.m_menuItem_chinese )

		self.m_menu_view.AppendSubMenu( self.m_menu_language, u"Language" )

		self.m_menubar.Append( self.m_menu_view, u"View" )

		self.m_menu_tools = wx.Menu()
		self.m_menu_usbDetection = wx.Menu()
		self.m_menuItem_usbDetectionDynamic = wx.MenuItem( self.m_menu_usbDetection, wx.ID_ANY, u"Dynamic", wx.EmptyString, wx.ITEM_RADIO )
		self.m_menu_usbDetection.Append( self.m_menuItem_usbDetectionDynamic )

		self.m_menuItem_usbDetectionStatic = wx.MenuItem( self.m_menu_usbDetection, wx.ID_ANY, u"Static", wx.EmptyString, wx.ITEM_RADIO )
		self.m_menu_usbDetection.Append( self.m_menuItem_usbDetectionStatic )

		self.m_menu_tools.AppendSubMenu( self.m_menu_usbDetection, u"USB Detection" )

		self.m_menubar.Append( self.m_menu_tools, u"Tools" )

		self.m_menu_window = wx.Menu()
		self.m_menubar.Append( self.m_menu_window, u"Window" )

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

		self.m_notebook_setup = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel_setup = wx.Panel( self.m_notebook_setup, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		wSizer_setup = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		self.m_staticText_mcuDevice = wx.StaticText( self.m_panel_setup, wx.ID_ANY, u"RT Device:", wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		self.m_staticText_mcuDevice.Wrap( -1 )

		wSizer_setup.Add( self.m_staticText_mcuDevice, 0, wx.ALL, 5 )

		m_choice_mcuDeviceChoices = [ u"i.MXRT1015", u"i.MXRT102x", u"i.MXRT105x", u"i.MXRT106x", u"i.MXRT1064 SIP" ]
		self.m_choice_mcuDevice = wx.Choice( self.m_panel_setup, wx.ID_ANY, wx.DefaultPosition, wx.Size( 110,-1 ), m_choice_mcuDeviceChoices, 0 )
		self.m_choice_mcuDevice.SetSelection( 2 )
		wSizer_setup.Add( self.m_choice_mcuDevice, 0, wx.ALL, 5 )

		self.m_staticText_null1Setup = wx.StaticText( self.m_panel_setup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 180,5 ), 0 )
		self.m_staticText_null1Setup.Wrap( -1 )

		wSizer_setup.Add( self.m_staticText_null1Setup, 0, wx.ALL, 5 )

		self.m_staticText_serialPort = wx.StaticText( self.m_panel_setup, wx.ID_ANY, u"Serial Port:", wx.DefaultPosition, wx.Size( 180,-1 ), 0 )
		self.m_staticText_serialPort.Wrap( -1 )

		wSizer_setup.Add( self.m_staticText_serialPort, 0, wx.ALL, 5 )

		self.m_staticText_null2Setup = wx.StaticText( self.m_panel_setup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 14,-1 ), 0 )
		self.m_staticText_null2Setup.Wrap( -1 )

		wSizer_setup.Add( self.m_staticText_null2Setup, 0, wx.ALL, 5 )

		self.m_radioBtn_uart = wx.RadioButton( self.m_panel_setup, wx.ID_ANY, u"UART", wx.DefaultPosition, wx.DefaultSize, 0 )
		wSizer_setup.Add( self.m_radioBtn_uart, 0, wx.ALL, 5 )

		self.m_radioBtn_usbhid = wx.RadioButton( self.m_panel_setup, wx.ID_ANY, u"USB-HID", wx.DefaultPosition, wx.DefaultSize, 0 )
		wSizer_setup.Add( self.m_radioBtn_usbhid, 0, wx.ALL, 5 )

		self.m_staticText_portVid = wx.StaticText( self.m_panel_setup, wx.ID_ANY, u"COM Port:", wx.DefaultPosition, wx.Size( 75,-1 ), 0 )
		self.m_staticText_portVid.Wrap( -1 )

		wSizer_setup.Add( self.m_staticText_portVid, 0, wx.ALL, 5 )

		m_choice_portVidChoices = []
		self.m_choice_portVid = wx.Choice( self.m_panel_setup, wx.ID_ANY, wx.DefaultPosition, wx.Size( 95,-1 ), m_choice_portVidChoices, 0 )
		self.m_choice_portVid.SetSelection( 0 )
		wSizer_setup.Add( self.m_choice_portVid, 0, wx.ALL, 5 )

		self.m_staticText_baudPid = wx.StaticText( self.m_panel_setup, wx.ID_ANY, u"Baudrate:", wx.DefaultPosition, wx.Size( 75,-1 ), 0 )
		self.m_staticText_baudPid.Wrap( -1 )

		wSizer_setup.Add( self.m_staticText_baudPid, 0, wx.ALL, 5 )

		m_choice_baudPidChoices = []
		self.m_choice_baudPid = wx.Choice( self.m_panel_setup, wx.ID_ANY, wx.DefaultPosition, wx.Size( 95,-1 ), m_choice_baudPidChoices, 0 )
		self.m_choice_baudPid.SetSelection( 0 )
		wSizer_setup.Add( self.m_choice_baudPid, 0, wx.ALL, 5 )


		self.m_panel_setup.SetSizer( wSizer_setup )
		self.m_panel_setup.Layout()
		wSizer_setup.Fit( self.m_panel_setup )
		self.m_notebook_setup.AddPage( self.m_panel_setup, u"Setup", False )

		bSizer_setup.Add( self.m_notebook_setup, 1, wx.EXPAND |wx.ALL, 5 )


		wSizer_func.Add( bSizer_setup, 1, wx.EXPAND, 5 )

		bSizer_download = wx.BoxSizer( wx.VERTICAL )

		self.m_notebook_download = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel_download = wx.Panel( self.m_notebook_download, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		wSizer_download = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		self.m_staticText_appPath = wx.StaticText( self.m_panel_download, wx.ID_ANY, u"Application Image File (.sb):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_appPath.Wrap( -1 )

		wSizer_download.Add( self.m_staticText_appPath, 0, wx.ALL, 5 )

		self.m_filePicker_appPath = wx.FilePickerCtrl( self.m_panel_download, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.Size( 260,-1 ), wx.FLP_DEFAULT_STYLE )
		wSizer_download.Add( self.m_filePicker_appPath, 0, wx.ALL, 5 )

		self.m_staticText_null1Download = wx.StaticText( self.m_panel_download, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		self.m_staticText_null1Download.Wrap( -1 )

		wSizer_download.Add( self.m_staticText_null1Download, 0, wx.ALL, 5 )

		self.m_button_allInOneAction = wx.Button( self.m_panel_download, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.Size( 120,40 ), 0 )
		self.m_button_allInOneAction.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		wSizer_download.Add( self.m_button_allInOneAction, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_staticText_null2Download = wx.StaticText( self.m_panel_download, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		self.m_staticText_null2Download.Wrap( -1 )

		wSizer_download.Add( self.m_staticText_null2Download, 0, wx.ALL, 5 )

		self.m_staticText_costTime = wx.StaticText( self.m_panel_download, wx.ID_ANY, u" 00:00.000", wx.DefaultPosition, wx.Size( 55,-1 ), 0 )
		self.m_staticText_costTime.Wrap( -1 )

		wSizer_download.Add( self.m_staticText_costTime, 0, wx.ALL, 5 )

		self.m_gauge_action = wx.Gauge( self.m_panel_download, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 190,20 ), wx.GA_HORIZONTAL )
		self.m_gauge_action.SetValue( 100 )
		wSizer_download.Add( self.m_gauge_action, 0, wx.ALL, 5 )


		self.m_panel_download.SetSizer( wSizer_download )
		self.m_panel_download.Layout()
		wSizer_download.Fit( self.m_panel_download )
		self.m_notebook_download.AddPage( self.m_panel_download, u"Download", False )

		bSizer_download.Add( self.m_notebook_download, 1, wx.EXPAND |wx.ALL, 5 )

		wSizer_logo = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		self.m_staticText_null1Logo = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 180,-1 ), 0 )
		self.m_staticText_null1Logo.Wrap( -1 )

		wSizer_logo.Add( self.m_staticText_null1Logo, 0, wx.ALL, 5 )

		self.m_bitmap_nxp = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 80,30 ), 0 )
		wSizer_logo.Add( self.m_bitmap_nxp, 0, wx.ALL, 5 )


		bSizer_download.Add( wSizer_logo, 1, wx.EXPAND, 5 )


		wSizer_func.Add( bSizer_download, 1, wx.EXPAND, 5 )


		bSizer_win.Add( wSizer_func, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer_win )
		self.Layout()
		self.m_statusBar = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.callbackClose )
		self.Bind( wx.EVT_MENU, self.callbackExit, id = self.m_menuItem_exit.GetId() )
		self.Bind( wx.EVT_MENU, self.callbackSetLanguageAsEnglish, id = self.m_menuItem_english.GetId() )
		self.Bind( wx.EVT_MENU, self.callbackSetLanguageAsChinese, id = self.m_menuItem_chinese.GetId() )
		self.Bind( wx.EVT_MENU, self.callbackSetUsbDetectionAsDynamic, id = self.m_menuItem_usbDetectionDynamic.GetId() )
		self.Bind( wx.EVT_MENU, self.callbackSetUsbDetectionAsStatic, id = self.m_menuItem_usbDetectionStatic.GetId() )
		self.Bind( wx.EVT_MENU, self.callbackShowHomePage, id = self.m_menuItem_homePage.GetId() )
		self.Bind( wx.EVT_MENU, self.callbackShowAboutAuthor, id = self.m_menuItem_aboutAuthor.GetId() )
		self.Bind( wx.EVT_MENU, self.callbackShowRevisionHistory, id = self.m_menuItem_revisionHistory.GetId() )
		self.m_choice_mcuDevice.Bind( wx.EVT_CHOICE, self.callbackSetMcuDevice )
		self.m_radioBtn_uart.Bind( wx.EVT_RADIOBUTTON, self.callbackSetUartPort )
		self.m_radioBtn_usbhid.Bind( wx.EVT_RADIOBUTTON, self.callbackSetUsbhidPort )
		self.m_filePicker_appPath.Bind( wx.EVT_FILEPICKER_CHANGED, self.callbackChangedAppFile )
		self.m_button_allInOneAction.Bind( wx.EVT_BUTTON, self.callbackAllInOneAction )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def callbackClose( self, event ):
		event.Skip()

	def callbackExit( self, event ):
		event.Skip()

	def callbackSetLanguageAsEnglish( self, event ):
		event.Skip()

	def callbackSetLanguageAsChinese( self, event ):
		event.Skip()

	def callbackSetUsbDetectionAsDynamic( self, event ):
		event.Skip()

	def callbackSetUsbDetectionAsStatic( self, event ):
		event.Skip()

	def callbackShowHomePage( self, event ):
		event.Skip()

	def callbackShowAboutAuthor( self, event ):
		event.Skip()

	def callbackShowRevisionHistory( self, event ):
		event.Skip()

	def callbackSetMcuDevice( self, event ):
		event.Skip()

	def callbackSetUartPort( self, event ):
		event.Skip()

	def callbackSetUsbhidPort( self, event ):
		event.Skip()

	def callbackChangedAppFile( self, event ):
		event.Skip()

	def callbackAllInOneAction( self, event ):
		event.Skip()


