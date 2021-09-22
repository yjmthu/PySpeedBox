import os
from ctypes import wintypes, Structure

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

def get_data_path() -> str:
    path = os.path.join(os.environ['APPDATA'], 'PySpeedBox')
    if os.path.exists(path):
        return path
    os.mkdir(path)
    return path

def get_ini_path() -> str:
    return os.path.join(get_data_path(), "PySpeedBox.ini")

class APPBARDATA(Structure):
    _fields_ = [
        ('cbSize', wintypes.DWORD),
        ('hWnd', wintypes.HWND),
        ('uCallbackMessage', wintypes.UINT),
        ('uEdge', wintypes.UINT),
        ('rc', wintypes.RECT),
        ('lParam', wintypes.LPARAM)
    ]
