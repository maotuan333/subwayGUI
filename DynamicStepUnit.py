import os.path
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QGridLayout, QLabel, QVBoxLayout, QSizePolicy
)
from config import *
from FileStatusButton import *
from StaticAssets import FunctionArrow

ALIGN_CENTER = Qt.AlignmentFlag.AlignCenter


# A widget representing the first file of a schema.
class DynamicStartFile(QWidget):
    def __init__(self, folder, prefix, suffix):
        super().__init__()
        self.label = prefix + suffix
        self.fullpath = folder / self.label

        # create layout
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.node = FileStatusButton(fullpath=self.fullpath,
                                     img_not_found=ASSETS_FOLDER / "node_default.png",
                                     img_found=ASSETS_FOLDER / "node_success.png")
        self.layout.addWidget(self.node, 0, 1)
        self.format_node()

    # UI of node
    def format_node(self):
        layout = QVBoxLayout()
        layout.addWidget(self.node.button, alignment=ALIGN_CENTER)
        layout.addWidget(QLabel(self.label), alignment=ALIGN_CENTER)
        self.node.setLayout(layout)

        # Format button
        self.node.button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

    def file_exists(self):
        return self.node.files_status != Status.FOUND

# A widget representing all elements of a processing step:
# a function arrow and a button for the file to be generated.
class DynamicStepUnit(QWidget):
    def __init__(self, folder, prefix, data):
        super().__init__()
        self.data = data
        self.filename = prefix + self.data.output.show_text
        self.filepath = folder / (prefix + self.data.output.show_text)
        self.prev_filepath = folder / (prefix + self.data.input.show_text)

        # create layout
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        # draw function arrow
        self.layout.addWidget(FunctionArrow(self.data.func.show_text), 1, 0)
        # draw node
        self.add_node()

    # UI of node
    def add_node(self):
        # Create node with icon urls
        self.node = FileStatusButton(fullpath=self.filepath,
                                     img_not_found=ASSETS_FOLDER / "node_default.png",
                                     img_found=ASSETS_FOLDER / "node_success.png",
                                     img_failed=ASSETS_FOLDER / "node_failed.png",
                                     msg_failed = "Failed to generate file: " + str(self.filepath)
                                                  + " by running " + self.data.func.filepath)
        # Add to lower right slot
        self.layout.addWidget(self.node, 1, 1)

        # Create layout around node
        layout = QVBoxLayout()
        layout.addWidget(self.node.button, alignment=ALIGN_CENTER)
        layout.addWidget(QLabel(self.filename), alignment=ALIGN_CENTER)
        self.node.setLayout(layout)

        # Format node UI
        self.node.button.setCheckable(True)  # TODO
        self.node.button.setFlat(True)  # TODO
        self.node.button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

    # Wrapper for generating output file on click
    def onclick(self):
        # If the step required to generate output file is manual
        if self.data.func.is_manual:
            msg = "Manual step required: Please complete '" + self.data.func.show_text + "' and try again."
            QMessageBox.about(self, 'Manual Step required', msg)
        else:
            # Generate output file and update status
            self.generate_file()
        # Display protocol if exists
        if self.data.readme.filepath:
            with open(self.data.readme.filepath, 'r') as f:
                msg = f.read()
            QMessageBox.about(self, 'Protocol', msg)

    # Execute processing script to generate output file
    def generate_file(self):
        # Check if script exists
        if not os.path.isfile(self.data.func.data):
            QMessageBox.critical(self, "Error", "'" + self.data.func.data + "' does not exist")

        # If MATLAB script:
        if self.data.func.data[-2:] == '.m':
            # Matlab engine had been activated in config
            MATLAB_ENGINE.addpath(os.path.dirname(self.data.func.data))
            try:  # Run script
                command = os.path.basename(self.data.func.data[:-2]) + "('" + self.prev_filepath + "');"
                MATLAB_ENGINE.eval(command, nargout=0)
            except:
                pass

        # If Python script:
        elif self.data.func.data[-3:] == '.py':
            try:  # $ python argparse_example.py arg
                command = 'python ' + self.data.func.filepath + ' ' + self.filepath
                os.system(command)
            except:
                pass
        else:
            QMessageBox.critical(self, "Error", "Function type not supported: only supports .m or .py scripts")
        # Check if file has been generated
        self.refresh(set_fail=True)

    # Check if output file had been generated
    def file_exists(self):
        return self.node.files_status == Status.FOUND

    # Update node files status
    def refresh(self,set_fail=False):
        self.node.refresh(set_fail=set_fail)