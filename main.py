# This Python file uses the following encoding: utf-8
import os, sys
from varbox import VarBox
from form import RETCODE_ERROR_EXIT, RETCODE_UPDATE, RETCODE_RESTART

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QGuiApplication


if __name__ == "__main__":
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)
    screen = QGuiApplication.primaryScreen()
    geo = screen.geometry()
    box = VarBox(geo.width(), geo.height())
    box.creatForm()
    exit_number = app.exec()
    if exit_number == RETCODE_RESTART:
        sys.argv.insert(0, __file__)
        sys.argv.append("restart")
        os.execv(sys.executable, sys.argv)
    elif exit_number == RETCODE_ERROR_EXIT:
        sys.exit(1)
    elif exit_number == RETCODE_UPDATE:
        sys.argv.insert(0, __file__)
        sys.argv.append("update")
        os.execv(sys.executable, sys.argv)
    else:
        sys.exit(exit_number)
