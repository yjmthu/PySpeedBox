from PySide6.QtWidgets import QDialog, QFrame, QGraphicsDropShadowEffect
from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QMouseEvent

from gmpoperatetip import GMPOperateTip
from blankform import BlankFrom

class  SpeedWidget(QDialog):
    _startPos = QPoint()
    _endPos = QPoint()

    def __init__(self) -> None:
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
    
    def initSpeedBox(self, frame: QFrame, left, right):
        self.effect = QGraphicsDropShadowEffect(self)
        self.effect.setOffset(0, 0)
        self.effect.setBlurRadius(15)
        self.effect.setColor(Qt.black)
        frame.setGraphicsEffect(self.effect)
        self.jobTip = GMPOperateTip(self)
        self.blank = BlankFrom(self)
        self.blank.closeButton.clicked.connect(right)
        self.blank.minButton.clicked.connect(left)
        self.blank.move(self.width()-100, 0)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            self.setMouseTracking(True)
            self._startPos = event.pos()
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            self.setMouseTracking(False)
        return super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self._endPos = event.pos() - self._startPos
        self.move(self.pos() + self._endPos)
        return super().mouseMoveEvent(event)
