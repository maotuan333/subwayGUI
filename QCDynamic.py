from PyQt6.QtWidgets import (
    QWidget,QMessageBox,QLabel,QVBoxLayout,QPushButton,QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import os.path
import glob
from Config import *


class QCDynamic(QWidget):
    def __init__(self, folder, prefix, suffix):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.fullpath=folder+'/'+prefix+suffix
        self.n=QPushButton()
        self.n.clicked.connect(self.show_img)
        self.n.setStyleSheet(
            "QPushButton { background-image : url('"+ASSETS_FOLDER+"/qc_on.png') ; "
            #"width:28px;height:28px;border-radius:14px; } \n"
            "QPushButton:disabled { background-image : url('"+ASSETS_FOLDER+"/node_success.png') ; } \n")
        layout.addWidget(self.n, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel(prefix + suffix))
        self.refresh()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def show_img(self):
        pic = QLabel(self)
        pic.setPixmap(QPixmap(self.fullpath))
        pic.setWindowTitle(self.fullpath)
        pic.show()

    def set_file_exist(self):
        self.file_exists=True
        self.n.setDisabled(False)
        self.n.setToolTip(self.fullpath)

    def set_file_un_exist(self):
        self.file_exists = False
        self.n.setDisabled(True)
        self.n.setToolTip(None)

    def refresh(self):
        fs = glob.glob(self.fullpath)
        if len(fs)==0:
            self.set_file_un_exist()
        elif len(fs)>1:
            str='found more than one file. List of files: \n'
            for f in fs:
                str=str+f+'\n'
            QMessageBox.warning(self, 'Multiple files found',str)
        else:
            self.set_file_exist()
