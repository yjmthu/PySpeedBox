import os
from pathlib import Path

from PySide6.QtWidgets import QButtonGroup
from PySide6.QtCore import QFile, QSize, Qt
from PySide6.QtUiTools import QUiLoader

from speedwidget import SpeedWidget

DIALOG_WIDTH = 460
DIALOG_HEIGHT = 310

class Dialog(SpeedWidget):

    def __init__(self, VarBox)->None:
        super().__init__()
        self.VarBox = VarBox
        self.initUi()
        self.initChildren()
        self.initOthers()
    
    def initUi(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint)

        ui_file = QFile(os.fspath(Path(__file__).resolve().parent / "dialog.ui"))
        ui_file.open(QFile.ReadOnly)
        self.ui = QUiLoader().load(ui_file, self)
        ui_file.close()

        qss = open("./qss/dialog_style.qss", 'rb')
        self.setStyleSheet(str(qss.read(), encoding='utf-8'))
        qss.close()

        self.setMinimumSize(QSize(DIALOG_WIDTH, DIALOG_HEIGHT))
        self.setMaximumSize(QSize(DIALOG_WIDTH, DIALOG_HEIGHT))
        #self.ui.lineAppData.setText(self.VarBox.get_dat_path())
        self.move((self.VarBox.ScreenWidth - self.width()) / 2, (self.VarBox.ScreenHeight - self.height()) / 2)
        self.ui.frame.setStyleSheet("QFrame{background-color:rgba(0, 0, 0, 0);}QLabel{border-radius: 3px;background-color: transparent;}Line{background-color:black};")
        self.initSpeedBox(self.ui.frame, self.showMinimized, self.close)

    def setTheme(self):
        self.ui.frame.setStyleSheet("QFrame{background-color:rgba(%1);} QLabel{border-radius: 3px;background-color: transparent;}Line{background-color:black};")
        self.jobTip.showTip("设置成功！")
    
    def initChildren(self):
        self.buttonGroup = QButtonGroup()
    
    def initOthers(self):
        self.buttonGroup.addButton(self.ui.rBtnNew, self.VarBox.PAPER_TYPE.Latest)
        self.buttonGroup.addButton(self.ui.rBtnHot, self.VarBox.PAPER_TYPE.Hot)
        self.buttonGroup.addButton(self.ui.rBtnNature, self.VarBox.PAPER_TYPE.Nature)
        self.buttonGroup.addButton(self.ui.rBtnAnime, self.VarBox.PAPER_TYPE.Anime)
        self.buttonGroup.addButton(self.ui.rBtnSimple, self.VarBox.PAPER_TYPE.Simple)
        self.buttonGroup.addButton(self.ui.rBtnRandom, self.VarBox.PAPER_TYPE.Random)
        self.buttonGroup.addButton(self.ui.rBtnBing, self.VarBox.PAPER_TYPE.Bing)
        self.buttonGroup.addButton(self.ui.rBtnNative, self.VarBox.PAPER_TYPE.Native)
        self.buttonGroup.addButton(self.ui.rBtnAdvance, self.VarBox.PAPER_TYPE.Advance)
        self.buttonGroup.setExclusive(True)