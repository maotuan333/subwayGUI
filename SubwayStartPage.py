import os.path

from Config import *
from PyQt6.QtWidgets import (
    QWidget,QVBoxLayout,QHBoxLayout,QFileDialog,QScrollArea,QMainWindow,QMenu,QPushButton,QLabel,QMessageBox,QDialog
)
from PyQt6.QtGui import (
    QCloseEvent,QMouseEvent,QKeyEvent,QIcon
)
from PyQt6.QtCore import (
    Qt,pyqtSlot, pyqtSignal,QEvent
)


class DropOrSelectButton(QPushButton):
    files = None

    def __init__(self, label, type='folder'):
        super().__init__()
        self.type=type
        self.setFlat(True)
        self.setAutoFillBackground(True)
        self.setIcon(QIcon(ASSETS_FOLDER + "drop_or_select_button.png"))
        self.setAcceptDrops(True)
        self.label = label
        self.setText(label)
        self.clicked.connect(self.files_selector)
        if type=='folder':
            self.setText('Drag in or click to select folders.\n\n'
                         '*: Multiple folders are allowed. \n '
                         '   Files that are not directories will be\n'
                         '   automatically filtered.')
        else: # elif type=='schema'
            self.setText('Drag in or click to select a schema file.\n\n'
                         '*: Only a single .txt file is allowed.')


    def files_selector(self):
        if self.type=='folder':
            msg = 'Choose your work path (folder to scan for files in):'
            file = QFileDialog.getExistingDirectory(self, msg).replace('\\', '/')
        else:# elif type=='schema'
            msg = 'Choose your schema (template for subway):'
            file = QFileDialog.getOpenFileName(self, msg, filter='Schema Files (*.txt)').replace('\\', '/')
        if file:
            self.clear()
            self.set_info([file])

    def set_info(self,info):
        self.files = info
        self.setText('\n'.join(self.files))

    def clear(self):
        self.files = None
        self.setText(self.label)

    # https://www.youtube.com/watch?v=KVEIW2htw0A
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            if self.type=='schema':
                if len(event.mimeData().urls()) > 1:
                    return
                s=str(event.mimeData().urls()[0].toLocalFile())
                if s.split('.')[-1]!='txt':
                    return
            event.accept()
            event.setDropAction(Qt.DropAction.CopyAction)
            self.clear()
            files=[]
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    s = str(url.toLocalFile())
                    if self.type=='folder' and not os.path.isdir(s):
                        continue
                    files.append(s)
            self.set_info(files)
        else:
            event.ignore()

    def return_info(self):
        if self.type=='folder' and type(self.files)==str:
            return [self.files]
        if self.type=='schema' and type(self.files)==list:
            return self.files[0]
        return self.files


class SubwayStartPage(QWidget):
    return_signals = pyqtSignal(list,str)
    work_folders = None
    schema_path = None

    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.folder_button = DropOrSelectButton('Select or Drop Folder')
        self.layout.addWidget(self.folder_button)
        self.schema_button = DropOrSelectButton('Select or Drop Schema', type='schema')
        self.layout.addWidget(self.schema_button)
        self.layout2 = QVBoxLayout()
        self.layout2.addLayout(self.layout)
        self.next_step_button = QPushButton('Run Subway (click or press Enter)')
        self.next_step_button.clicked.connect(self.get_workspace_info)
        self.layout2.addWidget(self.next_step_button, alignment=Qt.AlignmentFlag.AlignRight)
        self.setLayout(self.layout2)
        #self.setWindowModality(Qt.WindowModality.WindowModal)

    def get_workspace_info(self):
        self.work_folders=self.folder_button.return_info()
        self.schema_path=self.schema_button.return_info()
        if not self.work_folders:
            QMessageBox.warning(self, 'Warning', 'Please select work folder(s)!')
            return
        if not self.schema_path:
            QMessageBox.warning(self,'Warning','Please select a schema!')
            return
        #https://stackoverflow.com/questions/14010731/define-pyqt4-signals-with-a-list-as-argument thank u soooo much
        self.return_signals.emit(self.work_folders,self.schema_path)

    @pyqtSlot(QKeyEvent)
    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == Qt.Key.Key_Return:
            self.get_workspace_info()