from config import *
from c_Subway_Line import SubwayLine
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,  QScrollArea, QMainWindow, QMenu, QPushButton,QLabel
)
from PyQt6.QtGui import (
    QCloseEvent
)
from PyQt6.QtCore import (
    Qt, pyqtSlot, pyqtSignal
)
import pathlib
from util import schema_reader


# Main window for subway lines
class Subway(QWidget):
    schema = []
    closed = pyqtSignal(QMainWindow)
    info = None
    width=480
    start_files=[]

    def __init__(self, info):
        super().__init__()
        self.info=info
        self.setWindowTitle('SubwayGUI File System')
        # Create layout
        self.layout = QVBoxLayout()
        w = QWidget()
        w.setLayout(self.layout)
        self.schema = schema_reader(self.info['schema'])
        self.find_start_files()
        if len(self.start_files)==0:
            self.add_empty_page()
        else:
            self.add_super_buttons()

        # Outermost container of the window is a scrollable area
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setMinimumSize(860, self.width)
        self.scrollArea.setWidget(w)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def add_empty_page(self):
        self.layout.addWidget(QLabel("No start files found.\n\n Your start file suffix is: '"+\
                                self.schema[0].input.show_text+"'"))

    # Add a row of global action buttons
    def add_super_buttons(self):
        layout = QHBoxLayout()
        but1 = QPushButton('Refresh All')
        but1.clicked.connect(self.refresh_all)
        layout.addWidget(but1)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.addLayout(layout)

    # Find all files that matches the start file in the schema. Each start file will start a new subway line.
    def find_start_files(self):
        # Buffer for confirming which start_files to include
        for folder in self.info['folders']:
            self.start_files = [x for x in pathlib.Path(folder).rglob('*' + self.schema[0].input.show_text)]
            for start_file in self.start_files:
                print(start_file)
                w = SubwayLine(schema=self.schema,
                               start_file=start_file,
                               schema_path=self.info['schema'])
                self.layout.addWidget(w)
                self.width=w.frameGeometry().width()


    def drop_down(self, event):
        menu = QMenu()
        refresh = menu.addAction("Refresh all")
        action = menu.exec(event.pos())
        if action == refresh:
            self.refresh_all()

    # Rerun subway with the same folders and schema
    def refresh_all(self):
        self.clear_layout(self.layout)
        self.find_start_files()

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
