# This Python file uses the following encoding: utf-8
import os, sys
from ctypes import wintypes, windll

from funcbox import *
from varbox import VarBox

from PySide6.QtWidgets import QApplication


if __name__ == "__main__":
    HMutex: wintypes.HANDLE = windll.kernel32.CreateMutexW(None, False, "__PySpeedBox__")
    if windll.kernel32.GetLastError() == ERROR_ALREADY_EXISTS:
        exit(0)
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)
    box = VarBox()
    exit_number = app.exec()
    if exit_number == RETCODE_RESTART:
        sys.argv.insert(0, __file__)
        windll.kernel32.CloseHandle(HMutex)
        os.execv(sys.executable, sys.argv)
    elif exit_number == RETCODE_ERROR_EXIT:
        windll.kernel32.CloseHandle(HMutex)
        sys.exit(1)
    elif exit_number == RETCODE_UPDATE:
        sys.argv.insert(0, __file__)
        sys.argv.append("update")
        windll.kernel32.CloseHandle(HMutex)
        os.execv(sys.executable, sys.argv)
    else:
        windll.kernel32.CloseHandle(HMutex)
        sys.exit(exit_number)
