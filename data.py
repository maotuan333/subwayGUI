from PyQt6.QtWidgets import QFileDialog

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
            "filepath": None
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
            "is_manual": False
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
            "filepath": None
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
        "placeholder": "[(.txt) readme filepath]",
        "id": {
            "widget": 4,
            "box": 3
        },
        "results": {
            "show_text": None,
            "filepath": None
        }
    }
}
