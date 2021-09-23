from threading import Thread
from random import randint

from PySide6.QtCore import QObject, Signal

from funcbox import *

class Wallpaper(QObject):
    finished = Signal()
    isBusy = Signal()
    msgBox = Signal(str, str)
    def __init__(self, box) -> None:
        super().__init__()
        self.box = box
        self.__isRuning = False
        self.finished.connect(self.clean)
    
    def start_next(self) -> None:
        print("线程next启动", self.box.paperHistory)
        if not self.__isRuning:
            self.__isRuning = True
            Thread(target=lambda: self.set_from_Native(True), daemon=True).start()
        else:
            self.isBusy.emit()
    
    def start_prev(self) -> None:
        print("线程prev启动", self.box.paperHistory)
        if not self.__isRuning:
            self.__isRuning = True
            if self.box.paperCur > 0:
                self.box.paperCur -= 1
                print("当前索引：", self.box.paperCur)
                Thread(target=lambda: windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, self.box.paperHistory[self.box.paperCur], SPIF_SENDCHANGE | SPIF_UPDATEINIFILE), daemon=True).start()
            else:
                print("找呀找")
                self.msgBox.emit("找不到更早的壁纸历史记录！", "提示")
            self.finished.emit()
        else:
            print('当前正忙')
            self.isBusy.emit()
    
    def start_remv(self) -> None:
        print("线程remv启动")
        if not self.__isRuning:
            pass
            # self.__isRuning = True
            # Thread(target=lambda: self.set_from_Native(True), daemon=True).start()
        else:
            self.isBusy.emit()
    
    def clean(self):
        self.__isRuning = False
    
    def checkList(self) -> bool:
        if self.box.paperCur + 1 < len(self.box.paperHistory):
            self.box.paperCur += 1
            windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, self.box.paperHistory[self.box.paperCur], SPIF_SENDCHANGE | SPIF_UPDATEINIFILE)
            return True
        return False
    
    def set_from_Native(self, net):
        if self.box.paperCur + 1 < len(self.box.paperHistory):
            self.box.paperCur += 1
            windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, self.box.paperHistory[self.box.paperCur], SPIF_SENDCHANGE | SPIF_UPDATEINIFILE)
        elif os.path.exists(self.box.paperNativeDir):
            print(self.box.paperNativeDir)
            filters = [".png", ".jpg", ".jpeg", ".bmp", ".wbep"]
            dir = list(filter(lambda filename: os.path.splitext(filename)[1] in filters, os.listdir(self.box.paperNativeDir)))
            dir_count = len(dir)
            if not dir_count:
                if  not isOnline(self.box, False):
                    if isOnline(self.box, True):
                        pass
            file_name = os.path.join(self.box.paperNativeDir, dir[randint(0, dir_count-1)])
            if windll.kernel32.GetFileAttributesW(file_name) & FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS:
                if isOnline(self.box, net) and isOneDriveFile(file_name):
                    windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, file_name, SPIF_SENDCHANGE | SPIF_UPDATEINIFILE)
                    self.box.paperHistory.append(file_name)
                    self.box.paperCur = len(self.box.paperHistory) - 1
        print("线程结束")
        self.finished.emit()
