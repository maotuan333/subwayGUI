from Config import *
from PyQt6.QtWidgets import (
    QVBoxLayout, QWidget, QLabel
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class NodeStatic(QWidget):
    def __init__(self, label, qc_label=None):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        if qc_label:
            qc=QLabel()
            qc.setPixmap(QPixmap(ASSETS_FOLDER+"/qc_on.png"))
            layout.addWidget(qc, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(qc, alignment=Qt.AlignmentFlag.AlignCenter)
        lqc = QLabel(qc_label)
        layout.addWidget(lqc, alignment=Qt.AlignmentFlag.AlignCenter)
        n=QLabel()
        n.setPixmap(QPixmap(ASSETS_FOLDER+"/node_default.png"))
        layout.addWidget(n, alignment=Qt.AlignmentFlag.AlignCenter)
        l = QLabel(label)
        layout.addWidget(l)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)


class FunctionArrow(QWidget):
    def __init__(self, label):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        a = QLabel()
        a.setPixmap(QPixmap(ASSETS_FOLDER+"/arrow.png"))
        l = QLabel(label)
        layout.addWidget(l, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(a)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
