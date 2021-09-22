from ctypes import wintypes, pointer, windll, cdll, sizeof
import os

from PySide6.QtGui import QColor, QGuiApplication
from PySide6.QtCore import QDir, QPoint, QStandardPaths, QSettings

from funcbox import *
from form import Form
from dialog import Dialog
from menu import Menu

class VarBox:

    TYPE_MS_BING, TYPE_PY_SCRIPT, TYPE_PC_NATIVE = range(3)

    def __init__(self) -> None:
        screen = QGuiApplication.primaryScreen()
        geo = screen.geometry()
        self.ScreenWidth = geo.width()
        self.ScreenHeight = geo.height()
        self.AppId = str()
        self.PassWord = str()
        self.initSpeedBox()
    
    def creatWidgets(self):
        self.form = Form(self)
        self.abd = APPBARDATA()
        cdll.msvcrt.memset(pointer(self.abd), 0, sizeof(self.abd))
        self.abd.cbSize = sizeof(APPBARDATA)
        self.abd.hWnd = self.form.winId()
        self.abd.uCallbackMessage = MSG_APPBAR_MSGID
        windll.shell32.SHAppBarMessage(ABM_NEW, pointer(self.abd))
        self.form.show()

        self.dialog = Dialog(self)
        self.menu = Menu(self)
    
    def initSpeedBox(self):
        main_folder = get_data_path()
        ini_file = os.path.join(main_folder, "PySpeedBox.ini")
        if os.path.exists(ini_file):
            IniRead = QSettings(ini_file, QSettings.IniFormat)
            self.appfirstUse = False
            self.appRun = True

            IniRead.beginGroup("Wallpaper")
            self.paperHistory = list()
            self.paperCur = 0
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
            IniRead.endGroup()

            IniRead.beginGroup("Others")
            self.controlDesktopIcon = IniRead.value("controlDesktopIcon", False, bool)
            IniRead.endGroup()
        else:
            self.appfirstUse = True
            self.appRun = True

            self.paperHistory = list()
            self.paperCur = 0
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

            self.controlDesktopIcon = False

            IniWrite = QSettings(ini_file, QSettings.IniFormat)
            IniWrite.beginGroup("Wallpaper")
            IniWrite.setValue("paperType", self.paperType)
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

