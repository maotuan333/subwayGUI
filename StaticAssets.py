from Config import *
from PyQt6.QtWidgets import (
    QVBoxLayout, QWidget, QLabel
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

ALIGNMENT=Qt.AlignmentFlag.AlignCenter


# Static file node, contains a node icon and a label beneath it
class NodeStatic(QWidget):
    def __init__(self, label, qc_img=None,qc_meta=None):
        super().__init__()
        # Create layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(ALIGNMENT)

        # Add icon for QC
        qc = QLabel()
        if qc_img or qc_meta:
            qc.setPixmap(QPixmap(str(ASSETS_FOLDER/ "qc_on.png")))
        else:
            qc.setPixmap(QPixmap(str(ASSETS_FOLDER/ "qc_off.png")))

        # Add icon and label for node
        layout.addWidget(qc, alignment=ALIGNMENT)
        n=QLabel()
        n.setPixmap(QPixmap(str(ASSETS_FOLDER/ "node_default.png")))
        layout.addWidget(n, alignment=ALIGNMENT)
        l = QLabel(label)
        layout.addWidget(l,alignment=ALIGNMENT)


# Static step arrow, contains an arrow and name of the function on top
class FunctionArrow(QWidget):
    def __init__(self, label):
        super().__init__()
        # Create layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(ALIGNMENT)

        # Add icon and label of function
        l = QLabel(label)
        layout.addWidget(l, alignment=ALIGNMENT)
        a = QLabel()
        a.setPixmap(QPixmap(str(ASSETS_FOLDER/"arrow.png")))
        layout.addWidget(a)