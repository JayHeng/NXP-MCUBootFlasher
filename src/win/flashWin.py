# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
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
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"NXP MCU Boot Flasher", pos = wx.DefaultPosition, size = wx.Size( 650,446 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

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
		self.m_menuItem_english = wx.MenuItem( self.m_menu_language, wx.ID_ANY, u"EN - English", wx.EmptyString, wx.ITEM_RADIO )
		self.m_menu_language.Append( self.m_menuItem_english )

		self.m_menuItem_chinese = wx.MenuItem( self.m_menu_language, wx.ID_ANY, u"ZH - 简体中文", wx.EmptyString, wx.ITEM_RADIO )
		self.m_menu_language.Append( self.m_menuItem_chinese )

		self.m_menu_view.AppendSubMenu( self.m_menu_language, u"Language/语言" )

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

		self.m_staticText_mcuDevice = wx.StaticText( self.m_panel_setup, wx.ID_ANY, u"MCU Device:", wx.DefaultPosition, wx.Size( 75,-1 ), 0 )
		self.m_staticText_mcuDevice.Wrap( -1 )

		wSizer_setup.Add( self.m_staticText_mcuDevice, 0, wx.ALL, 5 )

		m_choice_mcuDeviceChoices = [ u"i.MXRT1011", u"i.MXRT1015", u"i.MXRT1021", u"i.MXRT105x", u"i.MXRT106x", u"i.MXRT1064 SIP" ]
		self.m_choice_mcuDevice = wx.Choice( self.m_panel_setup, wx.ID_ANY, wx.DefaultPosition, wx.Size( 125,-1 ), m_choice_mcuDeviceChoices, 0 )
		self.m_choice_mcuDevice.SetSelection( 3 )
		wSizer_setup.Add( self.m_choice_mcuDevice, 0, wx.ALL, 5 )

		self.m_staticText_null1Setup = wx.StaticText( self.m_panel_setup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 220,2 ), 0 )
		self.m_staticText_null1Setup.Wrap( -1 )

		wSizer_setup.Add( self.m_staticText_null1Setup, 0, wx.ALL, 5 )

		self.m_staticText_mcuBoard = wx.StaticText( self.m_panel_setup, wx.ID_ANY, u"MCU Boards (Unlimited):", wx.DefaultPosition, wx.Size( 220,-1 ), 0 )
		self.m_staticText_mcuBoard.Wrap( -1 )

		wSizer_setup.Add( self.m_staticText_mcuBoard, 0, wx.ALL, 5 )

		self.m_staticText_null2Setup = wx.StaticText( self.m_panel_setup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 5,-1 ), 0 )
		self.m_staticText_null2Setup.Wrap( -1 )

		wSizer_setup.Add( self.m_staticText_null2Setup, 0, wx.ALL, 5 )

		self.m_staticText_connectedBoards = wx.StaticText( self.m_panel_setup, wx.ID_ANY, u"Connected:", wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		self.m_staticText_connectedBoards.Wrap( -1 )

		wSizer_setup.Add( self.m_staticText_connectedBoards, 0, wx.ALL, 5 )

		self.m_textCtrl_connectedBoards = wx.TextCtrl( self.m_panel_setup, wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_PROCESS_ENTER )
		wSizer_setup.Add( self.m_textCtrl_connectedBoards, 0, wx.ALL, 5 )

		self.m_staticText_detectedBoards = wx.StaticText( self.m_panel_setup, wx.ID_ANY, u"Detected:", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		self.m_staticText_detectedBoards.Wrap( -1 )

		wSizer_setup.Add( self.m_staticText_detectedBoards, 0, wx.ALL, 5 )

		self.m_staticText_detectedBoardNum = wx.StaticText( self.m_panel_setup, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 20,-1 ), 0 )
		self.m_staticText_detectedBoardNum.Wrap( -1 )

		wSizer_setup.Add( self.m_staticText_detectedBoardNum, 0, wx.ALL, 5 )

		self.m_staticText_null3Setup = wx.StaticText( self.m_panel_setup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 220,2 ), 0 )
		self.m_staticText_null3Setup.Wrap( -1 )

		wSizer_setup.Add( self.m_staticText_null3Setup, 0, wx.ALL, 5 )

		self.m_staticText_serialPortIndex = wx.StaticText( self.m_panel_setup, wx.ID_ANY, u"MCU Port Idx:", wx.DefaultPosition, wx.Size( 75,-1 ), 0 )
		self.m_staticText_serialPortIndex.Wrap( -1 )

		wSizer_setup.Add( self.m_staticText_serialPortIndex, 0, wx.ALL, 5 )

		m_choice_serialPortIndexChoices = [ u"0" ]
		self.m_choice_serialPortIndex = wx.Choice( self.m_panel_setup, wx.ID_ANY, wx.DefaultPosition, wx.Size( 40,-1 ), m_choice_serialPortIndexChoices, 0 )
		self.m_choice_serialPortIndex.SetSelection( 0 )
		wSizer_setup.Add( self.m_choice_serialPortIndex, 0, wx.ALL, 5 )

		self.m_staticText_portInfo = wx.StaticText( self.m_panel_setup, wx.ID_ANY, u"N/A", wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		self.m_staticText_portInfo.Wrap( -1 )

		wSizer_setup.Add( self.m_staticText_portInfo, 0, wx.ALL, 5 )

		self.m_staticText_null4Setup = wx.StaticText( self.m_panel_setup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 20,-1 ), 0 )
		self.m_staticText_null4Setup.Wrap( -1 )

		wSizer_setup.Add( self.m_staticText_null4Setup, 0, wx.ALL, 5 )

		self.m_radioBtn_uart = wx.RadioButton( self.m_panel_setup, wx.ID_ANY, u"UART", wx.DefaultPosition, wx.DefaultSize, 0 )
		wSizer_setup.Add( self.m_radioBtn_uart, 0, wx.ALL, 5 )

		self.m_staticText_null5Setup = wx.StaticText( self.m_panel_setup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 20,-1 ), 0 )
		self.m_staticText_null5Setup.Wrap( -1 )

		wSizer_setup.Add( self.m_staticText_null5Setup, 0, wx.ALL, 5 )

		self.m_radioBtn_usbhid = wx.RadioButton( self.m_panel_setup, wx.ID_ANY, u"USB-HID", wx.DefaultPosition, wx.DefaultSize, 0 )
		wSizer_setup.Add( self.m_radioBtn_usbhid, 0, wx.ALL, 5 )

		self.m_staticText_portVid = wx.StaticText( self.m_panel_setup, wx.ID_ANY, u"COM Port:", wx.DefaultPosition, wx.Size( 75,-1 ), 0 )
		self.m_staticText_portVid.Wrap( -1 )

		wSizer_setup.Add( self.m_staticText_portVid, 0, wx.ALL, 5 )

		m_choice_portVidChoices = []
		self.m_choice_portVid = wx.Choice( self.m_panel_setup, wx.ID_ANY, wx.DefaultPosition, wx.Size( 125,-1 ), m_choice_portVidChoices, 0 )
		self.m_choice_portVid.SetSelection( 0 )
		wSizer_setup.Add( self.m_choice_portVid, 0, wx.ALL, 5 )

		self.m_staticText_baudPid = wx.StaticText( self.m_panel_setup, wx.ID_ANY, u"Baudrate:", wx.DefaultPosition, wx.Size( 75,-1 ), 0 )
		self.m_staticText_baudPid.Wrap( -1 )

		wSizer_setup.Add( self.m_staticText_baudPid, 0, wx.ALL, 5 )

		m_choice_baudPidChoices = []
		self.m_choice_baudPid = wx.Choice( self.m_panel_setup, wx.ID_ANY, wx.DefaultPosition, wx.Size( 125,-1 ), m_choice_baudPidChoices, 0 )
		self.m_choice_baudPid.SetSelection( 0 )
		wSizer_setup.Add( self.m_choice_baudPid, 0, wx.ALL, 5 )

		self.m_staticText_null6Setup = wx.StaticText( self.m_panel_setup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 220,1 ), 0 )
		self.m_staticText_null6Setup.Wrap( -1 )

		wSizer_setup.Add( self.m_staticText_null6Setup, 0, wx.ALL, 5 )

		self.m_staticText_null7Setup = wx.StaticText( self.m_panel_setup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 60,1 ), 0 )
		self.m_staticText_null7Setup.Wrap( -1 )

		wSizer_setup.Add( self.m_staticText_null7Setup, 0, wx.ALL, 5 )

		self.m_bitmap_nxp = wx.StaticBitmap( self.m_panel_setup, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 80,30 ), 0 )
		wSizer_setup.Add( self.m_bitmap_nxp, 0, wx.ALL, 5 )


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

		self.m_staticText_appPath = wx.StaticText( self.m_panel_download, wx.ID_ANY, u"Application Image File (.sb) / Folder:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_appPath.Wrap( -1 )

		wSizer_download.Add( self.m_staticText_appPath, 0, wx.ALL, 5 )

		self.m_filePicker_appFilePath = wx.FilePickerCtrl( self.m_panel_download, wx.ID_ANY, u"Select a file", u"Select a file", u"*.*", wx.DefaultPosition, wx.Size( 340,-1 ), wx.FLP_DEFAULT_STYLE )
		wSizer_download.Add( self.m_filePicker_appFilePath, 0, wx.ALL, 5 )

		self.m_dirPicker_appFolderPath = wx.DirPickerCtrl( self.m_panel_download, wx.ID_ANY, u"Select a folder", u"Select a folder", wx.DefaultPosition, wx.Size( 340,-1 ), wx.DIRP_DEFAULT_STYLE )
		wSizer_download.Add( self.m_dirPicker_appFolderPath, 0, wx.ALL, 5 )

		self.m_staticText_null1Download = wx.StaticText( self.m_panel_download, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 105,-1 ), 0 )
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

		self.m_gauge_action = wx.Gauge( self.m_panel_download, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 270,20 ), wx.GA_HORIZONTAL )
		self.m_gauge_action.SetValue( 100 )
		wSizer_download.Add( self.m_gauge_action, 0, wx.ALL, 5 )

		self.m_staticText_null3Download = wx.StaticText( self.m_panel_download, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 38,-1 ), 0 )
		self.m_staticText_null3Download.Wrap( -1 )

		wSizer_download.Add( self.m_staticText_null3Download, 0, wx.ALL, 5 )

		self.m_staticText_successfulBoards = wx.StaticText( self.m_panel_download, wx.ID_ANY, u"Successful Boards:", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		self.m_staticText_successfulBoards.Wrap( -1 )

		wSizer_download.Add( self.m_staticText_successfulBoards, 0, wx.ALL, 5 )

		self.m_staticText_successfulBoardNum = wx.StaticText( self.m_panel_download, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 20,-1 ), 0 )
		self.m_staticText_successfulBoardNum.Wrap( -1 )

		wSizer_download.Add( self.m_staticText_successfulBoardNum, 0, wx.ALL, 5 )

		self.m_staticText_failedBoards = wx.StaticText( self.m_panel_download, wx.ID_ANY, u"Failed Boards:", wx.DefaultPosition, wx.Size( 90,-1 ), 0 )
		self.m_staticText_failedBoards.Wrap( -1 )

		wSizer_download.Add( self.m_staticText_failedBoards, 0, wx.ALL, 5 )

		self.m_staticText_failedBoardNum = wx.StaticText( self.m_panel_download, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 20,-1 ), 0 )
		self.m_staticText_failedBoardNum.Wrap( -1 )

		wSizer_download.Add( self.m_staticText_failedBoardNum, 0, wx.ALL, 5 )

		self.m_staticText_null4Download = wx.StaticText( self.m_panel_download, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 260,2 ), 0 )
		self.m_staticText_null4Download.Wrap( -1 )

		wSizer_download.Add( self.m_staticText_null4Download, 0, wx.ALL, 5 )


		self.m_panel_download.SetSizer( wSizer_download )
		self.m_panel_download.Layout()
		wSizer_download.Fit( self.m_panel_download )
		self.m_notebook_download.AddPage( self.m_panel_download, u"Download", False )

		bSizer_download.Add( self.m_notebook_download, 1, wx.EXPAND |wx.ALL, 5 )

		wSizer_logo = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		self.m_button_slot0 = wx.Button( self, wx.ID_ANY, u"slot0", wx.DefaultPosition, wx.Size( 80,40 ), 0 )
		wSizer_logo.Add( self.m_button_slot0, 0, wx.ALL, 5 )

		self.m_button_slot1 = wx.Button( self, wx.ID_ANY, u"slot1", wx.DefaultPosition, wx.Size( 80,40 ), 0 )
		wSizer_logo.Add( self.m_button_slot1, 0, wx.ALL, 5 )

		self.m_button_slot2 = wx.Button( self, wx.ID_ANY, u"slot2", wx.DefaultPosition, wx.Size( 80,40 ), 0 )
		wSizer_logo.Add( self.m_button_slot2, 0, wx.ALL, 5 )

		self.m_button_slot3 = wx.Button( self, wx.ID_ANY, u"slot3", wx.DefaultPosition, wx.Size( 80,40 ), 0 )
		wSizer_logo.Add( self.m_button_slot3, 0, wx.ALL, 5 )

		self.m_button_slot4 = wx.Button( self, wx.ID_ANY, u"slot4", wx.DefaultPosition, wx.Size( 80,40 ), 0 )
		wSizer_logo.Add( self.m_button_slot4, 0, wx.ALL, 5 )

		self.m_button_slot5 = wx.Button( self, wx.ID_ANY, u"slot5", wx.DefaultPosition, wx.Size( 80,40 ), 0 )
		wSizer_logo.Add( self.m_button_slot5, 0, wx.ALL, 5 )

		self.m_button_slot6 = wx.Button( self, wx.ID_ANY, u"slot6", wx.DefaultPosition, wx.Size( 80,40 ), 0 )
		wSizer_logo.Add( self.m_button_slot6, 0, wx.ALL, 5 )

		self.m_button_slot7 = wx.Button( self, wx.ID_ANY, u"slot7", wx.DefaultPosition, wx.Size( 80,40 ), 0 )
		wSizer_logo.Add( self.m_button_slot7, 0, wx.ALL, 5 )


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
		self.m_textCtrl_connectedBoards.Bind( wx.EVT_TEXT_ENTER, self.callbackSetConnectedBoards )
		self.m_choice_serialPortIndex.Bind( wx.EVT_CHOICE, self.callbackSwitchSerialPortIndex )
		self.m_radioBtn_uart.Bind( wx.EVT_RADIOBUTTON, self.callbackSetUartPort )
		self.m_radioBtn_usbhid.Bind( wx.EVT_RADIOBUTTON, self.callbackSetUsbhidPort )
		self.m_choice_portVid.Bind( wx.EVT_CHOICE, self.callbackSetPortVid )
		self.m_choice_baudPid.Bind( wx.EVT_CHOICE, self.callbackSetBaudPid )
		self.m_filePicker_appFilePath.Bind( wx.EVT_FILEPICKER_CHANGED, self.callbackChangedAppFile )
		self.m_dirPicker_appFolderPath.Bind( wx.EVT_DIRPICKER_CHANGED, self.callbackChangedAppFolder )
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

	def callbackSetConnectedBoards( self, event ):
		event.Skip()

	def callbackSwitchSerialPortIndex( self, event ):
		event.Skip()

	def callbackSetUartPort( self, event ):
		event.Skip()

	def callbackSetUsbhidPort( self, event ):
		event.Skip()

	def callbackSetPortVid( self, event ):
		event.Skip()

	def callbackSetBaudPid( self, event ):
		event.Skip()

	def callbackChangedAppFile( self, event ):
		event.Skip()

	def callbackChangedAppFolder( self, event ):
		event.Skip()

	def callbackAllInOneAction( self, event ):
		event.Skip()


