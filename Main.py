import sys
from PyQt6.QtWidgets import (
    QApplication
)
from DynamicAssets import *
from pathlib import Path
import glob


# https://www.pythonguis.com/tutorials/pyqt6-widgets/
# https://stackoverflow.com/questions/47910192/qgridlayout-different-column-width
# https://stackoverflow.com/questions/4286036/how-to-have-a-directory-dialog

class SubwayLine(QWidget):
    elements = []
    script_path = ''
    i=0

    def __init__(self, folder, startfile, elements_strs):

        super().__init__()
        self.work_folder = folder + '/*' + startfile + '*'
        self.layout = QHBoxLayout()
        for s in elements_strs:
            self.add_element(s)

    def add_element(self, s):
        elt_type = s.split("::")[0]
        if elt_type == 'File':
            label = s.split("::")[1]
            elt = Node_dynamic(label, self.work_folder + label, self.script_path)
            elt.n.clicked.connect(lambda: self.onclick(self.i))
            self.i+=1
            self.elements.append(elt)
        elif elt_type == 'Function':  # len==3
            [label, self.script_path] = s.split("::")[1:2]
            elt = FunctionArrow(label)
        else:
            elt = QC_static()  # TODO
        self.layout.addWidget(elt)

    def onclick(self, end):
        for i in range(1, end):
            if self.elements[i - 1].file_exists and not self.elements[i].file_exists:
                self.elements[i].onclick()


class Subway(QMainWindow):
    strs = []

    def __init__(self):
        super().__init__()
        work_folder = QFileDialog.getExistingDirectory(self, 'Choose your work path (folder to scan for files in):')
        schema_path = QFileDialog.getOpenFileName(self, 'Choose your schema (template for subway):')[0]

        self.layout = QVBoxLayout()
        with open(schema_path, 'r') as file:
            while line := file.readline().rstrip():
                self.strs.append(line)
        startfile = self.strs[0].split('::')[-1]
        # for each starter file found, create a schema
        for this_start_file in Path(work_folder).rglob('*' + startfile):
            self.layout.addWidget(SubwayLine(work_folder,this_start_file,self.strs))
        w = QWidget()
        w.setLayout(self.layout)
        self.setCentralWidget(w)
        self.setWindowTitle('SubwayGUI File System')


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
        self.wrs.show()

    def start_new_schema(self):
        self.wsns = SchemaBuilder()
        self.wsns.show()

    def edit_existing_schema(self):
        pass


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
