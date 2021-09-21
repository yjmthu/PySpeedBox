from PySide6.QtWidgets import QGraphicsOpacityEffect, QLabel, QWidget
from PySide6.QtCore import SIGNAL, QPoint, Qt, QPropertyAnimation, QTimer

class GMPOperateTip(QWidget):
    centerPos = QPoint()
    
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent = parent)
        self.tip = QLabel(self)
        self.centerPos = self.parent().rect().center() 

        self.m_pAnimation = QPropertyAnimation(self)
        self.m_pAnimation.setTargetObject(self)

        self.m_pOpacity = QGraphicsOpacityEffect(self)
        self.m_pOpacity.setOpacity(1)
        self.setGraphicsEffect(self.m_pOpacity)
        self.m_pAnimation.setTargetObject(self.m_pOpacity)

        self.m_pAnimation.setPropertyName(b"opacity")
        self.m_pAnimation.setStartValue(1)
        self.m_pAnimation.setEndValue(0)

        self.m_pAnimation.setDuration(150)
        self.connect(self.m_pAnimation, SIGNAL("finished()"), self.do_finish)
        self.setStyleSheet("QWidget{background-color: transparent;}QLabel{background-color: #4cd05c; border-radius: 3px; padding: 6px;}")
        self.setVisible(False)
    
    def showTip(self, Str, time=500):
        self.tip.setText(Str)
        self.tip.adjustSize()
        self.setGeometry(self.centerPos.x()-self.tip.width()/2, self.centerPos.y()-self.tip.height()/2, self.tip.width(), self.tip.height())
        self.setVisible(True)
        QTimer.singleShot(time, self.m_pAnimation.start)
    
    def do_finish(self):
        self.setVisible(False)
        self.m_pOpacity.setOpacity(1)

