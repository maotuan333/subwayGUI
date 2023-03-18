from PyQt6.QtWidgets import (
    QWidget, QPushButton, QMessageBox
)
from PyQt6.QtCore import QUrl
import glob
from enum import Enum
import re


# Status of FileStatusButton
class Status(Enum):
    NOT_FOUND = 0
    FOUND = 1
    PARTIAL = 2
    FAILED = 3

    # 1. no file is found: button is clickable for action, such as generating those files;
    # 2. part of the files are found: behavior of the button needs to be specified;
    # 3. all files are found: button is unclickable, or cli for file viewing;
    # 4. error: the last action failed.

# An abstract container that has a button associated with the status of file(s)
class FileStatusButton(QWidget):
    # Status of the associated file(s)
    files_status = Status.NOT_FOUND
    # True if the button links to multiple files
    multiple = False

    def __init__(self, filepath,
                 img_not_found='', img_found='', img_failed='', img_partial='',
                 msg_failed=None, msg_partial=None):
        super().__init__()
        # Add button - a potential use of this button is to generate the indicated file.
        self.button = QPushButton()

        def reformat(path):
            """Reformat a pathlib path into CSS url."""
            if type(path)==list:
                return [QUrl.fromLocalFile(str(fp)).toLocalFile() for fp in path]
            else:
                return QUrl.fromLocalFile(str(path)).toLocalFile()

        self.img_not_found=reformat(img_not_found)
        self.img_found=reformat(img_found)
        self.img_failed=reformat(img_failed)
        self.img_partial=reformat(img_partial)

        self.msg_failed=msg_failed
        self.msg_partial=msg_partial

        # filepath can be a str or a list. If more than one file is specified, the button is in 'multiple' mode
        # and checks if all files exist. Otherwise, the button checks for a single file.
        self.filepath = reformat(filepath)
        if type(filepath) == list:
            if len(filepath) == 1:
                self.filepath = filepath[0] # Reduce list of length 1 to str
            else:
                self.multiple = True # Multiple files
        id_str=self.filepath[0] if self.multiple else self.filepath
        self.button_id = re.sub(r'[^a-zA-Z]', '', id_str)
        self.button.setObjectName(self.button_id)

        # Initialize file status
        self.refresh()

    def set_icon(self,url):
        """Change button appearance."""
        self.button.setStyleSheet("#"+self.button_id+" { "
                                  "width:28px;"
                                  "height:28px;"
                                  "border-radius:14px;"
                                  "background-image: url('" + url + "');"
                                  "}")

    # Update status when file is found
    def set_file_found(self):
        self.files_status = Status.FOUND
        self.set_icon(self.img_found)
        # Set button as unclickable
        self.button.setDisabled(True)
        # Hover to see full path(s)
        self.button.setToolTip(('\n'.join(self.filepath) if self.multiple else self.filepath))

    # Update status when file is missing
    def set_file_not_found(self):
        self.files_status = Status.NOT_FOUND
        self.set_icon(self.img_not_found)
        # Enable clicking
        self.button.setDisabled(False)
        # Erase hover message
        self.button.setToolTip(None)

    # Update status when only part of the files are found
    def set_file_partial(self, results):
        self.files_status = Status.PARTIAL
        self.set_icon(self.img_partial)
        # Hover to see full path(s) that were found
        found_files = [file for file, exists in zip(self.filepath, results) if exists]
        self.button.setToolTip('\n'.join(found_files))
        # Show warning box if needed
        if self.msg_partial:
            QMessageBox.critical(self, "Warning", self.msg_partial)

    # Update status to failed
    def set_failed(self):
        self.files_status = Status.FAILED
        self.set_icon(self.img_failed)
        # Show warning box if needed
        if self.msg_failed:
            QMessageBox.critical(self, "Warning", self.msg_failed)

    # Search for target file and update status
    def refresh(self, set_fail=False):
        # Did we successfully generate one or more files?
        if not self.multiple:
            # Search for file and update status
            if glob.glob(self.filepath):
                self.set_file_found()
                return
        else:
            # Check if all files exist
            results = [glob.glob(file) != [] for file in self.filepath]
            if all(results):
                self.set_file_found()
                return
            elif any(results):
                self.set_file_partial(results)
                return
        self.set_failed() if set_fail else self.set_file_not_found()
        # No files were generated. You can either leave the button in default or set its state
        # to failed by specifying 'set_fail'.

    def set_filepath(self,filepath):
        self.filepath=filepath
        self.refresh()