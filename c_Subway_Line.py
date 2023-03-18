from config import *
from PyQt6.QtWidgets import (
    QWidget, QMessageBox, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import os.path
from w_DynamicStepUnit import DynamicStepUnit,DynamicStartFile


class SubwayLine(QWidget):
    i=1 # current index of steps

    def __init__(self, schema, start_file,schema_path):
        super().__init__()
        self.schema_path=schema_path
        self.start_file=start_file

        # Create main layout
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Get file identifier of start file
        start_file_suffix = schema[0].input.show_text

        # Get folder and common prefix of files in this subway line
        prefix_fullpath = pathlib.Path(str(start_file).rstrip(start_file_suffix))
        self.folder = prefix_fullpath.parent
        self.prefix = prefix_fullpath.name

        # Create layout of subway line
        self.subway_layout = QHBoxLayout()

        # Add node for start file
        first_node = DynamicStartFile(folder=self.folder, filename=start_file.name)
        self.subway_layout.addWidget(first_node)

        # Add each following step
        for each_step in schema:
            self.add_step(each_step)

        # Create layout of function buttons
        buttons_layout=QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Refresh button
        refresh_button = QPushButton()
        refresh_button.setText("Refresh")
        refresh_button.clicked.connect(self.refresh)
        buttons_layout.addWidget(refresh_button)

        # Close button
        close_button = QPushButton()
        close_button.setText("Close")
        close_button.clicked.connect(self.close)
        buttons_layout.addWidget(close_button)

        # Organize widgets (top to bottom): function buttons, title, file train
        self.layout.addLayout(buttons_layout)
        title = QLabel(self.prefix)
        self.layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addLayout(self.subway_layout)

    # Wrapper for adding step
    def add_step(self, data):
        i=self.i
        data.pos=i-1
        prev_filepath=self.subway_layout.itemAt(i-1).widget().filepath
        step = DynamicStepUnit(folder=self.folder,
                              prefix=self.prefix,
                              data=data,
                               schema=self.schema_path,
                               prev_filepath=prev_filepath)
        self.subway_layout.addWidget(step)
        # Record current index of step for file generation
        step.node.button.clicked.connect(lambda: self.onclick(i))
        self.i += 1

    # Loop through and generate all files until the target file
    def onclick(self, target):
        for i in range(1,target+1):
            step=self.subway_layout.itemAt(i).widget()
            if not step.file_exists():
                step.onclick()

    # Refresh all the files in subway.
    def refresh(self):
        print('Refreshed subway line:',self.start_file)
        # Refresh each file
        for i in range(self.subway_layout.count()):
            step=self.subway_layout.itemAt(i).widget()
            step.refresh()
        # If the start file no longer exists, this subway line is no longer considered valid.
        if not self.subway_layout.itemAt(0).widget().file_exists():
            qm=QMessageBox.StandardButton
            # Ask user if they want to delete this subway line
            msg='The start file for \''+self.prefix+'  \' no longer exists. Close the subwayline?'
            ans=QMessageBox.question(self, 'Warning', msg, qm.Yes|qm.No)
            if ans==qm.Yes:
                self.deleteLater()