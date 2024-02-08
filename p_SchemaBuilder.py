from dotmap import DotMap
from static import NodeStatic, FunctionArrow
from c_InputStepInfoDialog import InputStepInfoDialog
from PyQt6.QtWidgets import (
    QWidget, QMessageBox, QHBoxLayout, QPushButton, QFileDialog, QDialog
)
from PyQt6.QtCore import Qt
import json
from util import schema_reader,schema_writer,update_json,yes_no
from static import data_schema

# A canvas for building schemas (rules of file trains) that will be used to find files
class SchemaBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.steps=[]
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        # Start page
        self.add_start_button()

    def add_start_button(self):
        start_button = QPushButton('Add Step')
        # can't delete or save at first step if I don't do this (why?)
        start_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        start_button.clicked.connect(self.add_first_step)
        self.layout.addWidget(start_button)

    def delete_start_button(self):
        # If start button is present then no other widget should be
        start_button = self.layout.itemAt(0).widget()
        self.layout.removeWidget(start_button)
        start_button.deleteLater()

    # Add the first node of a schema
    def add_first_step(self):
        # Remove start button
        self.delete_start_button()
        # Get inputs using dialog
        info = self.show_input_dialog('Input first step')
        if info:
            # The first node is added separately
            self.layout.addWidget(NodeStatic(info.input.show_text))
            # Add function used by the first step and its output
            self.add_step(info)
        else:
            self.add_start_button()

    # Wrapper that returns info from input dialog
    def show_input_dialog(self, msg):
        w = InputStepInfoDialog(self.get_prev())
        w.setWindowTitle(msg)
        w.show()
        response = w.exec()
        if response== QDialog.DialogCode.Accepted:
            results = DotMap()
            for row in w.data.items():
                key,value=row
                # get all rows that has schema info
                if "results" in value:
                    results[key] = value.results
            w.close()
            return results
        else:
            return None

    # Add a step
    # to the schema.
    # A step does not include the input, only the function and output node.
    # The first node is added separately in add_first_step.
    def add_step(self, info):
        # TODO dummy check: cannot input same name twice
        self.layout.addWidget(FunctionArrow(info.func.show_text),alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(NodeStatic(info.output.show_text),alignment=Qt.AlignmentFlag.AlignHCenter)
        self.steps.append(info)

    # Delete the last step added
    def delete_step(self):
        # Remove record of the last step from list
        self.steps.pop()
        # If this is the first step, delete start node as well
        n_widgets = 2 if self.steps else 3
        for i in range(n_widgets):
            index_last_item=self.layout.count() - 1
            last_item = self.layout.itemAt(index_last_item)
            self.layout.removeItem(last_item)
            last_item.widget().deleteLater()
            # If all nodes had been deleted
        if not self.steps:
            self.add_start_button()

    # Save new schema as json file
    def save_dialog(self):
        yes_save = yes_no(self, 'Do you want to save the current schema?')
        if yes_save:
            self.steps = [update_json(step, data_schema) for step in self.steps]
            schema_writer(data=self.steps)
        # Close this tab
        self.deleteLater()
        self.close()

    # Return the output of last step, i.e. input of new step
    def get_prev(self):
        return self.steps[-1].output.show_text if self.steps else None

    # Load schema from json file to edit
    def restore(self, filepath):
        self.delete_start_button()
        schema=schema_reader(filepath)
        if schema:
            self.layout.addWidget(NodeStatic(schema[0].input.show_text))
            for step in schema:
                self.add_step(step)

    # Double click adds new step
    def mouseDoubleClickEvent(self, QMouseEvent):
        info = self.show_input_dialog('Input next step')
        self.add_step(info)

    # Press S to save schema, D to delete step
    def keyReleaseEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key.Key_S:
            self.save_dialog()
            self.close()
        if QKeyEvent.key() == Qt.Key.Key_D:
            self.delete_step()
