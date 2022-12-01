from Config import *
import sys
from Subway import Subway
from SchemaBuilder import SchemaBuilder
from PyQt6.QtWidgets import (
    QWidget,QPushButton,QHBoxLayout,QApplication,QMenuBar,QTreeView,QSplitter,QTabWidget,QVBoxLayout,QMainWindow
)

from PyQt6.QtCore import Qt,QDir
from FileSidebar import FileSidebar
from SubwayStartPage import SubwayStartPage

# https://www.pythonguis.com/tutorials/pyqt6-widgets/
# https://stackoverflow.com/questions/47910192/qgridlayout-different-column-width
# https://stackoverflow.com/questions/4286036/how-to-have-a-directory-dialog

'''
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

class MainWindow(QMainWindow):
    wrs=None
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Welcome to SubwayGUI!')
        self.setMinimumSize(1290,860)
        menuBar = QMenuBar()
        self.setMenuBar(menuBar)
        filesMenu = menuBar.addMenu("&Files")
        startsPageMenu = menuBar.addMenu("&Start Page")
        settingsMenu = menuBar.addMenu("&Settings")

        # https://stackoverflow.com/questions/5144830/how-to-create-folder-view-in-pyqt-inside-main-window
        layout = QHBoxLayout()
        splitterFileView = QSplitter(Qt.Orientation.Vertical)
        splitterActions = QSplitter(Qt.Orientation.Vertical)
        self.tabs=QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.delete_tab)
        splitterActions.addWidget(self.tabs)

        self.fileSidebar = FileSidebar(cur_work_folder)
        splitterFileView.addWidget(self.fileSidebar)
        #TODO should i give all qcs handle to splitter view?

        self.start_page()

        layout.addWidget(splitterFileView,30)
        layout.addWidget(splitterActions,70)
        self.setLayout(layout)

        w = QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)

    def start_page(self):
        self.start_tab = QWidget()
        start_tab_layout=QVBoxLayout()
        self.start_tab.setLayout(start_tab_layout)
        self.tabs.addTab(self.start_tab,"start page")

        run_subway_check_button = QPushButton('Run subway check')
        run_subway_check_button.clicked.connect(self.run_subway_start_page)
        start_tab_layout.addWidget(run_subway_check_button)

        new_schema_module = QPushButton('Start new schema')
        new_schema_module.clicked.connect(self.start_new_schema)
        start_tab_layout.addWidget(new_schema_module)

        edit_schema_module = QPushButton('Edit existing schema')
        edit_schema_module.clicked.connect(self.edit_existing_schema)
        start_tab_layout.addWidget(edit_schema_module)

    def run_subway_start_page(self):
        self.ssp = SubwayStartPage()
        self.ssp.return_signals.connect(self.run_subway)
        self.tabs.addTab(self.ssp, 'Subway Start Page')
        self.tabs.setCurrentWidget(self.ssp)

    def run_subway(self,work_folders,schema_path):
        self.ssp.close()
        self.wrs=Subway(work_folders,schema_path)
        self.wrs.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.tabs.addTab(self.wrs.scrollArea, work_folders[0])
        self.tabs.setCurrentWidget(self.wrs.scrollArea)

    def start_new_schema(self):
        self.wsns = SchemaBuilder()
        self.wsns.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.tabs.addTab(self.wsns,"Schema Builder")
        self.tabs.setCurrentWidget(self.wsns)

    def edit_existing_schema(self):
        pass

    def delete_tab(self, index):
        self.tabs.removeTab(index)

    def mousePressEvent(self, QMouseEvent):
        if self.wrs and QMouseEvent.button() == Qt.MouseButton.RightButton:
            self.wrs.drop_down(QMouseEvent)



#what's the right way to pass signals between?

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    e=app.exec()
    MATLAB_ENGINE.exit()
    sys.exit(e)