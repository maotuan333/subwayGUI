from Config import *
from PyQt6.QtWidgets import (
    QPushButton, QLabel, QDialog, QLineEdit, QGridLayout, QCheckBox, QFileDialog, QMessageBox, QInputDialog
)
from PyQt6.QtCore import Qt
import os.path
from DropOrSelectButton import DropOrSelectButton
from functools import partial


# A form that allows user to input the specifics of a step
class InputStepInfoDialog(QDialog):
    # Set to true to enable hints
    verbal = True

    #
    script_path=None
    readme=None

    def __init__(self, prev_step=None):
        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)
        self.boxes = []
        self.tmp_protocol_created = False
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)
        self.function_is_manual_checkbox = QCheckBox()
        self.function_is_manual_checkbox.clicked.connect(self.message_for_manual_step)
        label_texts = ['*input: ', '*function/step: ', '*output: ', 'quality control: ', 'readme: ']
        self.file_dialog_functions = [QFileDialog.getOpenFileName,
                                      QFileDialog.getOpenFileName,
                                      QFileDialog.getOpenFileName,
                                      QFileDialog.getOpenFileNames,
                                      QFileDialog.getOpenFileName]
        self.file_dialog_msgs = ['Select input file for this step',
                                 'Select function/script for this step',
                                 'Select output of the step',
                                 'Select quality control file (maximum one image file and one text file allowed)',
                                 'Select read me file for this step']
        self.required = [True, True, True, False, False]
        self.filters = [None,
                        "Python/MATLAB file (*.py *.m)",
                        None,
                        'Image or Text files (*.txt *.png *.jpg *.jpeg *.tif *.tiff)',
                        'Text Files (*.txt)']
        self.default_texts = [prev_step, 'next_func', 'next_filetype', '', '']
        if not prev_step:  # this is the first step
            self.default_texts = ['filetype', 'func', 'filetype', '', '']
        for r, (lt, lit, func, msg, filter) in enumerate(
                zip(label_texts, self.default_texts, self.file_dialog_functions, self.file_dialog_msgs, self.filters)):
            if r > POS_FUNC:
                rr = r + 1
            else:
                rr = r
            if r == POS_FUNC:
                layout.addWidget(self.function_is_manual_checkbox, 2, 0)
                layout.addWidget(QLabel('This is a manual step'), 2, 1)
            layout.addWidget(QLabel(lt), rr, 0)
            self.boxes.append(QLineEdit(lit))
            layout.addWidget(self.boxes[r], rr, 1)
            but = DropOrSelectButton(title='file',
                                     file_dialog_function=func,
                                     file_dialog_msg=msg,
                                     file_dialog_filter=filter)
            but.return_signal.connect(partial(self.select_file, r))
            but.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            layout.addWidget(but, rr, 2)
            # TODO instead of connect function, now receiving pyqtSignal from drop/select button
            if r == 0 and prev_step:
                self.boxes[r].setEnabled(False)
                but.setEnabled(False)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)


    # TODO need to oraganize this function..
    def message_for_manual_step(self):
        if self.function_is_manual_checkbox.isChecked():
            if self.verbal:
                # https://stackoverflow.com/questions/49155926/how-to-customise-a-pyqt-message-box
                title = "Add Additional Info for Manual Step"
                msg = "Do you want to add a protocol/readme file? " \
                      "It will show up in subway runs to tell users what to do.\n\n" \
                      "You could select a .txt file in 'readme', or type your protocol in a text box.\n" \
                      "To stop seeing this message, click\'Stop showing this message\'."
                mb = QMessageBox()
                mb.setWindowTitle(title)
                mb.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
                mb.setText(msg)
                y1b = QPushButton('Yes, select file')
                y2b = QPushButton('Yes, input in text box')
                nb = QPushButton('No')
                gb = QPushButton('Stop showing this message')
                qmr = QMessageBox.ButtonRole.YesRole
                mb.addButton(y1b, qmr)
                mb.addButton(y2b, qmr)
                mb.addButton(nb, qmr)
                mb.addButton(gb, qmr)
                mb.exec()
                if mb.clickedButton() == y1b:
                    self.select_file(POS_README)
                elif mb.clickedButton() == y2b:
                    import uuid
                    protocol = \
                        QInputDialog.getMultiLineText(self, 'Protocol', 'Type in protocol for the manual step', '')[0]
                    step_name = self.boxes[POS_FUNC].text()
                    protocol_file_name = PROGRAM_FILES_FOLDER + '/'
                    if step_name != self.default_texts[POS_FUNC]:  # if not default text
                        protocol_file_name = protocol_file_name + step_name + ' readme-' + str(uuid.uuid4()) + '.txt'
                    else:
                        protocol_file_name = protocol_file_name+ 'manual step readme-' + str(uuid.uuid4()) + '.txt'
                        self.tmp_protocol_created = True
                        # TODO this could create junk files. to be addressed in schema editor
                    with open(protocol_file_name, 'w+') as f:
                        f.write(protocol)
                    self.select_file(POS_README,protocol_file_name)
                elif mb.clickedButton() == gb:
                    self.verbal = False
        else:  # box unchecked
            if self.tmp_protocol_created:  # delete created tmp file
                os.remove(self.boxes[POS_README].text())
            self.boxes[POS_README].setText(self.default_texts[POS_README])

    def select_file(self, i, files):
        if type(files)==str:
            files=[files]
        s = os.path.basename(files[0])
        if i == POS_FUNC:
            self.script_path = files[0]
        elif i == POS_README:
            self.readme = files[0]
            s = s.split('-')[0]
        if len(files) == 2:  # only for QC. we might have two files
            s = s + ' ' + os.path.basename(files[1])
        self.boxes[i].setText(s)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key.Key_Return:
            self.accept()
            for i, (box, required) in enumerate(zip(self.boxes, self.required)):
                if required and not box.text():
                    QMessageBox.warning(self, 'Required Field',
                                        'Please fill in all required (*) fields!')
            info = dict()
            info['input'] = self.boxes[POS_INPUT].text()
            info['func'] = self.boxes[POS_FUNC].text()
            info['output'] = self.boxes[POS_OUTPUT].text()
            info['readme'] = self.readme
            info['script_path'] = self.script_path
            if self.function_is_manual_checkbox.isChecked():
                info['is_manual'] = 'MANUAL'
            qc_text = self.boxes[POS_QC].text().split(' ')
            for qc in qc_text:
                if qc.split('.')[-1] == 'txt':
                    info['qc_meta'] = qc
                else:
                    info['qc_img'] = qc
            self.info = info
