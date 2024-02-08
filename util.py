# Collection of functions shared by many classes

import json
from datetime import date
import re
from PyQt6.QtWidgets import QMessageBox, QFileDialog
from dotmap import DotMap
import os


def schema_reader(schema_path):
    # Check if schema file exists
    try:
        # Read in by line
        with open(schema_path, 'r') as file:
            schema = json.load(file)
            # Basic format check
            for info in schema:
                # If we're missing input, output or func in the step, then the schema is not valid.
                if not ('input' in info and 'func' in info and 'output' in info):
                    # Stop reading and throw error.
                    QMessageBox.warning(None, 'Error in Schema',
                                        'One or more steps is not valid in ' + str(schema_path) + \
                                        '.\n(Missing input, function, or output.)')
    except:
        QMessageBox.warning(None, 'Warning', 'Read in of schema file failed:' + str(schema_path))
        return None
    schema = [DotMap(x) for x in schema]
    return schema


def schema_writer(data, schema_path=None, position=None):
    if not schema_path:
        # Default file name = new_schema_YYMMDD.json
        default_name = 'new_schema_' + date.today().strftime('%Y%m%d')
        schema_path = QFileDialog.getSaveFileName(None,'Save schema:', default_name,
                                                  'JSON file (*.json)')[0]
    else:
        if position is not None:
            schema = schema_reader(schema_path)
            schema[position] = update_json(data, schema[position])
            data=schema
    with open(schema_path, 'w') as file:
        json.dump(data, file, indent=1)


def update_json(destination, source):
    for key, value in source.items():
        if isinstance(value, dict):
            update_json(destination[key], source[key])
        if key not in destination:
            destination.update({key: value})
    return destination


def yes_no(parent, msg):
    qm = QMessageBox.StandardButton
    response = QMessageBox.question(parent, '', msg, qm.Yes | qm.No)
    return response == qm.Yes


def popup(dialog, title, *args):
    w = dialog(*args)
    w.setWindowTitle(title)
    w.show()
    response = w.exec()
    return [w, response]

# Address some filetypes not following naming convention
# by finding the file of maximum similarity
def filename_match(root_dir,identifier,parts):
    max_match=-1
    best_file=None
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if identifier in filename:
                n_match=len([s in filename for s in parts])
                if n_match>max_match:
                    max_match=n_match
                    best_file=os.path.join(dirpath,filename)
    return best_file

# Split up file parts by common separators
def filename_extract(filename):
    separators = " _-+,"
    pattern='|'.join(re.escape(s) for s in separators)
    fileparts=re.split(pattern,filename)
    return fileparts

def autowrap(string,line_len=20):
    return '\n'.join(string[i:i+line_len] for i in range(0,len(string),line_len))