import os.path
from functools import partial

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QPushButton, QLabel, QDialog, QLineEdit, QGridLayout, QCheckBox, QFileDialog, QMessageBox
)
from PyQt6.QtTest import QTest
from w_DropOrSelectButton import DropOrSelectButton
from dotmap import DotMap
from static import data_plain

# A form that allows user to input the specifics of a step
class InputStepInfoDialog(QDialog):
    verbal = True
    script_path = None
    readme = None

    def __init__(self, prev_step=None):
        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)
        self.boxes = []
        self.data = DotMap(data_plain)
        #self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)

        self.function_is_manual_checkbox = QCheckBox()
        self.function_is_manual_checkbox.clicked.connect(self.message_for_manual_step)

        for i, w in enumerate(self.data.items()):
            w=w[1]
            row=w.id.widget
            if i == 1:
                layout.addWidget(self.function_is_manual_checkbox, 2, 0)
                layout.addWidget(QLabel("manual step"), 2, 1)
            layout.addWidget(QLabel(w.label_text), row, 0)
            qle = QLineEdit()
            qle.setPlaceholderText(w.placeholder)
            if w.flags.full_path_only:
                qle.setDisabled(True)
            self.boxes.append(qle)
            layout.addWidget(self.boxes[i], row, 1)
            but = DropOrSelectButton(title="select",
                                     file_dialog_function=w.file_dialog.function,
                                     file_dialog_msg=w.file_dialog.message,
                                     file_dialog_filter=w.file_filter.string,
                                     extensions=w.file_filter.extensions,
                                     )
            but.return_signal.connect(partial(self.select_file, w.name))
            but.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            layout.addWidget(but, row, 2)
            if i == 0 and prev_step:
                self.boxes[i].setEnabled(False)
                self.boxes[i].setText(prev_step)
                but.setEnabled(False)
            self.setWindowModality(Qt.WindowModality.WindowModal)
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

    def message_for_manual_step(self):
        if self.function_is_manual_checkbox.isChecked():
            self.boxes[self.data.func.id.box].setDisabled(False)
            if self.verbal:
                # https://stackoverflow.com/questions/49155926/how-to-customise-a-pyqt-message-box
                title = "Add Additional Info for Manual Step"
                msg = "You could add a readme/protocol file for this manual step." \
                      "It will pop up in subway runs to give users directions.\n\n" \
                        "To add a file, select file in the 'readme' input box."
                mb = QMessageBox()
                mb.setWindowTitle(title)
                mb.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
                mb.setText(msg)
                yes_button = QPushButton("Yes, select file")
                no_button = QPushButton("No")
                stop_showing_button = QPushButton("Stop showing this message")
                mb.addButton(yes_button, QMessageBox.ButtonRole.YesRole)
                mb.addButton(no_button, QMessageBox.ButtonRole.YesRole)
                mb.addButton(stop_showing_button, QMessageBox.ButtonRole.YesRole)
                mb.exec()
                if mb.clickedButton() == yes_button:
                    readme_add_button = self.layout().itemAtPosition(
                        self.data.readme.id.widget, 2).widget()
                    QTest.mouseClick(readme_add_button, Qt.MouseButton.LeftButton)
                if mb.clickedButton() == stop_showing_button:
                    self.verbal=False
        else:
            self.boxes[self.data.func.id.box].setText(None)
            self.boxes[self.data.func.id.box].setDisabled(True)

    def select_file(self, name, file):
        file=file[0]
        s = os.path.basename(file)
        full_path_only = self.data[name].flags.full_path_only
        i = self.data[name].id.box
        if full_path_only:
            self.data[name].results.filepath = file
        self.boxes[i].setText(s)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key.Key_Return:
            self.data.func.results.is_manual = self.function_is_manual_checkbox.isChecked()
            for i, key in enumerate(self.data.keys()):
                box_text = self.boxes[i].text()
                if box_text:
                    self.data[key].results.show_text = box_text
                    if self.data[key].results.filepath is None:
                        self.data[key].results.filepath = box_text
                elif self.data[key].flags.required:
                    QMessageBox.warning(self, "Required Field", "Please fill in all required (*) fields!")
                    return
            self.accept()