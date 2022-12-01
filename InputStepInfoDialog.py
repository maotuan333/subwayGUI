from Config import *
from PyQt6.QtWidgets import (
    QPushButton, QLabel, QDialog, QLineEdit, QGridLayout, QCheckBox, QFileDialog, QMessageBox, QInputDialog
)
from PyQt6.QtCore import Qt
import os.path
from functools import partial


class InputStepInfoDialog(QDialog):
    verbal=True

    def __init__(self, prev_step=None):
        super().__init__()
        self.script_path = ''
        self.boxes = []
        self.info = []
        self.tmp_protocol_created=False
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)
        self.function_is_manual_checkbox = QCheckBox()
        self.function_is_manual_checkbox.clicked.connect(self.message_for_manual_step)
        layout = QGridLayout()
        label_texts = ['*input: ', '*function/step: ', '*output: ', 'quality control: ','readme: ']
        self.required=[True,True,True,False,False]
        self.filters = [None,
                       "Python/MATLAB file (*.py *.m)",
                       None,
                       'Image files (*.png *.jpg *.jpeg *.tif *.tiff);;Text Files (*.txt)',
                       'Text Files (*.txt)']
        self.default_texts = [prev_step, 'next_func', 'next_filetype', '', '']
        if not prev_step: #this is the first step
            self.default_texts = ['filetype', 'func', 'filetype', '', '']
        for r, (lt, lit) in enumerate(zip(label_texts, self.default_texts)):
            if r>POS_FUNC:
                rr=r+1
            else:
                rr = r
            if r==POS_FUNC:
                layout.addWidget(self.function_is_manual_checkbox, 2, 0)
                layout.addWidget(QLabel('This is a manual step'), 2, 1)
            layout.addWidget(QLabel(lt), rr, 0)
            self.boxes.append(QLineEdit(lit))
            layout.addWidget(self.boxes[r], rr, 1)
            but = QPushButton('file')
            but.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            layout.addWidget(but, rr, 2)
            but.clicked.connect(partial(self.select_file, r))
            if r==0 and prev_step:
                self.boxes[r].setEnabled(False)
                but.setEnabled(False)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setLayout(layout)

    def message_for_manual_step(self):
        if self.function_is_manual_checkbox.isChecked():
            if self.verbal:
                # https://stackoverflow.com/questions/49155926/how-to-customise-a-pyqt-message-box
                title="Add Additional Info for Manual Step"
                msg="Do you want to add a protocol/readme file? It will show up in subway runs to tell users what to do.\n\n" \
                    "You could select a .txt file in 'readme', or type your protocol in a text box.\n" \
                    "To stop seeing this message, click\'Stop showing this message\'."
                mb=QMessageBox()
                mb.setWindowTitle(title)
                mb.setText(msg)
                y1b=QPushButton('Yes, select file')
                y2b=QPushButton('Yes, input in text box')
                nb=QPushButton('No')
                gb=QPushButton('Stop showing this message')
                qmr=QMessageBox.ButtonRole.YesRole
                mb.addButton(y1b,qmr)
                mb.addButton(y2b,qmr)
                mb.addButton(nb,qmr)
                mb.addButton(gb,qmr)
                mb.exec()
                if mb.clickedButton()==y1b:
                    self.select_file(POS_README)
                elif mb.clickedButton()==y2b:
                    import uuid
                    protocol=QInputDialog.getMultiLineText(self,'Protocol', 'Type in protocol for the manual step','')[0]
                    step_name=self.boxes[POS_FUNC].text()
                    protocol_file_name= PROGRAM_FILES_FOLDER + '/'
                    if step_name!=self.default_texts[POS_FUNC]: #if not default text
                        protocol_file_name=protocol_file_name+step_name+'-protocol-'+str(uuid.uuid4())+'.txt'
                    else:
                        protocol_file_name=protocol_file_name+'protocol-'+str(uuid.uuid4())+'.txt'
                        self.tmp_protocol_created=True
                        #TODO this could create junk files. to be addressed in schema editor
                    with open(protocol_file_name,'w+') as f:
                        f.write(protocol)
                    self.boxes[POS_README].setText(protocol_file_name)
                elif mb.clickedButton()==gb:
                    self.verbal=False
        else: #box unchecked
            if self.tmp_protocol_created: #delete created tmp file
                os.remove(self.boxes[POS_README].text())
            self.boxes[POS_README].setText(self.default_texts[POS_README])

    def select_file(self,i):
        fd = QFileDialog()
        file_path=fd.getOpenFileName(self, 'select file/script of the function for this step',filter=self.filters[i])[0]
        file_name = os.path.basename(file_path)
        self.boxes[i].setText(file_name)
        if i == POS_FUNC:
            self.script_path = file_path

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == Qt.Key.Key_Return:
            for i, (box,required) in enumerate(zip(self.boxes,self.required)):#TODO probably should make a class instead of zipping everything
                t=box.text()
                if required and not t:
                    QMessageBox.warning(self, 'Required Field',
                                        'Please fill in all required (*) fields!')
                    return
                self.info.append(t)
            self.info.append(self.script_path)
            self.info.append(self.function_is_manual_checkbox.isChecked())
            self.accept()
