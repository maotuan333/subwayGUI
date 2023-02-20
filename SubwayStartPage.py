import json

from config import *
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox,QFileDialog
)
from PyQt6.QtGui import (
    QKeyEvent, QIcon
)
from PyQt6.QtCore import (
    Qt, pyqtSlot, pyqtSignal
)
from DropOrSelectButton import DropOrSelectButton
SQUARE_BUTTON_MIN_HEIGHT = 200
SQUARE_BUTTON_MAX_WIDTH = 400


class SubwayStartPage(QWidget):
    return_signals = pyqtSignal(dict)
    work_folders = None
    schema_path = None

    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()

        self.folder_button = DropOrSelectButton(title='Select or Drop Folder',
                                                placeholder='Drag in or click to select folders.\n\n'
                                                             '*: Multiple folders are allowed. \n '
                                                             '   Files that are not directories will be\n'
                                                             '   automatically filtered.',
                                                file_dialog_function=QFileDialog.getExistingDirectory,
                                                file_dialog_msg='Choose your work path (folder to scan for files in):',
                                                embedded_text=True,
                                                is_single_file=False,
                                                is_dir=True
                                                )
        self.folder_button.setMinimumHeight(SQUARE_BUTTON_MIN_HEIGHT)
        self.folder_button.setFixedWidth(SQUARE_BUTTON_MAX_WIDTH)

        self.layout.addWidget(self.folder_button)
        self.schema_button = DropOrSelectButton(title='Select or Drop Schema',
                                                placeholder='Drag in or click to select a schema file.\n\n'
                                                             '*: Only a single .json file is allowed.',
                                                file_dialog_function=QFileDialog.getOpenFileName,
                                                file_dialog_msg='Choose your schema (template for subway):',
                                                file_dialog_filter='Schema Files (*.json)',
                                                embedded_text=True
                                                )
        self.schema_button.setMinimumHeight(SQUARE_BUTTON_MIN_HEIGHT)
        self.schema_button.setFixedWidth(SQUARE_BUTTON_MAX_WIDTH)
        self.layout.addWidget(self.schema_button)

        self.layout2 = QVBoxLayout()
        self.layout2.addLayout(self.layout)
        self.next_step_button = QPushButton('Run Subway (click or press Enter)')
        self.next_step_button.clicked.connect(self.get_workspace_info)
        self.layout2.addWidget(self.next_step_button, alignment=Qt.AlignmentFlag.AlignRight)
        self.setLayout(self.layout2)

    def get_workspace_info(self):
        folders = self.folder_button.return_info()
        schema = self.schema_button.return_info()[0]
        if not folders:
            QMessageBox.warning(self, 'Warning', 'Please select work folder(s)!')
            return
        if not schema:
            QMessageBox.warning(self, 'Warning', 'Please select a schema!')
            return
        info=dict(header='Configuration of last subwayGUI run',
                   folders=folders,
                   schema=schema)
        # https://stackoverflow.com/questions/14010731/define-pyqt4-signals-with-a-list-as-argument thank u soooo much
        self.cache_config(info)
        self.return_signals.emit(info)

    def cache_config(self,info):
        """Store run history for 'run the same thing I did last time'."""
        with open(RUN_HISTORY, 'w') as file:
            json.dump(info,file,indent=1)

    @pyqtSlot(QKeyEvent)
    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == Qt.Key.Key_Return:
            self.get_workspace_info()
