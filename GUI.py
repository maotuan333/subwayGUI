from config import *
import config
from PyQt6.QtWidgets import (
    QMenuBar, QSplitter, QMainWindow
)
from FileSidebar import FileSidebar
from GUIWorkspace import GUIWorkspace
from PyQt6.QtCore import Qt


# Most outer layer of the GUI for file tracking.
class SubwayGUI(QMainWindow):

    def __init__(self):
        super().__init__()

        # styling
        self.setWindowTitle('Welcome to SubwayGUI!')
        self.setMinimumSize(1290, 860)

        # menu
        menuBar = QMenuBar()
        self.setMenuBar(menuBar)

        # main window
        splitter = QSplitter()

        self.fileSidebar = FileSidebar(str(CUR_WORK_FOLDER))
        splitter.addWidget(self.fileSidebar)
        self.mainWorkspace = GUIWorkspace()
        splitter.addWidget(self.mainWorkspace)
        splitter.setSizes([(int)(splitter.size().width() * 0.3),
                           (int)(splitter.size().width() * 0.7)])

        # round up
        self.setCentralWidget(splitter)


'''
Some rules for sorting out file paths...

work_folder: 'C:/absolute_path/exp_folder' - maximum common filepath of all files in the subway system
subway_folder: '/collection_of_files/yymmdd_Exp_00x' - excluding work_folder, lowest common ancestor of all files in one subway line
start_file = 'C:/absolute_path/exp_folder/collection_of_files/yymmdd_Exp_00x_start_file.ext'
subway_folder = 'C:/absolute_path/exp_folder/collection_of_files'
subway_prefix: 'yymmdd_Exp_00x' - maximum common prefix of all files in one subway line. 
                                    used for display purposes (as title of the subway line)
prev_suffix: '_1st_step.ext1'
my_suffix: '_2nd_step.ext2'
my_fullpath: subway_prefix + my_suffix - the file should satisfy this rule
my_start_file: subway_prefix + prev_suffix
'''

