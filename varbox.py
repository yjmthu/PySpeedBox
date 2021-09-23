from ctypes import pointer, windll, cdll, sizeof
import os

from PySide6.QtGui import QColor, QGuiApplication
from PySide6.QtCore import QDir, QPoint, QStandardPaths, QSettings, QTimer
from PySide6.QtWidgets import QMessageBox

from funcbox import *
from form import Form
from dialog import Dialog
from menu import Menu
from wallpaper import Wallpaper

class VarBox:

    TYPE_IN_DEFAULT, TYPE_IN_CODE, TYPE_MS_BING, TYPE_PC_NATIVE, TYPE_PY_CMD = range(5)

    def __init__(self) -> None:
        screen = QGuiApplication.primaryScreen().geometry()
        self.ScreenWidth, self.ScreenHeight = screen.width(), screen.height()
        self.initSpeedBox()
        self.initChildren()
        self.initConnections()
        self.initBehaviors()
    
    def initSpeedBox(self):
        main_folder = get_dat_path()
        ini_file = os.path.join(main_folder, "PySpeedBox.ini")
        if os.path.exists(ini_file):
            IniRead = QSettings(ini_file, QSettings.IniFormat)
            self.appfirstUse = False
            self.appRun = True

            IniRead.beginGroup("Wallpaper")
            self.paperHistory = list()
            self.paperCur = 0
            self.paperChangeWhenStart: bool = IniRead.value("paperChangeWhenStart", False, bool)
            self.paperAutoChange: bool = IniRead.value("paperAutoChange", False, bool)
            self.paperTimeInterval: int = IniRead.value("paperTimeInterval", 15, int)
            self.paperType = IniRead.value("paperType", VarBox.TYPE_MS_BING, int)
            self.paperNativeDir: str = QDir.toNativeSeparators(QStandardPaths.writableLocation(QStandardPaths.PicturesLocation))
            self.paperNativeDir: str = IniRead.value("paperNativeDir", self.paperNativeDir, str)
            self.paperHistory.append(QSettings("HKEY_CURRENT_USER\\Control Panel\\Desktop", QSettings.NativeFormat).value("WallPaper", None, str))
            IniRead.endGroup()

            IniRead.beginGroup("Bing")
            self.bingDateAsName: bool = IniRead.value("bingDateAsName", True, bool)
            self.bingAutoSave: bool = IniRead.value("bingAutoSave", True, bool)
            self.bingAutoRotation: bool = IniRead.value("bingAutoRotation", True, bool)
            IniRead.endGroup()

            IniRead.beginGroup("Dialog")
            r, g, b, a = IniRead.value("dialogUiThemeR", 8, int), IniRead.value("dialogUiThemeG", 8, int), IniRead.value("dialogUiThemeB", 8, int), IniRead.value("dialogUiThemeA", 8, int)
            self.dialogUiTheme = QColor(r, g, b, a)
            IniRead.endGroup()
            
            IniRead.beginGroup("Form")
            self.formUiPos = QPoint(IniRead.value("formUiPosX", 100, int), IniRead.value("formUiPosY", 100, int))
            IniRead.endGroup()

            IniRead.beginGroup("Translation")
            self.fanyerEnabled = IniRead.value("fanyerEnabled", False, bool)
            self.fanyerAutoHide = IniRead.value("fanyerAutoHide", True, bool)
            self.fanyerAppId = IniRead.value("fanyerAppId", "20210503000812254", str)
            self.fanyerPassWord = IniRead.value("fanyerPassWord", "Q_2PPxmCr66r6B2hi0ts", str)
            IniRead.endGroup()

            IniRead.beginGroup("Others")
            self.controlDesktopIcon = IniRead.value("controlDesktopIcon", False, bool)
            IniRead.endGroup()
        else:
            self.appfirstUse = True
            self.appRun = True

            self.paperHistory = list()
            self.paperCur = 0
            self.paperChangeWhenStart = False
            self.paperAutoChange = False
            self.paperTimeInterval = 15
            self.paperType = VarBox.TYPE_MS_BING
            self.paperNativeDir = QDir.toNativeSeparators(QStandardPaths.writableLocation(QStandardPaths.PicturesLocation))
            self.paperHistory.append(QSettings("HKEY_CURRENT_USER\\Control Panel\\Desktop", QSettings.NativeFormat).value("WallPaper", None, str))

            self.bingDateAsName = True
            self.bingAutoSave = True
            self.bingAutoRotation = True

            self.dialogUiTheme = QColor(8, 8, 8, 8)
            
            self.formUiPos = QPoint(100, 100)

            self.fanyerEnabled = False
            self.fanyerAutoHide = True
            self.fanyerAppId = "20210503000812254"
            self.fanyerPassWord =  "Q_2PPxmCr66r6B2hi0ts"

            self.controlDesktopIcon = False

            IniWrite = QSettings(ini_file, QSettings.IniFormat)
            IniWrite.beginGroup("Wallpaper")
            IniWrite.setValue("paperType", self.paperType)
            IniWrite.setValue("paperChangeWhenStart", self.paperChangeWhenStart)
            IniWrite.setValue("paperTimeInterval", self.paperTimeInterval)
            IniWrite.setValue("paperAutoChange", self.paperAutoChange)
            IniWrite.setValue("paperNativeDir", self.paperNativeDir)
            IniWrite.setValue("bingDateAsName", self.bingDateAsName)
            IniWrite.endGroup()

            IniWrite.beginGroup("Bing")
            IniWrite.setValue("bingAutoSave", self.bingAutoSave)
            IniWrite.setValue("bingAutoRotation", self.bingAutoRotation)
            IniWrite.endGroup()

            IniWrite.beginGroup("Translation")
            IniWrite.setValue("fanyiEnabled", self.fanyerEnabled)
            IniWrite.setValue("fanyerAutoHide", self.fanyerAutoHide)
            IniWrite.setValue("fanyerAppId", self.fanyerAppId)
            IniWrite.setValue("fanyerPassWord", self.fanyerPassWord)
            IniWrite.endGroup()

            IniWrite.beginGroup("Form")
            IniWrite.setValue("formUiPosX", self.formUiPos.x())
            IniWrite.setValue("formUiPosY", self.formUiPos.y())
            IniWrite.endGroup()

            IniWrite.beginGroup("Dialog")
            IniWrite.setValue("dialogUiThemeR", self.dialogUiTheme.red())
            IniWrite.setValue("dialogUiThemeG", self.dialogUiTheme.green())
            IniWrite.setValue("dialogUiThemeB", self.dialogUiTheme.blue())
            IniWrite.setValue("dialogUiThemeA", self.dialogUiTheme.alpha())
            IniWrite.endGroup()

            IniWrite.beginGroup("Others")
            IniWrite.setValue("controlDesktopIcon", self.controlDesktopIcon)
            IniWrite.endGroup()
        
        self.paperNativeDir = r"C:\Users\yjmthu\OneDrive\Language\Python\Projects\Netbian\image\4K风景"
        self.paperType = self.TYPE_PC_NATIVE

    def initChildren(self):
        self.timer = QTimer()
        self.wallpaper = Wallpaper(self)
        self.wallpaper.start_next()

        self.dialog = Dialog(self)
        self.menu = Menu(self)
        self.form = Form(self)
        self.abd = APPBARDATA()

    def initConnections(self):
        self.timer.timeout.connect(self.wallpaper.start_next)
        self.wallpaper.msgBox.connect(lambda text, title : QMessageBox.information(self.dialog, title, text))
    
    def initBehaviors(self):
        self.timer.start(self.paperTimeInterval * 60000)
        
        cdll.msvcrt.memset(pointer(self.abd), 0, sizeof(self.abd))
        self.abd.cbSize = sizeof(APPBARDATA)
        self.abd.hWnd = self.form.winId()
        self.abd.uCallbackMessage = MSG_APPBAR_MSGID
        windll.shell32.SHAppBarMessage(ABM_NEW, pointer(self.abd))
        self.form.show()
