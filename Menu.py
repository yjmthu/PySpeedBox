# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import QMenu, QApplication
from PySide6.QtCore import SIGNAL, QPoint, Qt
from PySide6.QtGui import QFont, QFontDatabase, QAction

from funcbox import *

class Menu(QMenu):
    def __init__(self, box):
        super(Menu, self).__init__()
        self.box = box
        self.initActions()
        self.initUi()
        self.initConnects()

    def initUi(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        qss = open("./qss/menu_style.qss", 'rb')
        self.setStyleSheet(str(qss.read(), encoding='utf-8'))
        qss.close()

        font = QFont()
        font.setFamily(QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont("./fonts/smallkaiti.ttf"))[0])
        font.setPointSize(10)
        self.setFont(font)

        self.setMaximumSize(MENU_WIDTH, MENU_HEIGHT)
        self.setMinimumSize(MENU_WIDTH, MENU_HEIGHT)

    def initActions(self):
        #wallpaper = MenuWallpaper

        self.settingDialogAct = QAction()
        self.settingDialogAct.setText("软件设置")
        self.addAction(self.settingDialogAct)

        self.translateAct = QAction()
        self.translateAct.setText("划词翻译")
        self.translateAct.setCheckable(True)
        self.addAction(self.translateAct)

        self.prevPaperAct = QAction()
        self.prevPaperAct.setText("上一张图")
        self.addAction(self.prevPaperAct)

        self.nextPaperAct = QAction()
        self.nextPaperAct.setText("下一张图")
        self.addAction(self.nextPaperAct)

        self.removePicAct = QAction()
        self.removePicAct.setText("不看此图")
        self.addAction(self.removePicAct)

        self.openFolderAct = QAction()
        self.openFolderAct.setText("打开目录")
        self.addAction(self.openFolderAct)

        self.shutdownAct = QAction()
        self.shutdownAct.setText("快速关机")
        self.addAction(self.shutdownAct)

        self.quitAct = QAction()
        self.quitAct.setText("本次退出")
        self.addAction(self.quitAct)

        self.noSleepAct = QAction()
        self.noSleepAct.setText("防止息屏")
        self.noSleepAct.setCheckable(True)
        self.addAction(self.noSleepAct)

    def initConnects(self):
        self.connect(self.quitAct, SIGNAL('triggered()'), QApplication.quit)
        self.connect(self.settingDialogAct, SIGNAL('triggered()'), self.box.dialog.show)
        self.connect(self.nextPaperAct, SIGNAL('triggered()'), self.box.wallpaper.start_next)
        self.connect(self.prevPaperAct, SIGNAL('triggered()'), self.box.wallpaper.start_prev)
        #self.quitAct.triggered.connect(lambda: QApplication.instance().quit())

    def Show(self, pos:QPoint):
        px, py = 0, 0
        if (pos.x() + MENU_WIDTH < self.box.ScreenWidth):
            px = pos.x()
        else:
            px = self.box.ScreenWidth - MENU_WIDTH
        if (pos.y() + MENU_HEIGHT < self.box.ScreenHeight):
            py = pos.y()
        else:
            py = pos.y() - MENU_HEIGHT
        self.move(px, py)
        self.show()
