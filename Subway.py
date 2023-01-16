from Config import *
from SubwayLine import SubwayLine
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QScrollArea, QMainWindow, QMenu, QPushButton, QLabel, QMessageBox
)
from PyQt6.QtGui import (
    QCloseEvent
)
from PyQt6.QtCore import (
    Qt, pyqtSlot, pyqtSignal
)
import pathlib
import os.path
from functools import partial
from DynamicStepUnit import DynamicStepUnit, DynamicStartFile
from Toolbox import schema_reader


# Main window for subway lines
class Subway(QWidget):
    schema = []
    # TODO why can't i close myself
    closed = pyqtSignal(QMainWindow)
    info = None

    def __init__(self, info):
        super().__init__()
        self.info=info
        self.setWindowTitle('SubwayGUI File System')
        # Create layout
        self.layout = QVBoxLayout()
        w = QWidget()
        w.setLayout(self.layout)

        self.add_super_buttons()

        self.read_schema()
        width = self.find_start_files()

        # TODO is this the right way?
        # Outermost container of the window is a scrollable area
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setMinimumSize(860, width)
        self.scrollArea.setWidget(w)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    # Add a row of global action buttons
    def add_super_buttons(self):
        layout = QHBoxLayout()
        but1 = QPushButton('Refresh All')
        but1.clicked.connect(self.refresh_all)
        layout.addWidget(but1)
        but2 = QPushButton('Show QC for All')
        but2.clicked.connect(self.show_qc)
        layout.addWidget(but2)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.addLayout(layout)

    # Read and convert schema file to list of dictionary
    def read_schema(self):
        self.schema = schema_reader(self.info['schema'])

    # Find all files that matches the start file in the schema. Each start file will start a new subway line.
    def find_start_files(self):
        start_file_suffix = self.schema[0]['input']
        # Buffer for confirming which start_files to include
        for folder in self.info['folders']:
            start_files = pathlib.Path(folder).rglob('*' + start_file_suffix)
            for start_file in start_files:
                print(start_file)
                w = SubwayLine(schema=self.schema,
                               start_file=start_file)
                self.layout.addWidget(w)
        return w.frameGeometry().width() or 480

    def drop_down(self, event):
        # https://stackoverflow.com/questions/36614635/pyqt-right-click-menu-for-qcombobox
        menu = QMenu()
        refresh = menu.addAction("Refresh all")
        qc = menu.addAction("Show QC for all")
        action = menu.exec(event.pos())
        if action == refresh:
            self.refresh_all()
        else:
            self.show_qc_for_all()

    # Rerun subway with the same folders and schema
    def refresh_all(self):
        self.clear_layout(self.layout)
        self.find_start_files()

    # TODO qc should pop up right after running a step
    def show_qc(self, step, subway_lines=None):
        if not subway_lines:
            subway_lines = range(self.layout.count() - 1)
        for i in subway_lines:
            self.layout.itemAt(i).show_qc(step)

    # https://stackoverflow.com/questions/9374063/remove-all-items-from-a-layout/9383780#9383780
    # TODO might be good as a common asset
    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())

    @pyqtSlot(QCloseEvent)
    def closeEvent(self, a0: QCloseEvent) -> None:
        # properly close myself..there might be better ways to do it
        # https://stackoverflow.com/questions/65356836/how-do-i-remove-every-reference-to-a-closed-windows
        self.closed.emit(self)
        super().closeEvent(a0)

# TODO: drag schema or folder into functioning workspace, but what should be the default behavior? replace current content?

# run all lines till..
# show qc for all lines
