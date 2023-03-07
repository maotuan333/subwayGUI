import os.path
import re

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel, QVBoxLayout, QSizePolicy, QLineEdit,
    QDialog, QHBoxLayout, QListWidget, QPlainTextEdit, QListWidgetItem, QCheckBox, QGridLayout
)

from config import *
from model import yes_no,schema_writer
from static import FunctionArrow
from w_FileStatusButton import *

ALIGN_CENTER = Qt.AlignmentFlag.AlignCenter


# A widget representing the first file of a schema.
class DynamicStartFile(QWidget):
    def __init__(self, folder, prefix, suffix):
        super().__init__()
        self.label = prefix + suffix
        self.filepath = folder / self.label

        # create layout
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.node = FileStatusButton(filepath=self.filepath,
                                     img_not_found=ASSETS_FOLDER / "node_default.png",
                                     img_found=ASSETS_FOLDER / "node_success.png")
        self.layout.addWidget(self.node, 0, 1)
        self.format_node()

    # UI of node
    def format_node(self):
        layout = QVBoxLayout()
        layout.addWidget(self.node.button, alignment=ALIGN_CENTER)
        layout.addWidget(QLabel(self.label), alignment=ALIGN_CENTER)
        self.node.setLayout(layout)

        # Format button
        self.node.button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

    def file_exists(self):
        return self.node.files_status != Status.FOUND

# A widget representing all elements of a processing step:
# a function arrow and a button for the file to be generated.
class DynamicStepUnit(QWidget):
    def __init__(self, folder, prefix, data, schema):
        super().__init__()
        self.schema=schema
        self.data = data
        self.filename = prefix + self.data.output.show_text
        self.filepath = folder / (prefix + self.data.output.show_text)
        self.prev_filepath = folder / (prefix + self.data.input.show_text)

        # create layout
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        # draw function arrow
        self.layout.addWidget(FunctionArrow(self.data.func.show_text), 1, 0)
        # draw node
        self.add_node()

    # UI of node
    def add_node(self):
        # Create node with icon urls
        self.node = FileStatusButton(filepath=self.filepath,
                                     img_not_found=ASSETS_FOLDER / "node_default.png",
                                     img_found=ASSETS_FOLDER / "node_success.png",
                                     img_failed=ASSETS_FOLDER / "node_failed.png",
                                     msg_failed="Failed to generate file: " + str(self.filepath)
                                                + " by running " + self.data.func.filepath)
        # Add to lower right slot
        self.layout.addWidget(self.node, 1, 1)

        # Create layout around node
        layout = QVBoxLayout()
        layout.addWidget(self.node.button, alignment=ALIGN_CENTER)
        layout.addWidget(QLabel(self.filename), alignment=ALIGN_CENTER)
        self.node.setLayout(layout)

        # Format node UI
        self.node.button.setCheckable(True)  # TODO
        self.node.button.setFlat(True)  # TODO
        self.node.button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

    # Wrapper for generating output file on click
    def onclick(self):
        # If the step required to generate output file is manual
        if self.data.func.is_manual:
            msg = "Manual step required: Please complete '" + self.data.func.show_text + "' and try again."
            QMessageBox.about(self, 'Manual Step required', msg)
        else:
            # Generate output file and update status
            self.generate_file()
        # Display protocol if exists
        if self.data.readme.filepath:
            with open(self.data.readme.filepath, 'r') as f:
                msg = f.read()
            QMessageBox.about(self, 'Protocol', msg)

    def config_parameters(self,prev_parameters=None):
        retry = True
        while retry:
            w = FunctionConfigDialog(self.data.func.filepath, self.data.func.show_text)
            w.setWindowTitle("Configure function parameters")
            w.show()
            response = w.exec()
            if response == QDialog.DialogCode.Accepted:
                self.data.func.been_run = True
                self.data.func.parameters = w.get_results()
                schema_writer(self.data,schema_path=self.schema,position=self.data.pos)
                retry = False
            else:
                retry = yes_no(self, "Parameter configuration failed. Try again?"
                                     "If you select no, the script will be run with"
                                     "previous configuration (if possible) or default, which might not work.")

    def update_parameters(self):
        reconfigure = yes_no(self,"Failed to run script. \n"
                             "Try updating script configurations?")
        if reconfigure:
            self.config_parameters(self.data.func.parameters)
            QMessageBox("Success", "Config updated! Now you can rerun the step.")

    # Execute processing script to generate output file
    def generate_file(self):
        fp = self.data.func.filepath
        # Check if script exists
        if not os.path.isfile(fp):
            QMessageBox.critical(self, "Error", "'" + self.data.func.filepath + "' does not exist")
            return
        # If not ran before then set up parameters
        if not self.data.func.been_run:
            self.config_parameters()
        if fp[-2:] == '.m':
            # Matlab engine had been activated in config
            MATLAB_ENGINE.addpath(os.path.dirname(fp))
            try:  # Run script
                # sample_function(<filepath>,<arg1>,<arg2>);
                func = self.data.func.show_text[:-2]
                params=self.data.func.parameters
                command = func + '('
                for i,param in enumerate(params):
                    val = self.prev_filepath if param.use_prevpath else param.value
                    command += (', ' if i != 0 else '' + val)
                command+= "');"
                MATLAB_ENGINE.eval(command, nargout=0)
            except:
                self.update_parameters()
        elif fp[-3:] == '.py':
            try:
                func = self.data.func.show_text
                params = self.data.func.parameters
                command = "$ python " + func
                for i, param in enumerate(params):
                    val = self.prev_filepath if param.use_prevpath else param.value
                    command += (' ' + val)
                    os.system(command)
            except:
                self.update_parameters()
        elif fp[-2:]=='.r':
            pass #TODO
        else:
            QMessageBox.critical(self, "Error", "Script type not supported")
        # Check if file has been generated
        self.refresh(set_fail=True)

    # Check if output file had been generated
    def file_exists(self):
        return self.node.files_status == Status.FOUND

    # Update node files status
    def refresh(self, set_fail=False):
        self.node.refresh(set_fail=set_fail)


