from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout

from components.novel_components.books_component import BooksPage
from components.novel_components.read_component import ReadComponent
from components.novel_components.search_component import SearchPage
from window_func.config_reader import read_info
from window_func.db_handler import BookSqlHandler


class NovelPage(QWidget):

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_config()

    def setup_config(self):
        self.book_id = read_info('read', 'book_id')
        if self.book_id:
            # 根据bookid获取内容后创建阅读页面
            book_list = self.book_id.split(",")[0:-1]
            temp_db = BookSqlHandler("get_book_info")
            for book_id in book_list:
                book_dict = temp_db.query_book_info(book_id)
                if book_dict["id_list"]:
                    temp_read_book_page = ReadComponent(book_dict)
                    self.tab_widget.addTab(temp_read_book_page, QIcon("static/icon/book_read.png"),
                                           book_dict["book_name"])

    def setup_ui(self):
        main_layout = QVBoxLayout()
        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("search")
        self.tab_widget.setWindowFlags(Qt.FramelessWindowHint)
        self.search_page = SearchPage()
        self.book_page = BooksPage()
        self.book_page.switch_tab_signal_trigger.connect(self.switch_tab)
        self.tab_widget.addTab(self.search_page, QIcon("static/icon/book_search.png"), "小说搜索")
        self.tab_widget.addTab(self.book_page, QIcon("static/icon/bookshelf.png"), "我的书架")
        main_layout.addWidget(self.tab_widget)
        self.setLayout(main_layout)

    def switch_tab(self, book_list):
        print("book_dict", book_list)
        temp_db = BookSqlHandler("get_book_info")
        book_dict = temp_db.query_book_info(book_list[0])
        if book_dict:
            temp_read_book_page = ReadComponent(book_dict)
            self.tab_widget.addTab(temp_read_book_page, QIcon("static/icon/book_read.png"), book_dict["book_name"])
            self.tab_widget.setCurrentWidget(temp_read_book_page)
