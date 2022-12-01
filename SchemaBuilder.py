from Config import *
from StaticAssets import NodeStatic,FunctionArrow
from InputStepInfoDialog import InputStepInfoDialog
from PyQt6.QtWidgets import (
    QWidget,QMessageBox,QHBoxLayout,QPushButton,QFileDialog
)
from PyQt6.QtCore import Qt
from datetime import date

class SchemaBuilder(QWidget):
    elements = []
    strs = []
    counter = False

    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.prev_step=None
        self.add_start_button()
        self.setLayout(self.layout)

    def add_start_button(self):
        start_button = QPushButton('Add Node')
        start_button.setFocusPolicy(Qt.FocusPolicy.NoFocus) #can't delete or save at first step if I don't do this
        start_button.clicked.connect(self.start_adding_nodes)
        self.layout.addWidget(start_button)

    def add_element(self, type, label, dynamic=True, script_path='', readme_path='', qc_label=None, is_manual=None):
        if qc_label:
            elt = type(label,qc_label=qc_label) #TODO not a good way...
        else:
            elt = type(label)
        self.elements.append(elt)
        self.layout.addWidget(elt)
        if type==NodeStatic: # POS_TYPE = 0
            str = 'File'
        elif type==FunctionArrow:
            str = 'Function'
        else:
            str = 'Unknown'
        str += ('::' + label) # POS_SUFFIX = 1
        if dynamic:
            str += '::SPACER' # TODO use this spot for something
            if qc_label: # POS_QC = 3
                str += ('::' + qc_label)
            else:
                str += ('::' + DEFAULT_NO_QC)
            if readme_path: # POS_README = 4
                str += ('::' + readme_path)
            else:
                str += ('::' + DEFAULT_NO_README)
            if script_path:  # POS_SCRIPT = 5
                str += ('::' + script_path)
            else:
                str += ('::' + DEFAULT_NO_SCRIPT)
            if is_manual: # POS_IS_MANUAL = 6
                str += '::MANUAL'
        self.strs.append(str)

    def start_adding_nodes(self):
        button = self.sender()
        button.deleteLater()
        info = self.show_input_dialog('Input first step')
        if info:
            self.add_element(NodeStatic, info[POS_INPUT],dynamic=False) #only need to add 1st node (inactive) in 1st step
            self.add_step(info)

    def show_input_dialog(self, str, prev_step=None):
        w = InputStepInfoDialog(prev_step)
        w.setWindowTitle(str)
        w.show()
        if w.exec():
            info = w.info
            w.close()
            return info

    def add_step(self, info):
        # TODO dummy check: cannot input same name twice
        self.prev_step=info[POS_OUTPUT]
        self.add_element(FunctionArrow, info[POS_FUNC],dynamic=False)
        self.add_element(NodeStatic, info[POS_OUTPUT], script_path=info[POS_SCRIPT], readme_path=info[POS_README],
                         qc_label=info[POS_QC], is_manual=info[POS_IS_MANUAL])

    def delete_step(self):
        self.elements.pop()
        self.strs.pop()
        count = self.layout.count()
        self.layout.itemAt(count-1).widget().deleteLater()
        if count > 1:
            self.layout.itemAt(count-2).widget().deleteLater()
        if count==1: #~perfection :/
            self.add_start_button()

    def save_dialog(self):
        qm = QMessageBox.StandardButton
        ans = QMessageBox.question(self, '', "Do you want to save the current schema?", qm.Yes | qm.No)
        if ans == qm.Yes:
            fn = QFileDialog.getSaveFileName(self, 'Save schema:', 'new_schema_' + date.today().strftime('%Y%m%d'),
                                             'Text Files (*.txt)')
            with open(fn[0], 'w+') as file:
                for str in self.strs:
                    file.write(str + '\n')

    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.MouseButton.LeftButton:
            if self.counter:  # detect double click
                self.counter = False
                info = self.show_input_dialog('Input next step', prev_step=self.prev_step)
                self.add_step(info)
            else:
                self.counter = True

    def keyReleaseEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key.Key_S:
            self.save_dialog()
            self.close()
        if QKeyEvent.key() == Qt.Key.Key_D:
            self.delete_step()











