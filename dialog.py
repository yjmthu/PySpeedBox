import os
from pathlib import Path

from PySide6.QtWidgets import QButtonGroup
from PySide6.QtCore import QFile, Qt
from PySide6.QtUiTools import QUiLoader

from speedwidget import SpeedWidget


class Dialog(SpeedWidget):

    def __init__(self, VarBox)->None:
        super().__init__()
        self.VarBox = VarBox
        self.buttonGroup = QButtonGroup()
        self.initUi()
    
    def initUi(self):
        ui_file = QFile(os.fspath(Path(__file__).resolve().parent / "dialog.ui"))
        ui_file.open(QFile.ReadOnly)
        self.ui = QUiLoader().load(ui_file, self)
        ui_file.close()
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint)

        qss = open("./qss/dialog_style.qss", 'rb')
        self.setStyleSheet(str(qss.read(), encoding='utf-8'))
        qss.close()

        self.initSpeedBox(self.ui.frame, self.showMinimized, self.close)

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
        #self.ui.lineAppData.setText(self.VarBox.get_dat_path())
        self.move((self.VarBox.ScreenWidth - self.width()) / 2, (self.VarBox.ScreenHeight - self.height()) / 2)
        #setTheme()
