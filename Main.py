import sys
from collections import deque
from Assets import *
from PyQt6.QtWidgets import (
    QApplication, QMainWindow,QMessageBox
)
from pathlib import Path
from datetime import date

# https://www.pythonguis.com/tutorials/pyqt6-widgets/
# https://stackoverflow.com/questions/47910192/qgridlayout-different-column-width
# https://stackoverflow.com/questions/4286036/how-to-have-a-directory-dialog


class Subway(QMainWindow):
    def __init__(self):
        super().__init__()
        glob_path = QFileDialog.getExistingDirectory(self, 'Choose your work path (folder to scan for files in):')
        schema_path = QFileDialog.getOpenFileName(self, 'Choose your schema (template for subway):')

        # for each starter file found, create a schema
        for path in Path(glob_path).rglob('*.'):
            pass


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

    def add_element(self, type, typestr,s):
        elt = type(s)
        self.elements.append(elt)
        self.layout.addWidget(elt)
        self.strs.append(typestr+'::'+s)

    def start_adding_nodes(self):
        button = self.sender()
        button.deleteLater()
        info = self.show_input_dialog('Input first step')
        self.add_element(Node_static,'File', info[0])
        self.add_step(info)

    def show_input_dialog(self, str, prev_step=None):
        w = InputStepInfoDialog(prev_step)
        w.setWindowTitle(str)
        w.show()
        if w.exec():
            info=w.info
            w.close()
            return info

    def add_step(self, info):
        # TODO dummy check: cannot input same name twice
        self.add_element(FunctionArrow_static,'Function', info[1])
        # TODO assume at least one step..
        self.add_element(Node_static,'File', info[2])
        if info[3] != '':
            self.add_element(QC_static,'QC', info[3])

    def delete_step(self):
        self.elements.pop()
        self.strs.pop()

    def save_dialog(self):
        qm=QMessageBox
        ans=qm.question(self, '', "Do you want to save the current schema?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if ans==QMessageBox.StandardButton.Yes:
            fn=QFileDialog.getSaveFileName(self,'select','new_schema_'+date.today().strftime('%Y%m%d'),'Text Files (*.txt)')
            with open(fn[0],'w+') as file:
                while self.strs:
                    file.write(self.strs[0]+'\n')
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
