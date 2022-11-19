from Assets import *
from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox
)
from collections import deque
from datetime import date
import matlab.engine
import os.path
from pathlib import Path
import glob


class SchemaBuilder(QMainWindow):
    elements = deque()
    strs = deque()
    counter = False

    def __init__(self):
        super().__init__()
        self.setWindowTitle('SubwayGUI Work Schema Builder')
        self.layout = QHBoxLayout()
        start_button = QPushButton('Add Node')
        start_button.clicked.connect(self.start_adding_nodes)
        self.layout.addWidget(start_button)
        w = QWidget()
        w.setLayout(self.layout)
        self.setCentralWidget(w)

    def add_element(self, type, typestr, label, filepath=None, manual=None):
        elt = type(label)
        self.elements.append(elt)
        self.layout.addWidget(elt)
        str = typestr + '::' + label
        if manual:
            str += '::null::manual'
        elif filepath:
            str += ('::' + filepath)
        self.strs.append(str)

    def start_adding_nodes(self):
        button = self.sender()
        button.deleteLater()
        info = self.show_input_dialog('Input first step')
        self.add_element(Node, 'File', info[0])
        self.add_step(info)

    def show_input_dialog(self, str, prev_step=None):
        w = InputStepInfoDialog(prev_step)
        w.setWindowTitle(str)
        w.show()
        if w.exec():
            info = w.info
            w.close()
            return info

    def add_step(self, info):
        # TODO dummy check: cannot input same name twice
        self.add_element(FunctionArrow, 'Function', info[1], filepath=info[4], manual=info[5])
        # TODO assume at least one step..
        self.add_element(Node, 'File', info[2])
        if info[3] != '':
            self.add_element(QC_static, 'QC', info[3])

    def delete_step(self):
        self.elements.pop()
        self.strs.pop()

    def save_dialog(self):
        qm = QMessageBox
        ans = qm.question(self, '', "Do you want to save the current schema?",
                          QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if ans == QMessageBox.StandardButton.Yes:
            fn = QFileDialog.getSaveFileName(self, 'Save schema:', 'new_schema_' + date.today().strftime('%Y%m%d'),
                                             'Text Files (*.txt)')
            with open(fn[0], 'w+') as file:
                while self.strs:
                    file.write(self.strs[0] + '\n')
                    self.strs.popleft()

    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.MouseButton.LeftButton:
            if self.counter:  # detect double click
                self.counter = False
                info = self.show_input_dialog('Input next step', prev_step=self.strs[-1].split('::')[-1])
                self.add_step(info)
            else:
                self.counter = True

    def keyReleaseEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key.Key_S:
            self.save_dialog()
            self.close()
        if QKeyEvent.key() == Qt.Key.Key_Delete:
            self.delete_step()


class Node_dynamic(QWidget):
    QC = None
    file_exists = False
    projected_filepath = ''
    filepath = ''

    def __init__(self, folder, prefix, suffix, script_path, prev_node=None,exists=False,step_name=None):
        super().__init__()
        self.fullpath = folder+'/'+prefix+suffix
        self.script_path = script_path
        self.prev_node=prev_node
        lo = QVBoxLayout()
        self.setLayout(lo)
        self.n = QPushButton()
        #self.n.clicked.connect(self.onclick)
        self.n.setCheckable(True)
        self.n.setFlat(True)
        self.n.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.n.setStyleSheet(
            "QPushButton { background-image : url('C:/Users/damao/PycharmProjects/subway/node_default.png') ; "
            "width:28px;height:28px;border-radius:14px; } \n"
            "QPushButton:pressed { background-image: url('C:/Users/damao/PycharmProjects/subway/node_failed.png') ;}\n"
            "QPushButton:disabled { background-image : url('C:/Users/damao/PycharmProjects/subway/node_success.png') ; } \n")
        if exists:
            self.set_file_exist()
        else:
            self.find_file()
        lo.addWidget(self.n, alignment=Qt.AlignmentFlag.AlignCenter)
        lo.addWidget(QLabel(suffix))
        lo.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def set_file_exist(self):
        self.file_exists=True
        self.n.setDisabled(True)
        self.n.setToolTip(self.fullpath)

    def set_file_un_exist(self):
        self.file_exists = False
        self.n.setDisabled(False)
        self.n.setToolTip(None)

    def find_file(self):
        try:
            fs = glob.glob(self.fullpath)
            if(len(fs)>1):
                str='found more than one file. List of files: \n'
                for f in fs:
                    str=str+f+'\n'
                QMessageBox.warning(self, "Multiple files found",str)
            self.set_file_exist()
        except:
            self.set_file_un_exist()

    def onclick(self):
        if not self.file_exists:
            self.n.setDown(False)
            if self.script_path == 'null':
                QMessageBox.about(self, "Manual Step required",
                                  "Manual Step required: Please complete specified manual step and try again!")
                return
            self.generate_file()
            self.find_file()
            if self.file_exists:
                self.n.setDisabled(True)
            else:
                self.n.setDown(True)
                QMessageBox.critical(self, "Warning",
                                     "Failed to generate file: " + self.fullpath + " by running " + self.script_path)

    def str_to_matlab_arg(self,s):
        return "{}".format(s)

    def generate_file(self):
        if not os.path.isfile(self.script_path):
            QMessageBox.critical(self, "Error", "Script " + self.script_path + " does not exist")
        if self.script_path[-2:] == '.m':
            eng = matlab.engine.start_matlab()
            eng.addpath(os.path.dirname(self.script_path))
            try: #maybe should create matlab eng at beginning of whole program an pass in
                command=os.path.basename(self.script_path[:-2]) + \
                        '(\''+self.prev_node.fullpath+'\');'
                eng.eval(command, nargout=0)
            except:
                pass
            eng.exit()
        elif self.script_path[-3:] == '.py':
            try:
                '''$ python argparse_example.py arg'''
                command='python '+self.script_path+' '+self.fullpath
                os.system(command)#TODO
            except:
                return
        else:  # launch software
            QMessageBox.critical(self, "Error", "Function type not supported: only supports .m or .py scripts")


'''
.sbx

//
default path.
select multiple folders.
scroll bar
save configuration. folder. 
good name.
control panel
file part to find file within subway line.
branching and converging?
a pipeline  doens't have to be linear, so it has to be a graph
do you want separate pieplines or one suway line per folder
'''
