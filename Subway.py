from Config import *
from SubwayLine import SubwayLine
from PyQt6.QtWidgets import (
    QWidget,QVBoxLayout,QHBoxLayout,QFileDialog,QScrollArea,QMainWindow,QMenu,QPushButton,QLabel,QMessageBox
)
from PyQt6.QtGui import (
    QCloseEvent,QMouseEvent,QKeyEvent,QIcon
)
from PyQt6.QtCore import (
    Qt,pyqtSlot, pyqtSignal,QEvent
)
from pathlib import Path
import os.path


class Subway(QWidget):
    strs = []
    closed = pyqtSignal(QMainWindow)
    schema_path = None
    work_folders = None

    def __init__(self,work_folders,schema_path):
        super().__init__()
        self.work_folders=work_folders
        self.schema_path=schema_path
        self.setWindowTitle('SubwayGUI File System')
        self.layout = QVBoxLayout()
        self.read_schema()
        width=self.find_start_files()
        w = QWidget()
        w.setLayout(self.layout)
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setMinimumSize(860,width)
        self.scrollArea.setWidget(w)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def read_schema(self):
        if self.schema_path:
            self.strs = []
            with open(self.schema_path, 'r') as file:
                while line := file.readline().rstrip():
                    self.strs.append(line)
        else:
            QMessageBox.warning(self,'Warning','Invalid schema path:' + str(self.schema_path))

    def find_start_files(self):
        if not self.work_folders:
            return 0
        start_file = self.strs[0].split('::')[POS_SUFFIX]
        #buffer for confirming which start_files to include
        for folder in self.work_folders:
            start_files=Path(folder).rglob('*' + start_file)
            for start_file in start_files:
                print(start_file)
                w=SubwayLine(work_folder=os.path.dirname(start_file),
                             start_file=str(start_file).replace('\\','/'), elements_strs=self.strs)
                self.layout.addWidget(w)
        return w.frameGeometry().width() or 480

    def position(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().topLeft()
        qr.moveTopLeft(cp)
        self.move(qr.center())

    def drop_down(self,event):
        # https://stackoverflow.com/questions/36614635/pyqt-right-click-menu-for-qcombobox
        menu = QMenu()
        refresh = menu.addAction("Refresh all")
        action = menu.exec(event.pos())
        if action == refresh:
            self.refresh_all()

    def refresh_all(self):
        self.clearLayout(self.layout)
        self.find_start_files()

    # https://stackoverflow.com/questions/9374063/remove-all-items-from-a-layout/9383780#9383780
    #TODO might be good as a common asset
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    @pyqtSlot(QCloseEvent)
    def closeEvent(self, a0: QCloseEvent) -> None:
        # properly close myself..there might be better ways to do it
        # https://stackoverflow.com/questions/65356836/how-do-i-remove-every-reference-to-a-closed-windows
        self.closed.emit(self)
        super().closeEvent(a0)

#TODO: function - check if txt file is a schema
#TODO: drag schema or folder into functioning workspace, but what should be the default behavior? replace current content?