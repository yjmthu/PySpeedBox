from PySide6.QtWidgets import QPushButton, QWidget
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QEnterEvent

class BlankFrom(QWidget):
    def __init__(self, parent, left, right, top=7) -> None:
        super().__init__(parent)
        self.setMaximumSize(100, 40)
        self.setMinimumSize(100, 40)
        self.__closeButton = QPushButton(self)
        self.__minButton = QPushButton(self)
        self.__minButton.setGeometry(self.width()-75,top,14,14)
        self.__closeButton.setGeometry(self.width()-40,top,14,14)
        self.__minButton.setToolTip("最小化")
        self.__closeButton.setToolTip("关闭")
        self.__minButton.setCursor(Qt.PointingHandCursor)
        self.__closeButton.setCursor(Qt.PointingHandCursor)
        self.__minButton.setStyleSheet("QPushButton{background-color:#85c43b; border-radius:7px;}")
        self.__closeButton.setStyleSheet("QPushButton{background-color:#ea6e4d; border-radius:7px;}")
        self.__closeButton.clicked.connect(right)
        self.__minButton.clicked.connect(left)
        self.move(self.parent().width()-self.width(), 0)

    def enterEvent(self, event: QEnterEvent) -> None:
        self.__closeButton.setStyleSheet("QPushButton{border-image: url(./icons/close.png);border-radius:7px;}")
        self.__minButton.setStyleSheet("QPushButton{border-image: url(./icons/minimize.png);border-radius:7px;}")
        return super().enterEvent(event)

    def leaveEvent(self, event : QEvent) -> None:
        self.__minButton.setStyleSheet("QPushButton{background-color:#85c43b; border-radius:7px;}")
        self.__closeButton.setStyleSheet("QPushButton{background-color:#ea6e4d; border-radius:7px;}")
        return super().leaveEvent(event)