class FunctionConfigDialog(QDialog):
    def __init__(self, filepath, func_name):
        super().__init__()
        self.filepath = filepath
        self.func_name = func_name
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.items = []
        self.info = []
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint)

        self.params_list = QListWidget()
        params_box = QVBoxLayout()
        self.viewer = QPlainTextEdit()
        self.viewer.setReadOnly(True)
        self.viewer.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.viewer.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        viewer_box = QVBoxLayout()
        done_button = QPushButton("Done!")
        done_button.clicked.connect(self.save_params)
        viewer_box.addWidget(done_button)
        viewer_box.addWidget(self.viewer)

        self.layout.addLayout(params_box)
        self.layout.addLayout(viewer_box)

        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_param)
        add_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        del_button = QPushButton("Delete Selected")
        del_button.clicked.connect(self.del_param)
        del_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        command_button = QPushButton("Preview command")
        command_button.clicked.connect(self.show_command)
        command_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        command_button.setMinimumWidth(150)
        self.command_text = QLabel()
        layout_command = QHBoxLayout()
        layout_command.addWidget(command_button)
        layout_command.addWidget(self.command_text)
        self.input_line = QLineEdit()
        layout_input = QHBoxLayout()
        layout_input.addWidget(self.input_line)
        layout_input.addWidget(add_button)
        params_box.addLayout(layout_input)
        params_box.addWidget(del_button)
        params_box.addLayout(layout_command)
        params_box.addWidget(self.params_list)

        self.get_file_view()
        header = Header("Parameter", "Default value", "Use as input")
        self.add_param(header)
        suggest_params = self.get_suggestions()
        for param in suggest_params:
            self.add_param(ParameterItem(param))
        self.param_at(0).setChecked_prevpath(True)

    def param_at(self, i):
        return self.params_list.itemWidget(self.params_list.item(i + 1))

    def n_params(self):
        return self.params_list.count() - 1

    def add_param(self, widget=None):
        if not widget:
            widget = ParameterItem(self.input_line.text())
        item = QListWidgetItem()
        # otherwise the widgets won't show up because they don't fit
        item.setSizeHint(widget.sizeHint())
        self.params_list.addItem(item)
        self.params_list.setItemWidget(item, widget)
        self.input_line.clear()

    def del_param(self):
        items = self.params_list.selectedItems()
        if items:
            for item in items:
                self.params_list.takeItem(self.params_list.row(item))

    def get_file_view(self):
        self.text = ""
        with open(self.filepath, 'r') as f:
            for line in f:
                self.text += line
        self.viewer.setPlainText(self.text)

    def get_suggestions(self):
        params = []
        text = self.text.split('\n')
        if self.filepath[-2:] == ".m":
            for line in text:
                if line.strip().startswith("function"):
                    param_list = re.search(r'\((.+?)\)', line).group(1)
                    if param_list:
                        params = re.findall(r'\w+', param_list)
                break
        elif self.filepath[-3:] == ".py":
            for line in text:
                reg = re.search(r'(?P<var_name>\w+)\s*=\s*sys\.argv\[\d+]', line)
                param = reg.group('var_name')
                if param:
                    params.append(param)
        return params

    def get_results(self):
        return self.info

    def save_params(self):
        yes_save = yes_no(self, "Save parameters for {}?".format(self.func_name))
        if not yes_save:
            return
        self.info = []
        for i in range(self.n_params()):
            pack = self.param_at(i).package()
            if not pack:
                QMessageBox.warning("Warning", "Please fill in all parameters names and values.")
                return
            self.info.append(pack)
        self.accept()
        self.close()

    def show_command(self):
        command = ''
        if self.func_name[-2:] == '.m':
            # sample_function(<prev_filepath>, <arg1>, <arg2>)
            command = '$ matlab "' + self.func_name[:-2] + '('
            for i in range(self.n_params()):
                val = self.param_at(i).value.text()
                if val:
                    command += (', ' if i!=0 else '' + val)
            command+= ');exit"'
        elif self.func_name[-3:] == '.py':
            command = "$ python " + self.func_name
            for i in range(self.n_params()):
                val = self.param_at(i).value.text()
                command += (' ' + val)
        self.command_text.setText(command)

