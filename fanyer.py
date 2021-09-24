
from funcbox import *
import os
from pathlib import Path
from ctypes import pointer, wintypes, windll

from PySide6.QtCore import QEvent, QFile, QObject, QSize, Qt
from PySide6.QtGui import QImage, QKeyEvent, QPixmap, QShowEvent, QTextCursor
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QHBoxLayout


from speedwidget import SpeedWidget


class Fanyer(SpeedWidget):
    def __init__(self, box, parent=None) -> None:
        super().__init__(parent=parent)
        self.box = box
        self.initUi()
        self.initSpeedBox(self.ui, self.showMinimized, self.close, 12)
    
    def initUi(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        qss = open("./qss/fanyer_style.qss", 'rb')
        self.setStyleSheet(str(qss.read(), encoding='utf-8'))
        qss.close()

        ui_file = QFile(os.fspath(Path(__file__).resolve().parent / "fanyer.ui"))
        ui_file.open(QFile.ReadOnly)
        self.ui = QUiLoader().load(ui_file)
        ui_file.close()

        self.setMinimumSize(QSize(FANYER_WIDTH, FANYER_HEIGHT))
        self.setMaximumSize(QSize(FANYER_WIDTH, FANYER_HEIGHT))
        self.layout().addChildWidget(self.ui)
        # self.ui.Icon.setPixmap(QPixmap.fromImage(QImage("./icons/ya.ico").scaled(20, 20, Qt.KeepAspectRatio)))
    
    def showEvent(self, arg__1: QShowEvent) -> None:

        rt = wintypes.RECT()
        windll.User32.GetWindowRect(self.winId(), pointer(rt))
        w = rt.right - rt.left
        h = rt.bottom - rt.top
        sw = windll.User32.GetSystemMetrics(SM_CXSCREEN)
        windll.User32.GetWindowRect(self.box.form.winId(), pointer(rt))
        x = sw - w if rt.left + rt.right + w > sw * 2 else 0 if rt.right + rt.left < w else (rt.left + rt.right - w) / 2
        y = rt.top - h if rt.top > h else rt.bottom

        cursor = self.ui.TextFrom.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.ui.TextFrom.setTextCursor(cursor)
        self.ui.TextFrom.setFocus()

        windll.User32.SetWindowPos(self.winId(), self.box.form.winId(), int(x), int(y), 0, 0, SWP_NOSIZE)

        arg__1.accept()
    
    def mouseDoubleClickEvent(self, event) -> None:
        rt = wintypes.RECT()
        windll.User32.GetWindowRect(self.winId(), pointer(rt))
        print(rt.left, rt.top)
        return super().mouseDoubleClickEvent(event)

    def eventFilter(self, arg__1: QObject, arg__2: QEvent) -> bool:
        if arg__1 == self.ui.TextFrom:
            if arg__2.type() == QEvent.KeyPress:
                event: QKeyEvent = arg__2
                if event.key() == Qt.Key_Return:
                    return True
                elif event.key() == Qt.Key_Delete:
                    self.ui.TextFrom.clear()
                    self.ui.TextTo.clear()
                    event.accept()
                    return True
        return super().eventFilter(arg__1, arg__2)
