import base64
import json

import requests
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QHeaderView, \
    QAbstractItemView, QTableWidgetItem, QApplication, QLabel

from constants.window_constant import NETWORK_DISK_TABLE_COLUMN, HOST_LIST
from window_func.notify_handler import NotificationWindow


class NetWorkDiskPage(QWidget):
    def __init__(self):
        super().__init__()
        self.source_list = []
        self.search_key = ""
        self.setup_display()
        self.setup_linkevent()

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
        self.page_label = QLabel()
        self.page_label.setFixedWidth(50)
        self.page_label.setText("页码")
        self.page_edit = QLineEdit()
        self.page_edit.setFixedWidth(100)
        self.page_edit.setText("1")
        self.page_edit.setAlignment(Qt.AlignCenter)
        self.page_edit.setPlaceholderText("输入页码")
        self.page_edit.setMaxLength(3)
        range_number = QIntValidator(self)
        range_number.setRange(1, 100)
        self.page_edit.setValidator(range_number)
        self.search_key_edit = QLineEdit()
        self.search_key_edit.setAlignment(Qt.AlignCenter)
        self.search_key_edit.setPlaceholderText("输入资源名称")
        self.search_key_edit.setFixedWidth(600)
        self.search_key_edit.setFocus()
        self.search_key_edit.setClearButtonEnabled(True)
        self.search_key_edit.setStyleSheet('color: rgb(180, 180, 180); font: 16px "微软雅黑";')
        self.search_btn = QPushButton(QIcon("static/icon/book_search_btn.png"), "搜索")
        self.search_btn.setStyleSheet('color: rgb(180, 180, 180); font: 16px "微软雅黑";')
        self.search_btn.setFixedWidth(100)
        tips_label = QLabel()
        tips_label.setText("点搜索\n页码累加")
        tips_label.setStyleSheet("color: red")
        tips_label.setFixedWidth(60)
        self.top_layout.addWidget(self.page_label)
        self.top_layout.addWidget(self.page_edit)
        self.top_layout.addWidget(self.search_key_edit)
        self.top_layout.addWidget(self.search_btn)
        self.top_layout.addWidget(tips_label)

    def setup_search_result(self):
        self.bottom_layout = QVBoxLayout()
        self.bottom_layout.setAlignment(Qt.AlignCenter)
        self.result_table = QTableWidget()
        # 设置列数量
        self.result_table.setColumnCount(len(NETWORK_DISK_TABLE_COLUMN))
        self.result_table.verticalHeader().setVisible(False)
        # 设置列表头
        self.result_table.setHorizontalHeaderLabels(NETWORK_DISK_TABLE_COLUMN)
        # 设置是否显示网格
        self.result_table.setShowGrid(False)
        # 设置列宽自适应和其他列的宽度
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.result_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.result_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)
        self.result_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Fixed)
        self.result_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Fixed)
        # 设置单元格禁止编辑
        self.result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置整行
        self.result_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 绑定获取单元格内容方法
        self.bottom_layout.addWidget(self.result_table)

    def setup_linkevent(self):
        self.search_btn.clicked.connect(self.search_source)

    def search_source(self):
        book_search_name = self.search_key_edit.text()
        page_number = self.page_edit.text()
        if book_search_name == "":
            NotificationWindow.warning(self, "警告", "搜索关键字不能为空！")
            return
        if page_number == "":
            NotificationWindow.warning(self, "警告", "页码不能为空！")
            return
        if book_search_name == self.search_key:
            self.page_edit.setText(f"{int(page_number) + 1}")
        else:
            self.page_edit.setText("1")
            self.search_key = book_search_name
        self.result_table.setRowCount(0)
        self.source_list.clear()
        search_thread = GetSourceThread(book_search_name, self.page_edit.text())
        search_thread.search_result_pyqtSignal_trigger.connect(self.insert_book_result)
        search_thread.start()
        search_thread.exec()

    def insert_book_result(self, result_obj: dict):
        if result_obj.get("status") != "success":
            NotificationWindow.error(self, "失败", result_obj.get("msg"))
            return
        else:
            self.source_list.extend(result_obj["result"]["items"])
        temp_source_list = result_obj["result"]["items"]
        for source in temp_source_list:
            count = self.result_table.rowCount()
            self.result_table.insertRow(self.result_table.rowCount())
            # index
            index_cell_item = QTableWidgetItem(str(count + 1))
            index_cell_item.setTextAlignment(Qt.AlignCenter)
            self.result_table.setItem(count, 0, index_cell_item)
            # title
            title_cell_item = QTableWidgetItem(str(source.get("title")))
            title_cell_item.setTextAlignment(Qt.AlignCenter)
            self.result_table.setItem(count, 1, title_cell_item)
            source_from_item = QTableWidgetItem("阿里")
            source_from_item.setTextAlignment(Qt.AlignCenter)
            self.result_table.setItem(count, 2, source_from_item)
            author_cell_item = QTableWidgetItem(str(source.get("available_time")))
            author_cell_item.setTextAlignment(Qt.AlignCenter)
            self.result_table.setItem(count, 3, author_cell_item)
            update_chapter_cell_item = QTableWidgetItem(str(source.get("insert_time")))
            update_chapter_cell_item.setTextAlignment(Qt.AlignCenter)
            self.result_table.setItem(count, 4, update_chapter_cell_item)
            add_book_btn = QPushButton("复制")
            add_book_btn.clicked.connect(self.copy_url)
            # 绑按钮事件
            self.result_table.setCellWidget(count, 5, add_book_btn)

    def copy_url(self):
        click_btn = self.sender()
        if click_btn:
            row_index = self.result_table.indexAt(click_btn.pos()).row()
            col_index = self.result_table.indexAt(click_btn.pos()).column()
            if col_index == 5:
                target_book = self.source_list[row_index]
                target_url = target_book["page_url"]
                if target_url:
                    clipboard = QApplication.clipboard()
                    clipboard.setText(target_url)
                    NotificationWindow.success(self, "复制", "复制链接成功！")
                else:
                    NotificationWindow.error(self, "复制", "复制链接失败！")


class GetSourceThread(QThread):
    search_result_pyqtSignal_trigger = pyqtSignal(dict)

    def __init__(self, search_key, page):
        super(GetSourceThread, self).__init__()
        self.search_key = search_key
        self.page = str(page)

    def run(self) -> None:
        for host in HOST_LIST:
            resp = requests.get(host + "/search?keyword=" + self.search_key + "&page=" + self.page + "&s_type=" + "2")
            data = base64.b64decode(resp.text)
            result = json.loads(data)
            if resp.status_code == 200:
                self.search_result_pyqtSignal_trigger.emit(result)
                break
