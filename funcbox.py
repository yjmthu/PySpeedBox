import os, time, sys, subprocess
from ctypes import POINTER, pointer, windll, wintypes, Structure, c_char
from enum import Enum

FORM_WIDTH = 92
FORM_HEIGHT = 40
DIALOG_WIDTH = 460
DIALOG_HEIGHT = 310
MENU_WIDTH = 92
MENU_HEIGHT = 270
FANYER_WIDTH = 240
FANYER_HEIGHT = 300

RETCODE_ERROR_EXIT = 1071
RETCODE_UPDATE = 1072
RETCODE_RESTART = 1073
SM_CXSCREEN = 0
SM_CYSCREEN = 1
MOUSEEVENTF_MOVE = 0x0001
GENERIC_READ = 0x80000000
FILE_SHARE_READ = 0x00000001
OPEN_EXISTING = 3
FILE_ATTRIBUTE_NORMAL = 0x00000080
SW_SHOW = 5
SW_HIDE = 0
SW_SHOWNORMAL = 1
SW_NORMAL = 1
SWP_NOSIZE = 0x0001
HWND_TOPMOST = wintypes.HWND(-1)

MSG_APPBAR_MSGID = 2731
ABM_NEW = 0
ABN_FULLSCREENAPP =  2
ERROR_ALREADY_EXISTS = 0xB7
FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS = 0x400000
SPI_SETDESKWALLPAPER = 0x0014
SPIF_SENDCHANGE = 0x0002
SPIF_UPDATEINIFILE = 0x0001
INVALID_HANDLE_VALUE = -1

def get_dat_path() -> str:
    path = os.path.join(os.environ['APPDATA'], 'PySpeedBox')
    if os.path.exists(path):
        return path
    os.mkdir(path)
    return path

def get_ini_path() -> str:
    return os.path.join(get_dat_path(), "PySpeedBox.ini")

def get_dir_path() -> str:
    return os.path.dirname(os.path.abspath(sys.argv[0]))

def get_scr_path() -> str:
    return os.path.abspath(sys.argv[0])

def subRunCmd(cmd):
    subprocess.run(cmd, shell=True, stdin=-1, stdout=-1, stderr=-1)

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

def isOneDriveFile(box, file_name):
    hFileRead: wintypes.HANDLE = windll.Kernel32.CreateFileW(file_name, GENERIC_READ, FILE_SHARE_READ, None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, None)
    for i in range(30):
        if hFileRead == INVALID_HANDLE_VALUE:
            return False
        fileDataBuffer = c_char(0)
        dwReadedSize = wintypes.DWORD(0)
        if windll.Kernel32.ReadFile(hFileRead, pointer(fileDataBuffer), 1, pointer(dwReadedSize), None) and dwReadedSize:
            windll.Kernel32.CloseHandle(hFileRead)
            return True
        if not box.appRun:
            break
        for j in range(6):
            if box.appRun:
                time.sleep(0.5)
            else:
                break
        else:
            continue
        break
    windll.Kernel32.CloseHandle(hFileRead)
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

class WINDOWCOMPOSITIONATTRIB(Enum):
    WCA_UNDEFINED = 0,
    WCA_NCRENDERING_ENABLED = 1,
    WCA_NCRENDERING_POLICY = 2,
    WCA_TRANSITIONS_FORCEDISABLED = 3,
    WCA_ALLOW_NCPAINT = 4,
    WCA_CAPTION_BUTTON_BOUNDS = 5,
    WCA_NONCLIENT_RTL_LAYOUT = 6,
    WCA_FORCE_ICONIC_REPRESENTATION = 7,
    WCA_EXTENDED_FRAME_BOUNDS = 8,
    WCA_HAS_ICONIC_BITMAP = 9,
    WCA_THEME_ATTRIBUTES = 10,
    WCA_NCRENDERING_EXILED = 11,
    WCA_NCADORNMENTINFO = 12,
    WCA_EXCLUDED_FROM_LIVEPREVIEW = 13,
    WCA_VIDEO_OVERLAY_ACTIVE = 14,
    WCA_FORCE_ACTIVEWINDOW_APPEARANCE = 15,
    WCA_DISALLOW_PEEK = 16,
    WCA_CLOAK = 17,
    WCA_CLOAKED = 18,
    WCA_ACCENT_POLICY = 19,
    WCA_FREEZE_REPRESENTATION = 20,
    WCA_EVER_UNCLOAKED = 21,
    WCA_VISUAL_OWNER = 22,
    WCA_LAST = 23


class ACCENT_STATE(Enum):
    """ 客户区状态枚举类 """
    ACCENT_DISABLED = 0,                   # 默认效果
    ACCENT_ENABLE_GRADIENT = 1,            # 梯度
    ACCENT_ENABLE_TRANSPARENTGRADIENT = 2, # 透明效果
    ACCENT_ENABLE_BLURBEHIND = 3,          # Aero效果
    ACCENT_ENABLE_ACRYLICBLURBEHIND = 4,   # 亚克力效果
    ACCENT_INVALID_STATE = 5


class ACCENT_POLICY(Structure):
    """ 设置客户区的具体属性 """
    _fields_ = [
        ('AccentState',   wintypes.DWORD),
        ('AccentFlags',   wintypes.DWORD),
        ('GradientColor', wintypes.DWORD),
        ('AnimationId',   wintypes.DWORD),
    ]


class WINDOWCOMPOSITIONATTRIBDATA(Structure):
    _fields_ = [
        ('Attribute',  wintypes.DWORD),
        ('Data',       POINTER(ACCENT_POLICY)),
        ('SizeOfData', wintypes.ULONG),
    ]

SetWindowCompositionAttribute = windll.user32.SetWindowCompositionAttribute
SetWindowCompositionAttribute.restype = wintypes.BOOL
SetWindowCompositionAttribute.argtypes = wintypes.HWND, POINTER(WINDOWCOMPOSITIONATTRIBDATA)
