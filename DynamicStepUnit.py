from PyQt6.QtWidgets import (
    QGridLayout, QLabel, QVBoxLayout, QSizePolicy
)
from PyQt6.QtCore import Qt
from Config import *
from FileStatusButton import *
from StaticAssets import FunctionArrow
import os.path
from functools import partial

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
        self.qc = None
        self.layout.addWidget(self.node, 0, 1)
        self.format_node()
        # TODO should we allow QC for start file?

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
# a function arrow, a button for the file to be generated, and any qc.
class DynamicStepUnit(QWidget):
    def __init__(self, folder, prefix, info):
        super().__init__()
        self.prefix=prefix
        self.info = info
        self.label = prefix + self.info['output']
        self.fullpath = folder / self.label
        self.prev_fullpath = folder / prefix / self.info['input']
        self.script_path = self.info['script_path']

        # create layout
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # draw function arrow
        self.layout.addWidget(FunctionArrow(self.info['func']), 1, 0)

        # draw node
        self.add_node()

        # draw QC
        if self.info.get('qc_img') or self.info.get('qc_meta'):
            self.add_qc()
        # layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # UI of node
    def add_node(self):
        # Create node with icon urls
        self.node = FileStatusButton(fullpath=self.fullpath,
                                     img_not_found=ASSETS_FOLDER / "node_default.png",
                                     img_found=ASSETS_FOLDER / "node_success.png",
                                     img_failed=ASSETS_FOLDER / "node_failed.png",
                                     msg_failed = "Failed to generate file: " + str(self.fullpath) + " by running " + self.script_path)
        # Add to lower right slot
        self.layout.addWidget(self.node, 1, 1)

        # Create layout around node
        layout = QVBoxLayout()
        layout.addWidget(self.node.button, alignment=ALIGN_CENTER)
        layout.addWidget(QLabel(self.label), alignment=ALIGN_CENTER)
        self.node.setLayout(layout)

        # Format node UI
        self.node.button.setCheckable(True)  # TODO
        self.node.button.setFlat(True)  # TODO
        self.node.button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        # background-image : url('"+ASSETS_FOLDER+"/node_default.png') ;
        # "QPushButton:pressed { background-image: url('"+ASSETS_FOLDER+"/node_failed.png') ;}\n"
        # "QPushButton:disabled { background-image : url('"+ASSETS_FOLDER+"/node_success.png') ; } \n")

    # UI of qc
    def format_qc(self):
        # Create QC button with icon urls
        self.qc = FileStatusButton(fullpath=[self.prefix + self.info.get('qc_img'), self.prefix + self.info.get('qc_meta')],
                                img_not_found = ASSETS_FOLDER / "qc_default.png",
                                img_partial = ASSETS_FOLDER / "qc_partial.png",
                                img_found = ASSETS_FOLDER / "qc_success.png",
                                msg_partial = "One of the qc format failed to generate. You might want to check manually!")
        # Add to upper right slot
        self.layout.addWidget(self.qc, 0, 1)

        # Connect QC button to global QC viewer
        self.qc.button.clicked.connect(partial(GLOBAL_QC_HANDLE.add_qc_tab,
                                            self.qc.fullpath, # fullpaths
                                            self.fullpath,  # parent_path
                                            self.label + '\'s Quality Control'))  # tab_title

    # Wrapper for generating output file on click
    def onclick(self):
        # If the step required to generate output file is manual
        if not self.script_path:
            # protocol exists, display protocol
            if self.info.get('readme'):
                with open(self.info['readme'], 'r') as f:
                    msg = f.read()
            # no protocol, show default message
            else:
                msg = "Manual step required: Please complete '" + self.info['func'] + "' and try again."
            QMessageBox.about(self, 'Manual Step required', msg)
            return
        # The step has a script associated with it.
        # Generate output file and update status
        self.generate_file()

    # Execute processing script to generate output file
    def generate_file(self):
        # Check if script exists
        if not os.path.isfile(self.script_path):
            QMessageBox.critical(self, "Error", "'" + self.script_path + "' does not exist")

        # If MATLAB script:
        if self.script_path[-2:] == '.m':
            # Matlab engine had been activated in config
            MATLAB_ENGINE.addpath(os.path.dirname(self.script_path))
            try:  # Run script
                command = os.path.basename(self.script_path[:-2]) + "('" + self.prev_fullpath + "');"
                MATLAB_ENGINE.eval(command, nargout=0)
            except:
                pass

        # If Python script:
        elif self.script_path[-3:] == '.py':
            try:  # $ python argparse_example.py arg
                command = 'python ' + self.script_path + ' ' + self.fullpath
                os.system(command)  # TODO The first arg by default is input file path. more args?
            except:
                pass
        else:  # TODO launch software
            QMessageBox.critical(self, "Error", "Function type not supported: only supports .m or .py scripts")
        # Check if file has been generated
        self.refresh(set_fail=True)
        # Automatically show QCs if they were generated
        if self.qc_exists():
            self.show_qc()

    def show_qc(self):
        self.qc.show()

    # Check if output file had been generated
    #TODO: does not check for QC...
    def file_exists(self):
        return self.node.files_status == Status.FOUND

    def qc_exists(self):
        try:
            return self.qc and self.qc.files_status == Status.FOUND
        except:
            return False

    # Update node and qc files status
    def refresh(self,set_fail=False):
        self.node.refresh(set_fail=set_fail)
        try:
            self.qc.refresh(set_fail=set_fail)
        except:
            pass