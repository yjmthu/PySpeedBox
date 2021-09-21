# This Python file uses the following encoding: utf-8
import os, sys
from funcbox import VARBOX

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QGuiApplication

FORM_WIDTH = 92
FORM_HEIGHT = 40
RETCODE_ERROR_EXIT = 1071
RETCODE_UPDATE = 1072
RETCODE_RESTART = 1073


if __name__ == "__main__":
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)
    screen = QGuiApplication.primaryScreen()
    geo = screen.geometry()
    VarBox = VARBOX(geo.width(), geo.height())
    VarBox.creatForm()
    exit_number = app.exec()
    if exit_number == RETCODE_RESTART:
        sys.argv.insert(0, __file__)
        os.execv(sys.executable, sys.argv)
    else:
        sys.exit(exit_number)
