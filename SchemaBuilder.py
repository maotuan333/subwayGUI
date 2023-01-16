from Config import *
from StaticAssets import NodeStatic, FunctionArrow
from InputStepInfoDialog import InputStepInfoDialog
from PyQt6.QtWidgets import (
    QWidget, QMessageBox, QHBoxLayout, QPushButton, QFileDialog, QGridLayout
)
from PyQt6.QtCore import Qt
from datetime import date
import json
from Toolbox import schema_reader

# A canvas for building schemas (rules of file trains) that will be used to find files
class SchemaBuilder(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize
        # steps: list of dicts, a record of steps information
        # used for info exchange within the gui
        self.steps=list()
        # toggle: toggle switch that detects double click
        self.toggle=False

        # Create layout
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        # Start page
        self.add_start_button()

    # Display start button
    def add_start_button(self):
        start_button = QPushButton('Add Node')
        # can't delete or save at first step if I don't do this (TODO why?)
        start_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        start_button.clicked.connect(self.add_first_step)
        self.layout.addWidget(start_button)

    def delete_start_button(self):
        # If start button is present then no other widget should be
        start_button = self.layout.itemAt(0).widget()
        self.layout.removeWidget(start_button)
        start_button.setParent(None)
        start_button.deleteLater()

    # This function adds the first node of a schema
    def add_first_step(self):
        # Remove start button
        self.delete_start_button()
        # Get inputs using dialog
        info = self.show_input_dialog('Input first step')
        if info:
            # Append current step to list of steps
            self.steps.append(info)
            # The first node is added separately
            self.layout.addWidget(NodeStatic(info['input']))
            # Add function used by the first step and its output
            self.add_step(info)

    # Wrapper that returns info from input dialog
    def show_input_dialog(self, msg):
        w = InputStepInfoDialog(self.get_prev())
        w.setWindowTitle(msg)
        w.show()
        if w.exec():
            info = w.info
            w.close()
            return info

    # Add a step to the schema.
    # A step does not include the input, only the function and output node.
    # The first node is added separately by start_adding_nodes.
    def add_step(self, info):
        # TODO dummy check: cannot input same name twice
        self.layout.addWidget(FunctionArrow(info['func']),alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(NodeStatic(info['output'],qc_meta=info.get('qc_meta'),qc_img=info.get('qc_img')),
                              alignment=Qt.AlignmentFlag.AlignHCenter)
        self.steps.append(info)

    # Delete the last step added
    def delete_step(self):
        # Remove record of the last step from list
        self.steps.pop()
        # Get indexes of items to be deleted
        for i in range(2):
            index_last_item=self.layout.count() - 1
            #TODO: delete function unit
            # remove last node
            last_item = self.layout.itemAt(index_last_item)
            self.layout.removeItem(last_item)
            last_item.widget().deleteLater()
            # If all nodes had been deleted
            if index_last_item == 0:
                # Restore start page and return
                self.add_start_button()
                return

    # Save new schema as json file
    def save_dialog(self):
        # Yes/no dialog pops up
        qm = QMessageBox.StandardButton
        msg = 'Do you want to save the current schema?'
        ans = QMessageBox.question(self, '', msg, qm.Yes | qm.No)
        # If user says yes:
        if ans == qm.Yes:
            # Default file name is new_schema_YYMMDD.json
            fn = QFileDialog.getSaveFileName(self, 'Save schema:', 'new_schema_' + date.today().strftime('%Y%m%d'),
                                             'JSON file (*.json)')
            # Dump schema info into json
            with open(fn[0], 'w+') as file:
                json.dump(self.steps, file, indent=1)
        # Close this tab
        self.deleteLater()
        self.close()

    # Return the output of last step, i.e. input of new step
    def get_prev(self):
        if self.steps:
            return self.steps[-1]['output']
        else:
            return None

    # Load schema from json file to edit
    def restore(self, filepath):
        self.delete_start_button()
        self.steps=schema_reader(filepath)
        if self.steps:
            # Add first node
            self.layout.addWidget(NodeStatic(self.steps[0]['input']))
            # Add subsequent steps
            for info in self.steps[]:
                self.add_step(info)

    # Double click to add new step
    def mouseReleaseEvent(self, QMouseEvent):
        # Detect left clicks
        if QMouseEvent.button() == Qt.MouseButton.LeftButton:
            # If this is the second click
            if self.toggle:
                self.toggle = False
                # Display input dialog
                info = self.show_input_dialog('Input next step')
                # Process info from input dialog
                self.add_step(info)
            # If this is the first click
            else:
                self.toggle = True # record first click

    # Press S for save schema, D for delete step
    def keyReleaseEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key.Key_S:
            self.save_dialog()
            self.close()
        if QKeyEvent.key() == Qt.Key.Key_D:
            self.delete_step()
