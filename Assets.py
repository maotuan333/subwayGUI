from PyQt6.QtWidgets import (
    QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QLineEdit, QDialog, QLineEdit, QGridLayout, QSizePolicy,
    QFileDialog
)
from PyQt6.QtGui import QIcon, QPixmap, QImage
from PyQt6.QtCore import Qt
import os.path


class InputStepInfoDialog(QDialog):
    def __init__(self, prev_step=None):
        super().__init__()
        self.script_path = ''
        self.boxes = []
        self.info = []
        layout = QGridLayout()
        label_texts = ['*input: ', '*function: ', 'output: ', 'qc: ']
        line_texts = ['filetype', 'func', 'filetype', '']
        if prev_step:
            line_texts = [prev_step, 'next_func', 'next_filetype', '']
        for r, (lt, lit) in enumerate(zip(label_texts, line_texts)):
            layout.addWidget(QLabel(lt), r, 0)
            self.boxes.append(QLineEdit(lit))
            layout.addWidget(self.boxes[r], r, 1)
            if r == 1:
                but = QPushButton('file')
                but.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                layout.addWidget(but, r, 2)
                but.clicked.connect(self.select_file)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setLayout(layout)

    def select_file(self):
        self.script_path = QFileDialog.getOpenFileName(self, 'select script of the function for this step')[0]
        script_name = os.path.basename(self.script_path).split('.')[0]
        self.boxes[1].setText(script_name)
        self.sender()

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == Qt.Key.Key_Return:
            for i, box in enumerate(self.boxes):
                self.info.append(box.text())
            self.info.append(self.script_path)
        self.accept()


class Node(QWidget):
    def __init__(self, label):
        super().__init__()
        lo = QVBoxLayout()
        self.setLayout(lo)
        n = QLabel()
        n.setPixmap(QPixmap("C:/Users/damao/PycharmProjects/subway/node_default.png"))
        l = QLabel(label)
        lo.addWidget(n, alignment=Qt.AlignmentFlag.AlignCenter)
        lo.addWidget(l)
        lo.setAlignment(Qt.AlignmentFlag.AlignCenter)


class FunctionArrow(QWidget):
    def __init__(self, label):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        a = QLabel()
        a.setPixmap(QPixmap("C:/Users/damao/PycharmProjects/subway/arrow.png"))
        l = QLabel(label)
        layout.addWidget(l, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(a)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)


class QC_static(QWidget):
    label = None
