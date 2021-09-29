import os
from pathlib import Path

from PySide6.QtWidgets import QHBoxLayout, QWidget
from PySide6.QtCore import QSize, Qt, QFile
from PySide6.QtUiTools import QUiLoader

from speedwidget import SpeedWidget


class BingSetting(SpeedWidget):
    def __init__(self, parent: QWidget, box) -> None:
        super().__init__(parent)
        self.box = box
        self.initUi()
        self.initSpeedBox(self.ui, self.showMinimized, self.close)
    
    def initUi(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(5, 0, 5, 5)
        qss = open("./qss/bing_style.qss", 'rb')
        self.setStyleSheet(str(qss.read(), encoding='utf-8'))
        qss.close()

        ui_file = QFile(os.fspath(Path(__file__).resolve().parent / "bingsetting.ui"))
        ui_file.open(QFile.ReadOnly)
        self.ui = QUiLoader().load(ui_file)
        ui_file.close()

        self.setMinimumSize(QSize(333, 222))
        self.setMaximumSize(QSize(333, 222))
        self.layout().addChildWidget(self.ui)
        # self.ui.Icon.setPixmap(QPixmap.fromImage(QImage("./icons/ya.ico").scaled(20, 20, Qt.KeepAspectRatio)))
    
    def Show(self):
        parent: QWidget = self.parent()
        self.move(parent.frameGeometry().x()+(parent.width()-self.width())/2, parent.frameGeometry().y()+(parent.height()-self.height())/2);
        self.exec()