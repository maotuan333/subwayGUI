
# Collection of functions shared by many classes

from PyQt6.QtWidgets import (
    QWidget, QMessageBox
)
import json


def schema_reader(schema_path):
    # Check if schema file exists
    try:
        # Read in by line
        with open(schema_path[0], 'r') as file:
            schema = json.load(file)
            # Basic format check
            for info in schema:
                # If we're missing input, output or func in the step, then the schema is not valid.
                if not (info.get('func') and info.get('input') and info.get('output')):
                    # Stop reading and throw error.
                    QMessageBox.warning(None, 'Error in Schema','One or more steps is not valid in '+str(schema_path)+\
                                        '.\n(Missing input, function, or output.)')
    except:
        QMessageBox.warning(None, 'Warning', 'Read in of schema file failed:' + str(schema_path))

    return schema