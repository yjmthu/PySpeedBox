import os, time
from random import randint
from ctypes import pointer, sizeof, windll, wintypes, Structure

FORM_WIDTH = 92
FORM_HEIGHT = 40
DIALOG_WIDTH = 460
DIALOG_HEIGHT = 310
MENU_WIDTH = 92
MENU_HEIGHT = 270
RETCODE_ERROR_EXIT = 1071
RETCODE_UPDATE = 1072
RETCODE_RESTART = 1073

MSG_APPBAR_MSGID = 2731
ABM_NEW = 0
ABN_FULLSCREENAPP =  2
ERROR_ALREADY_EXISTS = 0xB7
FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS = 0x400000
SPI_SETDESKWALLPAPER = 0x0014
SPIF_SENDCHANGE = 0x0002
SPIF_UPDATEINIFILE = 0x0001

def get_data_path() -> str:
    path = os.path.join(os.environ['APPDATA'], 'PySpeedBox')
    if os.path.exists(path):
        return path
    os.mkdir(path)
    return path

def get_ini_path() -> str:
    return os.path.join(get_data_path(), "PySpeedBox.ini")

def isOnline(box, wait):
    flag = wintypes.DWORD()
    for c in range(30 if wait else 0):
        if box.appRun and windll.wininet.InternetGetConnectedState(pointer(flag), 0):
            return True
        elif box.appRun:
            for i in range(6):
                time.sleep(0.5)
                if not box.appRun:
                    return False
        elif not box.appRun:
            return False
    return False

def isOneDriveFile(file_name):
    with open(file_name, 'rb') as f:
        if f.read1(1):
            return True
    return False

class APPBARDATA(Structure):
    _fields_ = [
        ('cbSize', wintypes.DWORD),
        ('hWnd', wintypes.HWND),
        ('uCallbackMessage', wintypes.UINT),
        ('uEdge', wintypes.UINT),
        ('rc', wintypes.RECT),
        ('lParam', wintypes.LPARAM)
    ]