class Header(QWidget):
    def __init__(self, input, value, checkbox):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)
        self.layout.addWidget(QLabel(input))
        self.layout.addWidget(QLabel(value))
        self.layout.addWidget(QLabel(checkbox))


class ParameterItem(QWidget):
    def __init__(self, input='', value='', checked=False):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)
        self.input = QLineEdit(input)
        self.input.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        self.input.setMinimumWidth(10)
        self.value = QLineEdit(value)
        self.value.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        self.value.setMinimumWidth(10)
        # self.value.setDisabled(True)
        # self.checkbox = QCheckBox()
        # self.checkbox.clicked.connect(self.defaultval_state_changed)
        # self.checkbox.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        self.checkbox_prevpath = QCheckBox()
        self.checkbox_prevpath.clicked.connect(self.prevpath_state_changed)
        self.checkbox_prevpath.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        # self.setChecked_defaultval(checked)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.value)
        # self.layout.addWidget(self.checkbox)
        self.layout.addWidget(self.checkbox_prevpath)

    def package(self):
        if not self.input.text():
            return None
        if not self.value.text():
            QMessageBox.warning("Warning","Empty value is currently not supported")
            return None
        return {
            "name": self.input.text(),
            "value": self.value.text(),
            # None if self.checkbox.isChecked() else ..
            "use_prevpath": self.checkbox_prevpath.isChecked()
        }

    # def setChecked_defaultval(self, checked):
    #     self.checkbox.setChecked(checked)
    #     self.defaultval_state_changed()

    def setChecked_prevpath(self, checked):
        self.checkbox_prevpath.setChecked(checked)
        self.prevpath_state_changed()

    # def defaultval_state_changed(self):
    #     if self.checkbox.isChecked():
    #         self.value.setEnabled(True)
    #         self.checkbox_prevpath.setDisabled(True)
    #     else:
    #         self.value.setDisabled(True)
    #         self.checkbox_prevpath.setEnabled(True)

    def prevpath_state_changed(self):
        if self.checkbox_prevpath.isChecked():
            self.value.setDisabled(True)
            self.value.setText("<filepath>")
            # self.checkbox.setDisabled(True)
        else:
            self.value.setEnabled(True)
            self.value.clear()
            # self.checkbox.setEnabled(True)
