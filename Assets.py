from PyQt6.QtWidgets import (
    QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QLineEdit, QDialog, QLineEdit, QGridLayout, QSizePolicy,QCheckBox,
    QFileDialog
)
from PyQt6.QtGui import QIcon, QPixmap, QImage
from PyQt6.QtCore import Qt
import os.path
from functools import partial

class InputStepInfoDialog(QDialog):
    def __init__(self, prev_step=None):
        super().__init__()
        self.script_path = ''
        self.boxes = []
        self.info = []
        self.function_is_manual_checkbox = QCheckBox()
        layout = QGridLayout()
        label_texts = ['*input: ', '*function: ', 'output: ', 'qc: ']
        line_texts = ['filetype', 'func', 'filetype', '']
        if prev_step:
            line_texts = [prev_step, 'next_func', 'next_filetype', '']
        for r, (lt, lit) in enumerate(zip(label_texts, line_texts)):
            if r>1:
                rr=r+1
            else:
                rr = r
            if r==1:
                layout.addWidget(self.function_is_manual_checkbox, 2, 0)
                layout.addWidget(QLabel('This is a manual step'), 2, 1)
            layout.addWidget(QLabel(lt), rr, 0)
            self.boxes.append(QLineEdit(lit))
            layout.addWidget(self.boxes[r], rr, 1)
            but = QPushButton('file')
            but.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            layout.addWidget(but, rr, 2)
            but.clicked.connect(partial(self.select_file, r))

        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setLayout(layout)

    def select_file(self,i):
        file_path = QFileDialog.getOpenFileName(self, 'select file/script of the function for this step')[0]
        file_name = os.path.basename(file_path)
        self.boxes[i].setText(file_name)
        if i == 1:
            self.script_path = file_path

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == Qt.Key.Key_Return:
            for i, box in enumerate(self.boxes):
                self.info.append(box.text())
                if self.script_path=='' and i==1:
                    self.script_path=box.text()
            self.info.append(self.script_path)
            self.info.append(self.function_is_manual_checkbox.isChecked())
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
