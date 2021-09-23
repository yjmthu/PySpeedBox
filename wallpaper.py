from ntpath import join
from os import path
from time import sleep
from random import randint
from PySide6.QtCore import QThread, QDir

from funcbox import *

class Wallpaper(QThread):
    def __init__(self, box, parent=None) -> None:
        super().__init__(parent=parent)
        self.box = box
    
    def run(self) -> None:
        return super().run()
    
    def set_from_Native(self, net):
        dir = QDir(self.box.paperNativeDir)
        if dir.exists():
            #filters = ["*.png", "*.jpg", "*.jpeg", "*.bmp", "*.wbep"]
            dir.setFilter(QDir.Files | QDir.NoSymLinks)
            dir_count = dir.count()
            if not dir_count:
                if  not isOnline(self.box, False):
                    if isOnline(self.box, True):
                        pass
                return
            file_name = os.path,join(self.box.paperNativeDir, dir[randint(0, dir_count-1)])
        if windll.kernel32.GetFileAttributesW(file_name) & FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS:
            if isOnline(self.box, net):
                if isOneDriveFile(file_name):
                    windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, file_name, SPIF_SENDCHANGE | SPIF_UPDATEINIFILE)
