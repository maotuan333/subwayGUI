import json

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMenuBar, QMainWindow
)
from PyQt6.QtWidgets import (
    QSplitter, QFileDialog
)

from c_FileSidebar import FileSidebar
from p_SchemaBuilder import SchemaBuilder
from p_Subway_Container import Subway
from p_Subway_StartPage import SubwayStartPage
from w_TabbedWorkspace import TabbedWorkspace
from config import *


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


class GUIWorkspace(QSplitter):
    subway = None

    def __init__(self):
        super().__init__()
        self.setOrientation(Qt.Orientation.Vertical)

        # upper portion
        self.up = TabbedWorkspace()
        self.up.add_start_page('Subway', 'Subway Start Page')
        self.up.add_start_button('Run new subway', self.run_subway_start_page)
        self.up.add_start_button('Run the same thing I did last time...', self.run_subway_prev_setup)
        self.addWidget(self.up)

        # lower portion
        self.down = TabbedWorkspace()
        self.down.add_start_page('Schema', 'Schema Start Page')
        self.down.add_start_button('Start new schema', self.start_new_schema)
        self.down.add_start_button('Edit existing schema', self.edit_existing_schema,
                                   drop_or_select=True,
                                   file_dialog_function=QFileDialog.getOpenFileName,
                                   file_dialog_msg="Select schema file to edit",
                                   file_dialog_filter="Schema Files (*.json)")
        self.addWidget(self.down)

    def run_subway_start_page(self):
        self.start_page = SubwayStartPage()
        self.start_page.return_signals.connect(self.run_subway)
        self.up.add_tab(self.start_page, 'Subway Start Page')

    def run_subway_prev_setup(self):
        try:
            with open(RUN_HISTORY, 'r') as file:
                last_run = json.load(file)
            self.run_subway(last_run)
        except Exception as e:
            logger.info(str(e))

    def run_subway(self, info):
        self.subway = Subway(info)
        # self.subway.(scrollArea.?)setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.up.add_tab(self.subway.scrollArea, info['folders'][0])

    def start_new_schema(self):
        self.down.add_tab(SchemaBuilder(), "Schema Builder")

    def edit_existing_schema(self, schema):
        if type(schema) is list:
            schema = schema[0]
        schema_editor = SchemaBuilder()
        schema_editor.restore(schema)
        self.down.add_tab(schema_editor, "Schema Editor")

    def mousePressEvent(self, QMouseEvent):
        if self.subway and QMouseEvent.button() == Qt.MouseButton.RightButton:
            self.subway.drop_down(QMouseEvent)


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
