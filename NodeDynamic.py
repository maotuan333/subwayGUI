import glob
import os.path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QMessageBox, QLabel, QVBoxLayout, QPushButton, QSizePolicy
)

from Config import *


class NodeDynamic(QWidget):
    def __init__(self, folder, prefix, suffix, exists=False, script_path=None, readme_path=None, prev_node=None,
                 manual=False):
        super().__init__()
        self.fullpath = folder + '/' + prefix + suffix
        self.script_path = script_path
        self.prev_node = prev_node
        self.manual = manual
        self.readme_path = readme_path
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.n = QPushButton()
        # self.n.clicked.connect(self.onclick) - for the purpose of chain reaction this is moved to subwayline
        self.n.setCheckable(True)
        self.n.setFlat(True)
        self.n.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.n.setStyleSheet(
            "QPushButton { background-image : url('"+ASSETS_FOLDER+"/node_default.png') ; "
            "width:28px;height:28px;border-radius:14px; } \n"
            "QPushButton:pressed { background-image: url('"+ASSETS_FOLDER+"/node_failed.png') ;}\n"
            "QPushButton:disabled { background-image : url('"+ASSETS_FOLDER+"/node_success.png') ; } \n")
        if exists:
            self.set_file_exist()
        else:
            self.refresh()
        layout.addWidget(self.n, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel(prefix+suffix))
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def set_file_exist(self):
        self.file_exists=True
        self.n.setDisabled(True)
        self.n.setToolTip(self.fullpath)

    def set_file_un_exist(self):
        self.file_exists = False
        self.n.setDisabled(False)
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

    def onclick(self):
        if not self.file_exists:
            self.n.setDown(False)
            if self.manual:
                if self.readme_path != DEFAULT_NO_README:
                    with open(self.readme_path,'r') as f:
                        msg = f.read()
                else:
                    msg = 'Manual Step required: Please complete specified manual step and try again!'
                QMessageBox.about(self, 'Manual Step required', msg)
                return
            self.generate_file()
            self.refresh()
            if self.file_exists:
                self.n.setDisabled(True)
            else:
                self.n.setDown(True)
                QMessageBox.critical(self, "Warning",
                                     "Failed to generate file: " + self.fullpath + " by running " + self.script_path)

    def generate_file(self):
        if not os.path.isfile(self.script_path):
            QMessageBox.critical(self, "Error", "Script " + self.script_path + " does not exist")
        if self.script_path[-2:] == '.m':
            MATLAB_ENGINE.addpath(os.path.dirname(self.script_path))
            try: #maybe should create matlab eng at beginning of whole program an pass in
                command= os.path.basename(self.script_path[:-2]) + \
                        '(\'' + self.prev_node.filepath + '\');'
                MATLAB_ENGINE.eval(command, nargout=0)
            except:
                pass
        elif self.script_path[-3:] == '.py':
            try:
                '''$ python argparse_example.py arg'''
                command='python '+self.script_path+' '+self.fullpath
                os.system(command)#TODO
            except:
                return
        else:  # launch software
            QMessageBox.critical(self, "Error", "Function type not supported: only supports .m or .py scripts")

