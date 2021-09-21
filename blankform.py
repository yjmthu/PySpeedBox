from PySide6.QtWidgets import QPushButton, QWidget
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QEnterEvent

class BlankFrom(QWidget):
    def __init__(self, parent, left, right) -> None:
        super().__init__(parent)
        self.setMaximumSize(100, 40)
        self.setMinimumSize(100, 40)
        self.closeButton = QPushButton(self)
        self.minButton = QPushButton(self)
        self.minButton.setGeometry(self.width()-75,12,14,14)
        self.closeButton.setGeometry(self.width()-40,12,14,14)
        self.minButton.setToolTip("最小化")
        self.closeButton.setToolTip("关闭")
        self.minButton.setCursor(Qt.PointingHandCursor)
        self.closeButton.setCursor(Qt.PointingHandCursor)
        self.minButton.setStyleSheet("QPushButton{background-color:#85c43b; border-radius:7px;}")
        self.closeButton.setStyleSheet("QPushButton{background-color:#ea6e4d; border-radius:7px;}")
        self.closeButton.clicked.connect(right)
        self.minButton.clicked.connect(left)
        self.move(self.parent().width()-self.width(), 0)

    def enterEvent(self, event: QEnterEvent) -> None:
        self.closeButton.setStyleSheet("QPushButton{border-image: url(./icons/close.png);border-radius:7px;}")
        self.minButton.setStyleSheet("QPushButton{border-image: url(./icons/minimize.png);border-radius:7px;}")
        return super().enterEvent(event)

    def leaveEvent(self, event : QEvent) -> None:
        self.minButton.setStyleSheet("QPushButton{background-color:#85c43b; border-radius:7px;}")
        self.closeButton.setStyleSheet("QPushButton{background-color:#ea6e4d; border-radius:7px;}")
        return super().leaveEvent(event)