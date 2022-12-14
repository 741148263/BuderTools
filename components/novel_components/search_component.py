import requests
import urllib3

from lxml import etree
from urllib import parse
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QHeaderView, \
    QAbstractItemView, QTableWidgetItem

from constants.window_constant import SEARCH_RESULT_TABLE_COLUMN, SEARCH_RULES, INSERT_BOOK_CASE
from window_func.db_handler import BookSqlHandler
from window_func.notify_handler import NotificationWindow


class SearchPage(QWidget):
    def __init__(self):
        super().__init__()
        self.search_result_books = []
        self.setup_display()
        self.setup_link_event()

    def setup_link_event(self):
        self.search_btn.clicked.connect(self.search_book)

    def setup_display(self):
        self.global_layout = QVBoxLayout()
        self.setup_search_top()
        top_widget = QWidget()
        top_widget.setLayout(self.top_layout)
        bottom_widget = QWidget()
        self.setup_search_result()
        bottom_widget.setLayout(self.bottom_layout)
        self.global_layout.addWidget(top_widget)
        self.global_layout.addWidget(bottom_widget)
        self.setLayout(self.global_layout)

    def setup_search_top(self):
        # 页面全局布局 垂直布局
        # 上部组件水平布局
        self.top_layout = QHBoxLayout()
        self.top_layout.setAlignment(Qt.AlignCenter)
        self.search_key_edit = QLineEdit()
        self.search_key_edit.setAlignment(Qt.AlignCenter)
        self.search_key_edit.setPlaceholderText("输入作者/小说名称")
        self.search_key_edit.setFixedWidth(600)
        self.search_key_edit.setFocus()
        self.search_key_edit.setClearButtonEnabled(True)
        self.search_key_edit.setStyleSheet('color: rgb(180, 180, 180); font: 16px "微软雅黑";')
        self.search_btn = QPushButton(QIcon("static/icon/book_search_btn.png"), "搜索")
        self.search_btn.setStyleSheet('color: rgb(180, 180, 180); font: 16px "微软雅黑";')
        self.search_btn.setFixedWidth(100)
        self.top_layout.addWidget(self.search_key_edit)
        self.top_layout.addWidget(self.search_btn)

    def setup_search_result(self):
        self.bottom_layout = QVBoxLayout()
        self.bottom_layout.setAlignment(Qt.AlignCenter)
        self.result_table = QTableWidget()
        # 设置列数量
        self.result_table.setColumnCount(len(SEARCH_RESULT_TABLE_COLUMN))
        self.result_table.verticalHeader().setVisible(False)
        # 设置列表头
        self.result_table.setHorizontalHeaderLabels(SEARCH_RESULT_TABLE_COLUMN)
        # 设置是否显示网格
        self.result_table.setShowGrid(False)
        # 设置列宽自适应和其他列的宽度
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.result_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.result_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Fixed)
        self.result_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Fixed)
        self.result_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.Fixed)
        # 设置单元格禁止编辑
        self.result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置整行
        self.result_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 绑定获取单元格内容方法
        self.bottom_layout.addWidget(self.result_table)

    def search_book(self):
        book_search_name = self.search_key_edit.text()
        if book_search_name:
            self.result_table.setRowCount(0)
            self.search_result_books.clear()
            search_thread = SearchThread(book_search_name)
            search_thread.search_result_signal_trigger.connect(self.insert_book_result)
            search_thread.start()
            search_thread.exec()

    def insert_book_result(self, book_obj: dict):
        self.search_result_books.append(book_obj)
        count = self.result_table.rowCount()
        self.result_table.insertRow(self.result_table.rowCount())
        # index
        index_cell_item = QTableWidgetItem(str(count + 1))
        index_cell_item.setTextAlignment(Qt.AlignCenter)
        self.result_table.setItem(count, 0, index_cell_item)
        # title
        title_cell_item = QTableWidgetItem(str(book_obj.get("title")))
        title_cell_item.setTextAlignment(Qt.AlignCenter)
        self.result_table.setItem(count, 1, title_cell_item)
        # author
        author_cell_item = QTableWidgetItem(str(book_obj.get("author")))
        author_cell_item.setTextAlignment(Qt.AlignCenter)
        self.result_table.setItem(count, 2, author_cell_item)
        # 最新章节
        update_chapter_cell_item = QTableWidgetItem(str(book_obj.get("update_chapter")))
        update_chapter_cell_item.setTextAlignment(Qt.AlignCenter)
        self.result_table.setItem(count, 3, update_chapter_cell_item)
        # 来源
        from_cell_item = QTableWidgetItem(str(book_obj.get("from")))
        from_cell_item.setTextAlignment(Qt.AlignCenter)
        self.result_table.setItem(count, 4, from_cell_item)
        # 状态
        status_cell_item = QTableWidgetItem(str(book_obj.get("status")))
        status_cell_item.setTextAlignment(Qt.AlignCenter)
        self.result_table.setItem(count, 5, status_cell_item)
        # 按钮
        add_book_btn = QPushButton("加入书架")
        add_book_btn.clicked.connect(self.add_book)
        # 绑按钮事件
        self.result_table.setCellWidget(count, 6, add_book_btn)

    def add_book(self):
        click_btn = self.sender()
        if click_btn:
            row_index = self.result_table.indexAt(click_btn.pos()).row()
            col_index = self.result_table.indexAt(click_btn.pos()).column()
            if col_index == 6:
                target_book = self.search_result_books[row_index]
                add_thread = AddBookThread(target_book)
                add_thread.add_result_signal_trigger.connect(self.notify_result)
                add_thread.start()
                add_thread.exec()

    def notify_result(self, result_flag: bool):
        if result_flag:
            NotificationWindow.success(self, "成功", "添加成功")
        else:
            NotificationWindow.error(self, "成功", "添加失败")


