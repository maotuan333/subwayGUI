from PyQt6.QtWidgets import (
    QFileDialog, QPushButton,QLabel
)
from PyQt6.QtCore import Qt, pyqtSignal
import os.path


class DropOrSelectButton(QPushButton):
    files = None
    label=None
    extensions = None
    return_signal=pyqtSignal(list)

    def __init__(self, title, file_dialog_function, file_dialog_msg, file_dialog_filter=None, extensions=None,
                 is_dir=False, is_single_file=True, embedded_text=False, placeholder=''):
        super().__init__()
        self.title=title
        self.initial_text = placeholder
        self.file_dialog_function=file_dialog_function
        self.file_dialog_msg=file_dialog_msg
        self.filter=file_dialog_filter
        self.extensions=extensions
        self.embedded_text=embedded_text
        self.is_dir=is_dir
        self.is_single_file=is_single_file
        self.setFlat(True)
        self.setAutoFillBackground(True)
        self.setAcceptDrops(True)
        if embedded_text:
            self.add_label()
        else:
            self.setText(title)
        self.clicked.connect(self.files_selector)

    def files_selector(self):
        if self.is_dir:
            file = self.file_dialog_function(self,self.file_dialog_msg).replace('\\', '/')
        else:
            file = self.file_dialog_function(self,self.file_dialog_msg, filter=self.filter)[0].replace('\\', '/')
        if file:
            self.reset_label()
            if type(file)==str:
                file=[file] # make sure file is always a list, even if it's a single file
            self.set_label(file)
            self.return_signal.emit(self.files)

    def add_label(self):
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.label.setWordWrap(True)
        self.reset_label()

    def set_label(self, info):
        self.files = info
        if self.label:
            text = self.title + '\n\n' + '\n'.join(self.files)
            self.label.setText(text)
            self.label.adjustSize()
            self.resize(self.label.width(), self.label.height())

    def reset_label(self):
        self.files = None
        text=self.title+'\n\n'+self.initial_text
        if self.label:
            self.label.setText(text)
            self.label.adjustSize()
            self.resize(self.label.width(), self.label.height())

    # https://www.youtube.com/watch?v=KVEIW2htw0A
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            # check number of urls
            urls=[event.mimeData().urls()[0]] if self.is_single_file else event.mimeData().urls()

            files = []
            # check if input url(s) has required file/folder extension. Only valid urls are added to files.
            for url in urls:
                s = str(url.toLocalFile())
                if self.is_dir and not os.path.isdir(s):
                    continue
                if os.path.isdir(s) and not self.is_dir:
                    continue
                if not self.is_dir and self.extensions \
                        and '.'+s.split('.')[-1] not in self.extensions:
                    continue
                files.append(s)
            # accept and update if input contains valid info
            if len(files)>0:
                event.accept()
                event.setDropAction(Qt.DropAction.CopyAction)
                if self.embedded_text:
                    self.set_label(files)
                self.files = files
                self.return_signal.emit(self.files)

    def return_info(self):
        return self.files
