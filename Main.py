import sys
from PyQt6.QtWidgets import (
    QApplication,QScrollArea,
)
from PyQt6.QtGui import QGuiApplication,QCloseEvent
from DynamicAssets import *
from pathlib import Path
import os.path
from PyQt6.QtCore import pyqtSlot, pyqtSignal


# https://www.pythonguis.com/tutorials/pyqt6-widgets/
# https://stackoverflow.com/questions/47910192/qgridlayout-different-column-width
# https://stackoverflow.com/questions/4286036/how-to-have-a-directory-dialog

'''
work_folder: 'C:/absolute_path/exp_folder' - maximum common filepath of all files in the subway system
subway_folder: '/collection_of_files/yymmdd_Exp_00x' - excluding work_folder, lowest common ancestor of all files in one subway line
start_file = 'C:/absolute_path/exp_folder/collection_of_files/yymmdd_Exp_00x_start_file.ext'
subway_folder = 'C:/absolute_path/exp_folder/collection_of_files'
subway_prefix: 'yymmdd_Exp_00x' - maximum common prefix of all files in one subway line. 
                                    used for display purposes (as title of the subway line)
prev_suffix: '_1st_step.ext1'
my_suffix: '_2nd_step.ext2'
my_fullpath: subway_prefix + my_suffix - the file should satisfy this rule
my_start_file: subway_prefix + prev_suffix
'''
#TODO: refresh function. refresh a subway line or all subway lines. refind all files. this deals with when a file was manually imported/deleted

class SubwayLine(QWidget):
    elements = []
    script_path = ''
    i=1

    def __init__(self, work_folder, start_file, elements_strs):
        super().__init__()
        self.elements=[]
        self.i=1
        self.script_path=''
        self.layout = QVBoxLayout(self)
        self.subway_layout = QHBoxLayout()
        start_file_suffix = elements_strs[0].split("::")[1]
        subway_prefix_fullpath=start_file.rstrip(start_file_suffix)
        self.subway_folder=os.path.dirname(subway_prefix_fullpath)
        self.subway_prefix=os.path.basename(subway_prefix_fullpath)
        self.work_folder = work_folder

        first_node = Node_dynamic(folder=self.subway_folder,prefix=self.subway_prefix,
                                  suffix=start_file_suffix, script_path='',exists=True)
        self.elements.append(first_node)
        self.subway_layout.addWidget(first_node)
        for s in elements_strs[1:]:
            self.add_element(s)

        closeButton=QPushButton()
        closeButton.setText("Close")  # text
        closeButton.setIcon(QIcon("close.png"))  #   # shortcut key
        closeButton.clicked.connect(self.close)

        title = QLabel(self.subway_prefix)
        self.layout.addWidget(closeButton, alignment=Qt.AlignmentFlag.AlignRight)
        self.layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addLayout(self.subway_layout)

    def add_element(self, s):
        elt_type = s.split("::")[0]
        if elt_type == 'File':
            elt = Node_dynamic(folder=self.subway_folder,
                               prefix=self.subway_prefix,
                               suffix=s.split("::")[1],
                               script_path=self.script_path,
                               prev_node=self.elements[self.i-1])
            elt.n.clicked.connect(lambda: self.onclick(self.i))
            self.i+=1
            self.elements.append(elt)
        elif elt_type == 'Function':  # len==3
            [label, self.script_path] = s.split("::")[1:3]
            elt = FunctionArrow(label)
        else:
            elt = QC_static()  # TODO
        self.subway_layout.addWidget(elt)

    def onclick(self, end):
        for i in range(1, end):
            if self.elements[i - 1].file_exists and not self.elements[i].file_exists:
                self.elements[i].onclick()

    def refresh(self):
        for ele in self.elements:
            if ele.file_exists:
                ele.find_file()
        if not self.elements[0].file_exists:
            QMessageBox.warning(self,'Warning','The start file for /''+self.subway_prefix+'/' no longer exists.')
            #or just close it right away



class Subway(QMainWindow):
    strs = []
    closed = pyqtSignal(QMainWindow)

    def __init__(self):
        super().__init__()
        self.strs=[]
        self.layout = QVBoxLayout()
        self.work_folder = QFileDialog.getExistingDirectory(self, 'Choose your work path (folder to scan for files in):').replace('\\','/')
        schema_path = QFileDialog.getOpenFileName(self, 'Choose your schema (template for subway):')[0].replace('\\','/')
        self.read_schema(schema_path)
        width=self.select_start_files()

        # for each starter file found, create a schema
        w = QWidget()
        w.setLayout(self.layout)
        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setMinimumSize(860,width)
        scrollArea.setWidget(w)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setWindowTitle('SubwayGUI File System')
        self.setCentralWidget(scrollArea)
        self.position()
        self.show()

    def read_schema(self,schema_path):
        with open(schema_path, 'r') as file:
            while line := file.readline().rstrip():
                self.strs.append(line)

    def select_start_files(self):
        start_file = self.strs[0].split('::')[-1]
        #buffer for confirming which start_files to include
        start_files=Path(self.work_folder).rglob('*' + start_file)
        for start_file in start_files:
            print(start_file)
            w=SubwayLine(work_folder=os.path.dirname(start_file), start_file=str(start_file).replace('\\','/'), elements_strs=self.strs)
            self.layout.addWidget(w)
        return w.frameGeometry().width() or 480
        #TODO: deletion in schema builder
        # closing subway lines that aren't real subway lines

        # .spb, .ephys, .eye, .mat, -quad

    def position(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().topLeft()
        qr.moveTopLeft(cp)
        self.move(qr.center())

    @pyqtSlot(QCloseEvent)
    def closeEvent(self, a0: QCloseEvent) -> None:
        self.closed.emit(self)
        super().closeEvent(a0)
        #properly close myself..might be better ways to do it
        #https://stackoverflow.com/questions/65356836/how-do-i-remove-every-reference-to-a-closed-windows


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.start_page()

    def start_page(self):
        self.setWindowTitle('Welcome to SubwayGUI!')
        layout = QHBoxLayout()

        rs = QPushButton('Run subway check')
        rs.clicked.connect(self.run_subway)
        layout.addWidget(rs)

        sns = QPushButton('Start new schema')
        sns.clicked.connect(self.start_new_schema)
        layout.addWidget(sns)

        ees = QPushButton('Edit existing schema')
        ees.clicked.connect(self.edit_existing_schema)
        layout.addWidget(ees)

        w = QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)

    def run_subway(self):
        self.wrs = Subway()

    def start_new_schema(self):
        self.wsns = SchemaBuilder()
        self.wsns.show()

    def edit_existing_schema(self):
        pass

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())

