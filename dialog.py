import os
from pathlib import Path

from PySide6.QtWidgets import QButtonGroup, QComboBox, QHBoxLayout, QPushButton, QSlider
from PySide6.QtCore import QEvent, QFile, QObject, QSize, Qt, QSettings
from PySide6.QtGui import QMouseEvent, QShowEvent, QIcon
from PySide6.QtUiTools import QUiLoader

from funcbox import *
from speedwidget import SpeedWidget

TASK_DESK_SUB = "HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced"
SHOW_SECONDS_IN_SYSTEM_CLOCK = "ShowSecondsInSystemClock"
TASKBAR_ACRYLIC_OPACITY = "TaskbarAcrylicOpacity"
reg_keys = [
    "HKEY_CURRENT_USER\\SOFTWARE\\Classes\\*\\shell\\QCoper",
    "HKEY_CURRENT_USER\\SOFTWARE\\Classes\\Directory\\shell\\QCoper",
    "HKEY_CURRENT_USER\\SOFTWARE\\Classes\\Directory\\Background\\shell\\QCoper",
    "mshta vbscript:clipboarddata.setdata(\"text\",\"%%1\")(close)"
]

class Dialog(SpeedWidget):

    def __init__(self, box)->None:
        super().__init__()
        self.box = box
        self.initUi()
        self.initChildren()
        self.initConnections()
        self.initOthers()
    
    def initUi(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint)
        self.setWindowIcon(QIcon("./icons/speedbox.ico"))
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(5, 5, 5, 5)
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

        self.move((self.box.ScreenWidth - self.width()) / 2, (self.box.ScreenHeight - self.height()) / 2)
        self.ui.setStyleSheet("QFrame{background-color:rgba(0, 0, 0, 100);}QLabel{border-radius: 3px;background-color: transparent;}Line{background-color:black};")
        self.initSpeedBox(self.ui, self.showMinimized, self.close)

    def setTheme(self):
        self.ui.setStyleSheet("QFrame{background-color:rgba(%1);} QLabel{border-radius: 3px;background-color: transparent;}Line{background-color:black};")
        self.jobTip.showTip("设置成功！")
    
    def initChildren(self):
        self.buttonGroup = QButtonGroup()
    
    def initConnections(self):
        self.ui.rBtnNative.toggled.connect(lambda checked: self.ui.BtnChooseFolder.setEnabled(checked))
        self.ui.sLdTimeInterval.valueChanged.connect(lambda value: self.ui.labTimeInterval.setText(str(value)))
        self.ui.cBxAutoStart.clicked.connect(self.setAppAutoStart)

    def initOthers(self):
        self.buttonGroup.addButton(self.ui.rBtnDefault, 0)
        self.buttonGroup.addButton(self.ui.rBtnCode, 1)
        self.buttonGroup.addButton(self.ui.rBtnBing, 2)
        self.buttonGroup.addButton(self.ui.rBtnNative, 3)
        self.buttonGroup.addButton(self.ui.rBtnScript, 4)
        self.buttonGroup.setExclusive(True)

        # pBtns = self.ui.findChildren(QPushButton)
        # for pBtn in pBtns:
        #     pBtn.installEventFilter(self)
        sliders = self.ui.findChildren(QSlider)
        for slider in sliders:
            slider.installEventFilter(self)
        combs = self.ui.findChildren(QComboBox)
        for comb in combs:
            comb.installEventFilter(self)
    
    def showEvent(self, event: QShowEvent) -> None:
        self.ui.lineNativePaperPath.setText(self.box.paperNativeDir)
        self.ui.chkAutoChangePaper.setChecked(self.box.paperAutoChange)
        self.ui.chkChangeWhenStart.setChecked(self.box.paperChangeWhenStart)
        self.ui.sLdTimeInterval.setValue(self.box.paperTimeInterval)
        self.ui.lineAppData.setText(get_dat_path())
        self.ui.line_APP_ID.setText(self.box.fanyerAppId)
        self.ui.line_PASS_WORD.setText(self.box.fanyerPassWord)
        self.ui.cBxAutoStart.setChecked(QSettings("HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", QSettings.NativeFormat).value("PySpeedBox", "", str) == ("cscript //Nologo \"%s\"" % os.path.join(get_dir_path(), "start.vbs")))
        self.ui.BtnChooseFolder.setEnabled(self.ui.rBtnNative.isChecked())
        self.ui.chkFile.setChecked(QSettings(reg_keys[0], QSettings.NativeFormat).contains("."))
        self.ui.chkFolder.setChecked(QSettings(reg_keys[1], QSettings.NativeFormat).contains("."))
        self.ui.chkFolderBack.setChecked(QSettings(reg_keys[2], QSettings.NativeFormat).contains("."))
        self.ui.chkTimeUnit_sec.setChecked(QSettings(TASK_DESK_SUB, QSettings.NativeFormat).contains(SHOW_SECONDS_IN_SYSTEM_CLOCK))
        self.buttonGroup.button(self.box.paperType).setChecked(True)

        #self.ui.BtnChooseFolder.setEnabled(last_checked_button == 7)
        return super().showEvent(event)
    
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if isinstance(watched, QComboBox):
            if event.type() == QEvent.MouseMove:
                return True
        elif isinstance(watched, QSlider):
            env: QMouseEvent = event
            tar: QSlider = watched
            if event.type() == QEvent.MouseMove:
                tar.setValue(env.position().x() / tar.width() * (tar.maximum() - tar.minimum()) + tar.minimum())
                return True
            if event.type() == QEvent.MouseButtonPress:
                tar.setValue(env.position().x() / tar.width() * (tar.maximum() - tar.minimum()) + tar.minimum())
                tar.setMouseTracking(True)
                return True
            elif event.type() == QEvent.MouseButtonRelease:
                tar.setMouseTracking(False)
                return True
            else:
                pass
        return super().eventFilter(watched, event)
    
    def setAppAutoStart(self, checked: bool) -> None:
        reg = QSettings(
            "HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",
            QSettings.NativeFormat)
        if checked:
            reg.setValue("PySpeedBox", "cscript //Nologo \"%s\"" % os.path.join(get_dir_path(), "start.vbs"))
        else:
            reg.remove("PySpeedBox")
        self.jobTip.showTip("修改成功！")
