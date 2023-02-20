import json

from config import *
from PyQt6.QtWidgets import (
    QSplitter,QFileDialog
)
from Subway import Subway
from SchemaBuilder import SchemaBuilder
from SubwayStartPage import SubwayStartPage
from TabbedWorkspace import TabbedWorkspace
from PyQt6.QtCore import Qt


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
                                file_dialog_function = QFileDialog.getOpenFileName,
                                file_dialog_msg = "Select schema file to edit",
                                file_dialog_filter= "Schema Files (*.json)")
        self.addWidget(self.down)

    def run_subway_start_page(self):
        self.start_page = SubwayStartPage()
        self.start_page.return_signals.connect(self.run_subway)
        self.up.add_tab(self.start_page, 'Subway Start Page')

    def run_subway_prev_setup(self):
        with open(RUN_HISTORY, 'r') as file:
            last_run=json.load(file)
        self.run_subway(last_run)

    def run_subway(self, info):
        self.subway = Subway(info)
        # self.subway.(scrollArea.?)setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.up.add_tab(self.subway.scrollArea, info['folders'][0])

    def start_new_schema(self):
        self.down.add_tab(SchemaBuilder(), "Schema Builder")

    def edit_existing_schema(self,schema):
        if type(schema) is list:
            schema=schema[0]
        schema_editor=SchemaBuilder()
        schema_editor.restore(schema)
        self.down.add_tab(schema_editor, "Schema Editor")

    def mousePressEvent(self, QMouseEvent):
        if self.subway and QMouseEvent.button() == Qt.MouseButton.RightButton:
            self.subway.drop_down(QMouseEvent)
