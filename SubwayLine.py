from Config import *
from PyQt6.QtWidgets import (
    QWidget, QMessageBox, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from NodeDynamic import NodeDynamic
import os.path
from StaticAssets import FunctionArrow


class SubwayLine(QWidget):

    def __init__(self, work_folder, start_file, elements_strs):
        super().__init__()
        self.elements = []
        self.i = 1
        self.layout = QVBoxLayout(self)
        buttons_layout=QHBoxLayout()
        self.subway_layout = QHBoxLayout()
        start_file_suffix = elements_strs[0].split('::')[POS_SUFFIX]
        subway_prefix_fullpath = start_file.rstrip(start_file_suffix)
        self.subway_folder = os.path.dirname(subway_prefix_fullpath)
        self.subway_prefix = os.path.basename(subway_prefix_fullpath)
        self.work_folder = work_folder

        first_node = NodeDynamic(folder=self.subway_folder, prefix=self.subway_prefix,
                                 suffix=start_file_suffix, exists=True)
        self.elements.append(first_node)
        self.subway_layout.addWidget(first_node)
        for s in elements_strs[1:]:
            self.add_element(s)

        refresh_button = QPushButton()
        refresh_button.setText("Refresh")
        refresh_button.clicked.connect(self.refresh)
        buttons_layout.addWidget(refresh_button)

        close_button = QPushButton()
        close_button.setText("Close")  # text
        close_button.setIcon(QIcon("close.png"))  # # shortcut key
        close_button.clicked.connect(self.close)
        buttons_layout.addWidget(close_button)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        title = QLabel(self.subway_prefix)
        self.layout.addLayout(buttons_layout)
        self.layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addLayout(self.subway_layout)

    def add_element(self, s):
        splitted=s.split('::')
        elt_type =splitted[POS_TYPE]
        if elt_type == 'File':
            try:
                _=splitted[POS_IS_MANUAL]
                manual=True
            except:
                manual=False
            elt = NodeDynamic(folder=self.subway_folder,
                              prefix=self.subway_prefix,
                              suffix=splitted[POS_SUFFIX],
                              script_path=splitted[POS_SCRIPT],
                              qc_suffix=splitted[POS_QC],
                              readme_path=splitted[POS_README],
                              prev_node=self.elements[self.i - 1],
                              manual=manual)
            self.elements.append(elt)
            i=self.i
            elt.n.clicked.connect(lambda: self.onclick(i))
            self.i += 1
        elif elt_type == 'Function':  # len==3
            label = s.split("::")[POS_SUFFIX]
            elt = FunctionArrow(label)
        self.subway_layout.addWidget(elt)

    def onclick(self, end):
        for i in range(1, end+1):
            if self.elements[i - 1].file_exists and not self.elements[i].file_exists:
                self.elements[i].onclick()

    def refresh(self):
        for ele in self.elements:
            if ele.file_exists:
                ele.refresh()
        if not self.elements[0].file_exists:
            qm=QMessageBox.StandardButton
            ans=QMessageBox.question(self, 'Warning', 'The start file for \''+self.subway_prefix+'  \' no longer exists. Close the subwayline?', qm.Yes|qm.No)
            if ans==qm.Yes:
                self.deleteLater()
            # or just close it right away
