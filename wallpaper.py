from threading import Thread
from random import randint

from PySide6.QtCore import QObject, Signal

from funcbox import *

class Wallpaper(QObject):

    finished = Signal()
    isBusy = Signal()
    msgBox = Signal(str, str)
    errorSettings = Signal()
    def __init__(self, box) -> None:
        super().__init__()
        self.box = box
        self.__isRuning = False
        self.finished.connect(self.clean)

        self.runThread = lambda f: Thread(target=f, daemon=True).start()
    
    def start_next(self) -> None:
        print("线程next启动")
        if not self.__isRuning:
            self.__isRuning = True
            self.runThread(lambda: self.set_from_Native(True))
        else:
            self.isBusy.emit()
    
    def start_prev(self) -> None:
        print("线程prev启动")
        if not self.__isRuning:
            self.__isRuning = True
            if self.box.paperCur > 0:
                self.box.paperCur -= 1
                self.setWallpaper(self.box.paperHistory[self.box.paperCur])
            else:
                self.msgBox.emit("找不到更早的壁纸历史记录！", "提示")
            self.finished.emit()
        else:
            self.isBusy.emit()
    
    def start_remo(self) -> None:
        print("线程remv启动")
        if not self.__isRuning:
            self.__isRuning = True
            if (os.path.exists(self.box.paperHistory[self.box.paperCur])):
                os.remove(self.box.paperHistory[self.box.paperCur])
            del self.box.paperHistory[self.box.paperCur]
            if self.box.paperCur < len(self.box.paperHistory):
                self.runThread(lambda: self.setWallpaper(self.box.paperHistory[self.box.paperCur], True))
            else:
                self.runThread(lambda: self.set_from_Native(True))
        else:
            self.isBusy.emit()
    
    def clean(self):
        print("线程结束")
        self.__isRuning = False
    
    def setWallpaper(self, paper_path: str, emit=False):
        windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, paper_path, SPIF_SENDCHANGE | SPIF_UPDATEINIFILE)
        if emit:
            self.finished.emit()
    
    def checkList(self) -> bool:
        if self.box.paperCur + 1 < len(self.box.paperHistory):
            self.box.paperCur += 1
            self.setWallpaper(self.box.paperHistory[self.box.paperCur])
            return True
        return False
    
    def set_from_Native(self, net):
        if self.box.paperCur + 1 < len(self.box.paperHistory):
            self.box.paperCur += 1
            self.setWallpaper(self.box.paperHistory[self.box.paperCur])
        elif os.path.exists(self.box.paperNativeDir):
            filters = [".png", ".jpg", ".jpeg", ".bmp", ".wbep"]
            dir = list(filter(lambda filename: os.path.splitext(filename)[1] in filters, os.listdir(self.box.paperNativeDir)))
            dir_count = len(dir)
            if not dir_count:
                self.errorSettings.emit()
                self.finished.emit()
                return
            file_name = os.path.join(self.box.paperNativeDir, dir[randint(0, dir_count-1)])
            if windll.kernel32.GetFileAttributesW(file_name) & FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS:
                if isOnline(self.box, net) and isOneDriveFile(self.box, file_name):
                    self.setWallpaper(file_name)
                    self.box.paperHistory.append(file_name)
                    self.box.paperCur = len(self.box.paperHistory) - 1
        self.finished.emit()
