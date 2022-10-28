from PyQt6.QtWidgets import (
    QPushButton,QHBoxLayout,QVBoxLayout,QWidget,QLabel,QLineEdit,QDialog,QLineEdit,QGridLayout,QSizePolicy,QFileDialog
)
from PyQt6.QtGui import QIcon,QPixmap,QImage
from PyQt6.QtCore import Qt

class InputStepInfoDialog(QDialog):
    def __init__(self,prev_step=None):
        super().__init__()
        self.boxs = []
        self.info = []
        layout=QGridLayout()
        label_texts=['*input: ','*function: ','output: ','qc: ']
        line_texts=['filetype','func','filetype','']
        if prev_step:
            line_texts=[prev_step,'next_func','next_filetype','']
        for r,(lt,lit) in enumerate(zip(label_texts,line_texts)):
            layout.addWidget(QLabel(lt), r, 0)
            self.boxs.append(QLineEdit(lit))
            layout.addWidget(self.boxs[r], r, 1)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setLayout(layout)

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == Qt.Key.Key_Return:
            for i,box in enumerate(self.boxs):
                self.info.append(box.text())
        self.accept()


class Node_static(QWidget):
    def __init__(self,label):
        super().__init__()
        lo=QVBoxLayout()
        self.setLayout(lo)
        n=QLabel()
        n.setPixmap(QPixmap("C:/Users/damao/PycharmProjects/subway/node_default.png"))
        l=QLabel(label)
        lo.addWidget(n,alignment=Qt.AlignmentFlag.AlignCenter)
        lo.addWidget(l)
        lo.setAlignment(Qt.AlignmentFlag.AlignCenter)


class Node(QWidget):
    QC=None
    def __init__(self,label,glob_path):
        super().__init__()
        lo=QVBoxLayout()
        self.setLayout(lo)
        self.n=QPushButton()
        self.n.setCheckable(True)
        self.n.setFlat(True)
        self.n.setSizePolicy(QSizePolicy.Policy.Maximum,QSizePolicy.Policy.Maximum)
        self.n.setStyleSheet("QPushButton { background-image : url('C:/Users/damao/PycharmProjects/subway/node_default.png') ; "
                             "width:28px;height:28px;border-radius:14px; } \n"
                        "QPushButton:pressed { background-image: url('C:/Users/damao/PycharmProjects/subway/node_failed.png') ;}\n"
                        "QPushButton:disabled { background-image : url('C:/Users/damao/PycharmProjects/subway/node_success.png') ; } \n")
        self.n.clicked.connect(self.onclick)
        l=QLabel(label)
        lo.addWidget(self.n,alignment=Qt.AlignmentFlag.AlignCenter)
        lo.addWidget(l)
        lo.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def onclick(self):
        self.n.setDown(False)
        sucess=True
        if(sucess):
            self.n.setDisabled(True)
        else:
            self.n.setDown(True)


class FunctionArrow_static(QWidget):
    def __init__(self,label):
        super().__init__()
        layout=QVBoxLayout()
        self.setLayout(layout)
        a=QLabel()
        a.setPixmap(QPixmap("C:/Users/damao/PycharmProjects/subway/arrow.png"))
        l=QLabel(label)
        layout.addWidget(l,alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(a)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)


class QC_static(QWidget):
    label=None
