from fanyer import Fanyer
import os
from pathlib import Path
from ctypes import wintypes

from psutil import net_io_counters, virtual_memory

from PySide6.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QWidget
from PySide6.QtCore import QFile, QSettings, Qt, QPoint, QRect, QTimer, QPropertyAnimation, QEvent
from PySide6.QtGui import QFont, QMouseEvent, QFontDatabase, QEnterEvent
from PySide6.QtUiTools import QUiLoader

from funcbox import *

def gsh(count):
    if count < 1024:
        return "%.1f " % count
    if count < 1048576:
        return "%.1f K" % (count / 1024)
    count >>= 10
    if count < 1048576:
        return "%.1f M" % (count / 1024)
    count >>= 10
    return "%.1f G" % (count / 1024)

class Form(QWidget):
    _startPos = QPoint()
    _endPos = QPoint()
    _moved = False
    _old_bytes = [0, 0]

    def __init__(self, box):
        super().__init__()
        self.box = box
        self.initUi()
        self.initChildren()
        self.initConnects()
        self.initOthers()

    def start(self):
        net_info = net_io_counters()  # 获取流量统计信息
        recv_bytes = net_info.bytes_recv
        sent_bytes = net_info.bytes_sent
        self.ui.Labup.setText("↑  %sB" % gsh(sent_bytes-self._old_bytes[1]))
        self.ui.Labdown.setText("↓  %sB" % gsh(recv_bytes-self._old_bytes[0]))
        self._old_bytes = [recv_bytes, sent_bytes]
        self.ui.LabMemory.setText(str(int(round(virtual_memory().percent))))

    def initUi(self):
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        ui_file = QFile(os.fspath(Path(__file__).resolve().parent / "form.ui"))
        ui_file.open(QFile.ReadOnly)
        self.ui = QUiLoader().load(ui_file)
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
        self.layout().addChildWidget(self.ui)
        self.move(self.box.formUiPos)

    def initChildren(self):
        self.animation = QPropertyAnimation(self, b"geometry", self)
        self.timer = QTimer(self)
        self.fanyer = Fanyer(self.box, self)

    def initConnects(self):
        self.timer.timeout.connect(self.start)
        self.animation.finished.connect(self.savePos)

    def initOthers(self):
        net_info = net_io_counters()  # 获取流量统计信息
        self._old_bytes[0] = net_info.bytes_recv
        self._old_bytes[1] = net_info.bytes_sent
        self.timer.start(1000)

    def nativeEvent(self, eventType, message: int):
        msg = wintypes.MSG.from_address(message.__int__())
        if msg.message == MSG_APPBAR_MSGID and msg.wParam == ABN_FULLSCREENAPP:
                if (msg.lParam):
                    self.hide()
                else:
                    self.show()
                return True, 0
        return super().nativeEvent(eventType, message)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.RightButton:
            self.box.menu.Show(event.globalPosition())
        elif event.button() == Qt.LeftButton:
            self.setMouseTracking(True)
            self._startPos = event.pos()
        elif event.button() == Qt.MiddleButton:
            QApplication.instance().exit(RETCODE_RESTART)
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            self._endPos = event.pos() - self._startPos
            self.move(self.pos() + self._endPos)
        if self.box.fanyerEnabled and self.fanyer.isVisible():
            self.fanyer.hide()
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.setMouseTracking(False)
            self.savePos()
        return super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        if self.box.fanyerEnabled:
            if not self.fanyer.isVisible():
                self.fanyer.show()
            else:
                self.fanyer.hide()
        return super().mouseDoubleClickEvent(event)

    def enterEvent(self, event: QEnterEvent) -> None:
        pos = self.frameGeometry().topLeft()
        if self._moved:
            if pos.x() + FORM_WIDTH >= self.box.ScreenWidth:
                self.startAnimation(self.box.ScreenWidth - FORM_WIDTH + 2, pos.y())
                self._moved = False
            elif pos.x() <= 0:
                self.startAnimation(0, pos.y())
                self._moved = False
            elif pos.y() <= 0:
                self.startAnimation(pos.x(), 0)
                self._moved = False
        return super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        pos = self.frameGeometry().topLeft()
        if pos.x() + FORM_WIDTH >= self.box.ScreenWidth:
            self.startAnimation(self.box.ScreenWidth - 2, pos.y())
            self._moved = True
        elif pos.x() <= 2:
            self.startAnimation(2 - FORM_WIDTH, pos.y())
            self._moved = True
        elif pos.y() <= 2:
            self.startAnimation(pos.x(), 2 - FORM_HEIGHT)
            self._moved = True
        return super().leaveEvent(event)

    def startAnimation(self, width: int, height:int):
        startpos = self.geometry()
        self.animation.setStartValue(startpos)
        newpos = QRect(width, height, startpos.width(), startpos.height())
        self.animation.setEndValue(newpos)
        self.animation.setDuration(FORM_WIDTH)
        self.animation.start()

    def savePos(self):
        self.box.formUiPos = self.pos()
        IniWrite = QSettings(get_ini_path(), QSettings.IniFormat)
        IniWrite.beginGroup("Form")
        IniWrite.setValue("formUiPosX", self.box.formUiPos.x())
        IniWrite.setValue("formUiPosY", self.box.formUiPos.y())
        IniWrite.endGroup()