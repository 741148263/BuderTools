from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout

from components.novel_components.books_component import BooksPage
from components.novel_components.read_component import ReadComponent
from components.novel_components.search_component import SearchPage
from window_func.config_reader import read_info
from window_func.db_handler import BookSqlHandler
from window_func.config_reader import delete_book_info


class NovelPage(QWidget):

    def __init__(self):
        super().__init__()
        self.tab_list = []
        self.tab_id_list = []
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
        self.book_page.switch_tab_pyqtSignal_trigger.connect(self.switch_tab)
        self.tab_widget.addTab(self.search_page, QIcon("static/icon/book_search.png"), "小说搜索")
        self.tab_widget.addTab(self.book_page, QIcon("static/icon/bookshelf.png"), "我的书架")
        main_layout.addWidget(self.tab_widget)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setTabShape(QTabWidget.Triangular)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.setLayout(main_layout)

    def switch_tab(self, book_list):
        temp_db = BookSqlHandler("get_book_info")
        book_dict = temp_db.query_book_info(book_list[0])
        # 如果当前需要打开的小说页面已经打开，则不需要重新进行打开
        # 获取当前已经打开的tab页面的信息
        tab_id_dict = self.update_tab_info()
        if book_dict and book_dict["id"] not in tab_id_dict.values():
            temp_read_book_page = ReadComponent(book_dict)
            self.tab_widget.addTab(temp_read_book_page, QIcon("static/icon/book_read.png"), book_dict["book_name"])
            self.tab_id_list.append(book_dict["id"])
            self.tab_list.append(temp_read_book_page)
            self.tab_widget.setCurrentWidget(temp_read_book_page)
        else:
            # 直接切换当前页面显示
            current_tab_index = self.tab_id_list.index(book_dict["id"])
            self.tab_widget.setCurrentWidget(self.tab_list[current_tab_index])

    def close_tab(self, index):
        if index not in [0, 1]:
            remove_book_id = self.tab_widget.widget(index).__dict__.get("book_id")
            self.tab_widget.removeTab(index)
            # 修改config.ini文件，避免下次打开的时候继续打开文件
            delete_book_info(remove_book_id)

    def update_tab_info(self) -> list:
        tab_id_dict = {}
        for i in range(0, self.tab_widget.count()):
            id = self.tab_widget.widget(i).__dict__.get("book_id", None)
            if id:
                tab_id_dict.update({i: id})
        return tab_id_dict
