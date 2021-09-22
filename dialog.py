import os
from pathlib import Path

from PySide6.QtWidgets import QButtonGroup, QHBoxLayout, QLayout
from PySide6.QtCore import QFile, QSize, Qt
from PySide6.QtUiTools import QUiLoader

from funcbox import *
from speedwidget import SpeedWidget


class Dialog(SpeedWidget):

    def __init__(self, box)->None:
        super().__init__()
        self.box = box
        self.initUi()
        self.initChildren()
        self.initOthers()
    
    def initUi(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint)

        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(5,5,5,5)
        qss = open("./qss/dialog_style.qss", 'rb')
        self.setStyleSheet(str(qss.read(), encoding='utf-8'))
        qss.close()

        ui_file = QFile(os.fspath(Path(__file__).resolve().parent / "dialog.ui"))
        ui_file.open(QFile.ReadOnly)
        self.ui = QUiLoader().load(ui_file, None)
        ui_file.close()
        self.layout().addChildWidget(self.ui)

        self.setMinimumSize(QSize(DIALOG_WIDTH, DIALOG_HEIGHT))
        self.setMaximumSize(QSize(DIALOG_WIDTH, DIALOG_HEIGHT))
        #self.ui.lineAppData.setText(self.box.get_dat_path())
        self.move((self.box.ScreenWidth - self.width()) / 2, (self.box.ScreenHeight - self.height()) / 2)
        self.ui.setStyleSheet("QFrame{background-color:rgba(0, 0, 0, 100);}QLabel{border-radius: 3px;background-color: transparent;}Line{background-color:black};")
        self.initSpeedBox(self.ui, self.showMinimized, self.close)

    def setTheme(self):
        self.ui.frame.setStyleSheet("QFrame{background-color:rgba(%1);} QLabel{border-radius: 3px;background-color: transparent;}Line{background-color:black};")
        self.jobTip.showTip("设置成功！")
    
    def initChildren(self):
        self.buttonGroup = QButtonGroup()
    
    def initOthers(self):
        pass
        # self.buttonGroup.addButton(self.ui.rBtnNew, self.box.PAPER_TYPE.Latest)
        # self.buttonGroup.addButton(self.ui.rBtnHot, self.box.PAPER_TYPE.Hot)
        # self.buttonGroup.addButton(self.ui.rBtnNature, self.box.PAPER_TYPE.Nature)
        # self.buttonGroup.addButton(self.ui.rBtnAnime, self.box.PAPER_TYPE.Anime)
        # self.buttonGroup.addButton(self.ui.rBtnSimple, self.box.PAPER_TYPE.Simple)
        # self.buttonGroup.addButton(self.ui.rBtnRandom, self.box.PAPER_TYPE.Random)
        # self.buttonGroup.addButton(self.ui.rBtnBing, self.box.PAPER_TYPE.Bing)
        # self.buttonGroup.addButton(self.ui.rBtnNative, self.box.PAPER_TYPE.Native)
        # self.buttonGroup.addButton(self.ui.rBtnAdvance, self.box.PAPER_TYPE.Advance)
        # self.buttonGroup.setExclusive(True)