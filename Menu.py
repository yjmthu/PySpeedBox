# This Python file uses the following encoding: utf-8
from ctypes import byref

from PySide6.QtWidgets import QMenu, QApplication
from PySide6.QtCore import SIGNAL, QPoint, QTimer, Qt
from PySide6.QtGui import QFont, QFontDatabase, QAction

from funcbox import *

class Menu(QMenu):

    def __init__(self, box):
        super(Menu, self).__init__()
        self.box = box
        self.initChildren()
        self.initActions()
        self.initUi()
        self.initConnects()
    
    def initChildren(self):
        self.timer = QTimer()
    
    def do_stop_sleep(self, checked):
        if checked:
            self.timer.start(40000)
        else:
            self.timer.stop()

    def get_mouse_moved(self):
        W_MAX = windll.user32.GetSystemMetrics(SM_CXSCREEN)
        pt = wintypes.POINT()
        windll.user32.GetCursorPos(wintypes.byref(pt))
        X = -1 if pt.x == W_MAX else 1
        windll.user32.mouse_event(MOUSEEVENTF_MOVE, X, 0, 0, None)
        time.sleep(0.001)
        windll.user32.mouse_event(MOUSEEVENTF_MOVE, -X, 0, 0, None)

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

        self.remoPicAct = QAction()
        self.remoPicAct.setText("不看此图")
        self.addAction(self.remoPicAct)

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
        self.timer.timeout.connect(self.get_mouse_moved)
        self.connect(self.quitAct, SIGNAL('triggered()'), QApplication.quit)
        self.connect(self.settingDialogAct, SIGNAL('triggered()'), self.box.dialog.show)
        self.connect(self.nextPaperAct, SIGNAL('triggered()'), self.box.wallpaper.start_next)
        self.connect(self.prevPaperAct, SIGNAL('triggered()'), self.box.wallpaper.start_prev)
        self.connect(self.remoPicAct, SIGNAL('triggered()'), self.box.wallpaper.start_remo)
        self.connect(self.openFolderAct, SIGNAL('triggered()'), lambda: subRunCmd('start explorer {}'.format(get_dir_path())))
        self.connect(self.noSleepAct, SIGNAL('triggered(bool)'), self.do_stop_sleep)
        self.connect(self.shutdownAct,  SIGNAL('triggered()'), lambda: subRunCmd('shutdown -s -t 0 -f'))
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
