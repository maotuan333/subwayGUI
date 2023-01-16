from Config import *
from PyQt6.QtWidgets import (
    QSplitter,QLabel,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from TabbedWorkspace import TabbedWorkspace

# Sidebar for viewing quality control images and metadata
class QCViewer(TabbedWorkspace):

    def __init__(self):
        super().__init__()

    def add_qc_tab(self,fullpaths,parent_path,tab_title):
        # Workspace is a vertical splitter
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Prepare qc metadata
        qc_meta = QLabel()
        qc_meta.setWordWrap(True)
        meta_exists = False
        meta_str = 'Parent: ' + parent_path + '\n\n'

        # Prepare qc image
        qc_img = QLabel()
        img_exists = False

        # See what's in fullpaths
        for filepath in fullpaths:
            if filepath:
                if filepath.endswith('.txt'): # Found quality control metadata
                    # Extract metadata
                    with open(file, 'r') as file:
                        string = file.read()
                    meta_str += string
                    meta_exists = True

                else: # Found quality control image
                    qc_img.setPixmap(QPixmap(filepath))
                    img_exists = True

        # Create and insert qc img
        if not img_exists:
            qc_img.setText('No quality control metadata available for this step.')
            splitter.insertWidget(0, qc_img)

        # Create and insert qc metadata textbox
        if not meta_exists:
            meta_str += 'No quality control metadata available for this step.'
        qc_meta.setText(meta_str)
        splitter.insertWidget(1,qc_meta)

        # Add tab to QC Viewer
        self.add_tab(splitter, tab_title)