from DropOrSelectButton import DropOrSelectButton
from Config import *
from PyQt6.QtWidgets import (
    QTabWidget,QVBoxLayout,QHBoxLayout,QLabel,QWidget,QPushButton
)
from PyQt6.QtCore import Qt

SQUARE_BUTTON_HEIGHT = 100


class TabbedWorkspace(QTabWidget):
    welcome_text=None
    tab_title=None
    start_page=None
    start_page_button_box=None
    start_page_index=None
    auto_close_start_page=True

    def __init__(self):
        super().__init__()
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.delete_tab)
        #set style sheet...

    def delete_tab(self, index):
        self.removeTab(index)
        if self.count()==0:
            self.add_start_page(self.welcome_text,self.tab_title)

    def close_start_page(self):
        if self.start_page_index:
            self.removeTab(self.start_page_index)
        self.start_page_index=None

    def add_start_page(self,welcome_text, tab_title):
        self.welcome_text=welcome_text
        self.tab_title=tab_title
        layout = QVBoxLayout()
        layout.addWidget(QLabel(welcome_text))
        self.start_page_button_box = QHBoxLayout()
        layout.addLayout(self.start_page_button_box)
        self.start_page = QWidget()
        self.start_page.setLayout(layout)
        self.start_page_index=self.addTab(self.start_page, tab_title)
        self.setCurrentWidget(self.start_page)

    def add_start_button(self,button_name,behavior,drop_or_select=False,**kwargs):
        button=DropOrSelectButton(button_name,**kwargs) if drop_or_select else QPushButton(button_name)
        button.return_signal.connect(behavior) if drop_or_select else button.clicked.connect(behavior)
        button.setMinimumHeight(SQUARE_BUTTON_HEIGHT)
        self.start_page_button_box.addWidget(button)

    def add_tab(self,tab,tab_title):
        if self.count()==1 and self.auto_close_start_page:
            self.close_start_page()
        tab.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        index=self.addTab(tab,tab_title)
        self.setCurrentIndex(index)
        return index

#TODO make this class cloasable