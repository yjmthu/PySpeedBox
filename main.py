# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from Menu import Menu
from funcbox import VARBOX

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QFile, Qt, QPoint
from PySide6.QtGui import QFont, QMouseEvent, QFontDatabase, QGuiApplication
from PySide6.QtUiTools import QUiLoader

FORM_WIDTH = 92
FORM_HEIGHT = 40

class Form(QWidget):
    _startPos = QPoint()
    _endPos = QPoint()
    def __init__(self, VarBox: VARBOX):
        super(Form, self).__init__()
        self.VarBox = VarBox
        self.load_ui()
        self.menu = Menu(VarBox)

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        font_use = QFontDatabase.addApplicationFont("./fonts/qitijian.otf")
        fontFamilies = QFontDatabase.applicationFontFamilies(font_use)
        font = QFont()
        font.setFamily(fontFamilies[0])
        font.setPointSize(18)
        font.setBold(True)
        self.ui.LabMemory.setFont(font)
        font_use = QFontDatabase.addApplicationFont("./fonts/netspeed.ttf")
        fontFamilies = QFontDatabase.applicationFontFamilies(font_use)
        font.setFamily(fontFamilies[0])
        font.setPointSize(8)
        font.setBold(True)
        self.ui.Labdown.setFont(font)
        self.ui.Labup.setFont(font)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumSize(FORM_WIDTH, FORM_HEIGHT)
        self.setMaximumSize(FORM_WIDTH, FORM_HEIGHT)
        self.ui.LabMemory.setMaximumWidth(30)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.RightButton:
            self.menu.Show(event.globalPosition())
        elif event.buttons() == Qt.LeftButton:
            self.setMouseTracking(True)
            self._startPos = event.pos()
        return super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            self._endPos = event.pos() - self._startPos
            self.move(self.pos() + self._endPos)
        return super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            self.setMouseTracking(False)
            self._endPos = event.pos() - self._startPos
        return super().mouseReleaseEvent(event)
    
    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None: 
        QApplication.instance().quit()
        return super().mouseDoubleClickEvent(event)


if __name__ == "__main__":
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)
    screen = QGuiApplication.primaryScreen()
    geo = screen.geometry()
    VarBox = VARBOX(geo.width(), geo.height())
    widget = Form(VarBox)
    widget.show()
    sys.exit(app.exec())
