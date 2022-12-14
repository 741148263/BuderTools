import requests
import urllib3
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QPushButton, QTextEdit, QColorDialog, \
    QFontDialog
from lxml import etree

from constants.window_constant import SEARCH_RULES
from window_func.db_handler import BookSqlHandler


class ReadComponent(QWidget):

    def __init__(self, book_dict):
        super().__init__()
        self.book_dict = book_dict
        self.book_id = self.book_dict["id"]
        self.book_from = self.book_dict["from"]
        self.chapter_id_list = self.book_dict["id_list"]
        self.book_titles = self.book_dict["title_list"]
        self.book_hrefs = self.book_dict["href_list"]
        self.read_index = self.book_dict["read_index"]
        self.font_color = "black"
        self.current_color = "orange"
        self.hide_flag = True
        self.setup_display()
        self.setup_content()
        self.setup_link_event()

    def setup_link_event(self):
        self.color_button.clicked.connect(self.background_color_select)
        self.font_color_button.clicked.connect(self.font_color_select)
        # self.font_button.clicked.connect(self.font_select )
        self.last_button.clicked.connect(self.last_chapter_request)
        self.next_button.clicked.connect(self.next_chapter_request)
        self.hide_btn.clicked.connect(self.modify_layout)

    def modify_layout(self):
        if self.hide_flag:
            self.left_side.hide()
            self.hide_flag = False
        else:
            self.left_side.show()
            self.hide_flag = True

    def last_chapter_request(self):
        if self.read_index != 0:
            self.read_index -= 1
            self.get_content()

    def next_chapter_request(self):
        if self.read_index != len(self.book_titles) - 1:
            self.read_index += 1
            self.get_content()

    def background_color_select(self):
        try:
            current_color = QColorDialog.getColor()
            if current_color.isValid():
                self.current_color = current_color.name()
                self.book_detail_text.setStyleSheet(
                    "QTextEdit{background-color:%s; border:0px;color: %s}" % (self.current_color, self.font_color))
        except Exception as e:
            print("color", e)

    def font_color_select(self):
        try:
            current_color = QColorDialog.getColor()
            if current_color.isValid():
                self.font_color = current_color.name()
                self.book_detail_text.setStyleSheet(
                    "QTextEdit{background-color:%s; border:0px;color:%s}" % (self.current_color, self.font_color))
        except Exception as e:
            print("color", e)

    def font_select(self):
        current_font, ok = QFontDialog.getFont()
        if ok:
            self.book_detail_text.setFont(current_font)

    def setup_content(self):
        self.type_list.setCurrentRow(self.read_index)
        # 初始化章节内容
        urllib3.disable_warnings()
        book_pattern = SEARCH_RULES.get(self.book_from)
        chapter_content_resp = requests.get(self.book_hrefs[self.read_index], book_pattern.get("header"), verify=False)
        chapter_content_resp.encoding = book_pattern.get("chapterListCharSet")
        chapter_content_parse = etree.HTML(chapter_content_resp.text)
        if book_pattern.get("chapterContentStopIndex"):
            chapter_content = chapter_content_parse.xpath(book_pattern.get("chapterContentXpath"))[
                              :book_pattern.get("chapterContentStopIndex")]
        else:
            chapter_content = chapter_content_parse.xpath(book_pattern.get("chapterContentXpath"))
        self.update_content(chapter_content)

    def get_content(self):
        current_href = self.book_hrefs[self.read_index]
        get_thread = GetContentThread(current_href, self.book_from, self.chapter_id_list[self.read_index])
        get_thread.conentSignalTrigger.connect(self.update_content)
        get_thread.start()
        get_thread.exec_()

    def setup_display(self):
        # 全局布局
        self.global_layout = QHBoxLayout()
        self.setup_left_side()
        self.setup_right_side()
        self.left_side = QWidget()
        self.left_side.setFixedWidth(300)
        self.left_side.setLayout(self.left_layout)
        right_side = QWidget()
        right_side.setLayout(self.right_layout)
        self.global_layout.addWidget(self.left_side)
        self.global_layout.addWidget(right_side)
        self.setLayout(self.global_layout)

    def setup_left_side(self):
        self.left_layout = QVBoxLayout()
        self.type_list = QListWidget()
        self.type_list.setItemAlignment(Qt.AlignHCenter)
        self.type_list.addItems(self.book_titles)
        self.type_list.itemClicked.connect(self.select_chapter)
        self.left_layout.addWidget(self.type_list)

    def setup_right_side(self):
        self.right_layout = QVBoxLayout()
        self.right_top_layout = QHBoxLayout()
        self.hide_btn = QPushButton("隐藏")
        self.right_top_layout.addWidget(self.hide_btn)
        self.last_button = QPushButton("上一页")
        self.right_top_layout.addWidget(self.last_button)
        self.color_button = QPushButton("背景颜色")
        self.right_top_layout.addWidget(self.color_button)
        # self.font_button = QPushButton("字体设置")
        # self.right_top_layout.addWidget(self.font_button)
        self.font_color_button = QPushButton("字体颜色设置")
        self.right_top_layout.addWidget(self.font_color_button)
        self.next_button = QPushButton("下一页")
        self.right_top_layout.addWidget(self.next_button)

        right_top_widget = QWidget()
        right_top_widget.setLayout(self.right_top_layout)
        self.right_layout.addWidget(right_top_widget)

        self.book_detail_text = QTextEdit()
        self.book_detail_text.setFocusPolicy(Qt.NoFocus)
        self.book_detail_text.setTextColor(Qt.green)
        self.right_layout.addWidget(self.book_detail_text)

    def select_chapter(self, item):
        self.read_index = self.book_titles.index(item.text())
        temp_db = BookSqlHandler(self.book_titles[self.read_index])
        temp_db.update_book_read_index(self.book_id, self.read_index)
        self.get_content()

    def update_content(self, content_list):
        chapter_content = ""
        for row in content_list:
            chapter_content += "<p>{}</p>".format(row)
        content = "<h1 style='text-align:center'>{}</h1>".format(self.book_titles[self.read_index]) + chapter_content
        self.book_detail_text.setHtml(content)


class GetContentThread(QThread):
    conentSignalTrigger = pyqtSignal(list)

    def __init__(self, target_href, book_from, chapter_id):
        super(GetContentThread, self).__init__()
        self.target_href = target_href
        self.book_from = book_from
        self.chapter_id = chapter_id

    def run(self) -> None:
        urllib3.disable_warnings()
        book_pattern = SEARCH_RULES.get(self.book_from)
        chapter_content_resp = requests.get(self.target_href, book_pattern.get("header"), verify=False)
        chapter_content_resp.encoding = book_pattern.get("chapterListCharSet")
        chapter_content_parse = etree.HTML(chapter_content_resp.text)
        if book_pattern.get("chapterContentStopIndex"):
            chapter_content = chapter_content_parse.xpath(book_pattern.get("chapterContentXpath"))[
                              :book_pattern.get("chapterContentStopIndex")]
        else:
            chapter_content = chapter_content_parse.xpath(book_pattern.get("chapterContentXpath"))
        self.conentSignalTrigger.emit(chapter_content)
