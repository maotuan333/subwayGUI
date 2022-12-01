from PyQt6.QtWidgets import (
    QTreeView,QAbstractItemView
)
from PyQt6.QtGui import QFileSystemModel

class FileSidebar(QTreeView):
    def __init__(self,path):
        super().__init__()
        # https://stackoverflow.com/questions/50283851/how-to-display-list-of-files-in-a-specified-directory
        self.resizeColumnToContents(0)
        self.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)
        self.fsm = QFileSystemModel()
        self.fsm.setRootPath(path)
        self.fsm.setReadOnly(False)

        #self.setSelectionMode(self.SingleSelection)
        self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)

        self.path = path
        self.setModel(self.fsm)
        self.setRootIndex(self.fsm.index(path))
        self.fsm.directoryLoaded.connect(self._fetchAndExpand)
        self.setColumnHidden(1,True) #hide 'size' column

    def _fetchAndExpand(self):
        # https://stackoverflow.com/questions/24920360/fully-expand-a-qtreeview-representing-a-qfilesystemmodel
        index = self.fsm.index(self.path)
        self.expand(index)

    #https://stackoverflow.com/questions/48121711/drag-and-drop-within-pyqt5-treeview