from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from components.music_components.search_music import SearchMusicPage


class MusicPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("search_music")
        self.tab_widget.setWindowFlags(Qt.FramelessWindowHint)
        self.search_page = SearchMusicPage()
        self.tab_widget.addTab(self.search_page, QIcon("static/icon/book_search.png"), "音乐搜索")
        main_layout.addWidget(self.tab_widget)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setTabShape(QTabWidget.Triangular)
        self.setLayout(main_layout)
