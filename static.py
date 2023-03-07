from config import *
from PyQt6.QtWidgets import (
    QVBoxLayout, QWidget, QLabel,QFileDialog
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

ALIGNMENT=Qt.AlignmentFlag.AlignCenter

data_schema = {
    "input": {
            "show_text": None,
            "filepath": None
        },
    "func": {
        "show_text": None,
        "filepath": None,
        "is_manual": False,
        "been_run": False
    },
    "output": {
        "show_text": None,
        "filepath": None
    },
    "readme": {
        "show_text": None,
        "filepath": None
    }
}

data_plain = {
    "input": {
        "name": "input",
        "label_text": "*input: ",
        "file_dialog": {
            "function": QFileDialog.getOpenFileName,
            "message": "Select input file for this step"
        },
        "file_filter": {
            "string": None,
            "extensions": None
        },
        "flags": {
            "required": True,
            "full_path_only": False,
        },
        "placeholder": "[unique extension or suffix]",
        "id": {
            "widget": 0,
            "box": 0
        },
        "results": {
            "show_text": None,
            "filepath": None,
        }
    },
    "func": {
        "name": "func",
        "label_text": "*function/step: ",
        "file_dialog": {
            "function": QFileDialog.getOpenFileName,
            "message": "Select function/script for this step"
        },
        "file_filter": {
            "string": "Python/MATLAB file (*.py *.m)",
            "extensions": [".py", ".m"]
        },
        "flags": {
            "required": True,
            "full_path_only": True,
        },
        "placeholder": "[(.py, .m) script path]",
        "id": {
            "widget": 1,
            "box": 1
        },
        "results": {
            "show_text": None,
            "filepath": None,
            "is_manual": False,
            "been_run": False
        }
    },
    "output": {
        "name": "output",
        "label_text": "*output: ",
        "file_dialog": {
            "function": QFileDialog.getOpenFileName,
            "message": "Select output of the step"
        },
        "file_filter": {
            "string": None,
            "extensions": None
        },
        "flags": {
            "required": True,
            "full_path_only": False,
        },
        "placeholder": "[unique extension or suffix]",
        "id": {
            "widget": 3,
            "box": 2
        },
        "results": {
            "show_text": None,
            "filepath": None,
        }
    },
    "readme": {
        "name": "readme",
        "label_text": "readme: ",
        "file_dialog": {
            "function": QFileDialog.getOpenFileName,
            "message": "Select text file as a readme/protocol of the step"
        },
        "file_filter": {
            "string": "Text Files (*.txt)",
            "extensions": [".txt"]
        },
        "flags": {
            "required": False,
            "full_path_only": True,
        },
        "placeholder": "[readme filepath]",
        "id": {
            "widget": 4,
            "box": 3
        },
        "results": {
            "show_text": None,
            "filepath": None,
        }
    }
}


# Static file node, contains a node icon and a label beneath it
class NodeStatic(QWidget):
    def __init__(self, label):
        super().__init__()
        # Create layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(ALIGNMENT)

        # Add icon and label for node
        n=QLabel()
        n.setPixmap(QPixmap(str(ASSETS_FOLDER/ "node_default.png")))
        layout.addWidget(n, alignment=ALIGNMENT)
        l = QLabel(label)
        layout.addWidget(l,alignment=ALIGNMENT)


# Static step arrow, contains an arrow and name of the function on top
class FunctionArrow(QWidget):
    def __init__(self, label):
        super().__init__()
        # Create layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(ALIGNMENT)

        # Add icon and label of function
        l = QLabel(label)
        layout.addWidget(l, alignment=ALIGNMENT)
        a = QLabel()
        a.setPixmap(QPixmap(str(ASSETS_FOLDER/"arrow.png")))
        layout.addWidget(a)


