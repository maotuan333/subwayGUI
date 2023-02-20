import sys
from PyQt6.QtWidgets import (
    QApplication,QMainWindow,QWidget,QLabel,QLineEdit,QGridLayout
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('SubwayGUI start page')
        l=QGridLayout()

        label_texts = ['*input: ', '*func: ', 'output: ', 'qc: ']
        line_texts = ['filetype1', 'func1', 'filetype2', '']
        for r, (lt, lit) in enumerate(zip(label_texts, line_texts)):
            print(lt)
            l.addWidget(QLabel(lt), r, 0)
            l.addWidget(QLineEdit(lit), r, 1)

        widget=QWidget()
        widget.setLayout(l)
        self.setCentralWidget(widget)

app=QApplication(sys.argv)
window=MainWindow()
window.show()
sys.exit(app.exec())