class AddBookThread(QThread):
    add_result_signal_trigger = pyqtSignal(bool)

    def __init__(self, book: dict):
        super(AddBookThread, self).__init__()
        self.target_book = book

    def run(self) -> None:
        insert_db = BookSqlHandler("add_thread")
        insert_result = insert_db.insert_book(self.target_book)
        self.add_result_signal_trigger.emit(insert_result)
        no_chapter_list = insert_db.search_no_chapter()
        if no_chapter_list:
            for book in no_chapter_list:
                book_pattern = SEARCH_RULES.get(book[1])
                urllib3.disable_warnings()
                chapter_list_resp = requests.get(book[2], book_pattern.get("header"), verify=False)
                chapter_list_resp.encoding = book_pattern.get("chapterListCharSet")
                chapter_list_parse = etree.HTML(chapter_list_resp.text)
                chapter_title_list = chapter_list_parse.xpath(
                    book_pattern.get("chapterXpath").get("chapterTitleXpath"))[book_pattern.get("chapterStartIndex"):]
                chapter_href_list = chapter_list_parse.xpath(book_pattern.get("chapterXpath").get("chapterHrefXpath"))[
                                    book_pattern.get("chapterStartIndex"):]
                print("chapter_title_list", chapter_title_list)
                print("chapter_href_list", chapter_href_list)
                if book_pattern.get("chapterHrefJoin"):
                    chapter_href_list = [book_pattern.get("baseUrl") + href for href in chapter_href_list]
                if all([chapter_title_list, chapter_href_list]):
                    result = insert_db.insert_book_case(book[0], chapter_title_list, chapter_href_list)
                    if result:
                        insert_db.update_book_chapter_state(book[0])


# 搜索线程
class SearchThread(QThread):
    search_result_signal_trigger = pyqtSignal(dict)

    def __init__(self, book_key):
        super(SearchThread, self).__init__()
        self.book_search_key = book_key
        self.search_rules = SEARCH_RULES

    def run(self):
        for source in self.search_rules.values():
            source_from = source.get("sourceName")
            current_url = source.get("searchUrl")
            current_header = {"User-Agent": source.get("agent",
                                                       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")}
            try:
                urllib3.disable_warnings()
                search_resp = requests.get(
                    current_url.format(parse.quote(self.book_search_key, encoding=source.get("searchCharSet"))),
                    headers=current_header, verify=False, timeout=5)
                search_resp.encoding = source.get("searchCharSet")
                search_resp.close()
            except:
                continue
            etree_handler = etree.HTML(search_resp.text)
            title_pattern = source.get("searchXpath").get("titleRuleXpath", None)
            if title_pattern:
                titles = etree_handler.xpath(title_pattern)
                if not titles:
                    continue
            href_pattern = source.get("searchXpath").get("hrefRuleXpath", None)
            if href_pattern:
                hrefs = etree_handler.xpath(href_pattern)
            update_chapter_pattern = source.get("searchXpath").get("updateChapterXpath")
            if update_chapter_pattern:
                update_chapters = etree_handler.xpath(update_chapter_pattern)
            else:
                update_chapters = ["" for _ in titles]
            author_pattern = source.get("searchXpath").get("autherXpath")
            if author_pattern:
                global authors
                authors = etree_handler.xpath(author_pattern)
            status_pattern = source.get("searchXpath").get("statusXpath")
            if status_pattern:
                global statuses
                statuses = etree_handler.xpath(status_pattern)
            else:
                statuses = ["/" for _ in titles]
            for title, update_chapter, author, status, href in zip(titles, update_chapters, authors, statuses, hrefs):
                self.search_result_signal_trigger.emit({
                    "title": title,
                    "update_chapter": update_chapter,
                    "author": author,
                    "status": status,
                    "href": href,
                    "from": source_from,
                })
