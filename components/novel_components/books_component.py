from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QHeaderView, \
    QAbstractItemView, QTableWidgetItem, QPushButton, QMenu

from constants.window_constant import SEARCH_RESULT_TABLE_COLUMN
from window_func.config_reader import write_info, add_book_info, delete_book_info
from window_func.db_handler import BookSqlHandler
from window_func.notify_handler import NotificationWindow


class BooksPage(QWidget):
    switch_tab_pyqtSignal_trigger = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.book_list = []
        self.setup_display()
        self.setup_timer()

    def setup_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.setup_book_detail)
        self.timer.start(1000)

    def setup_display(self):
        self.global_layout = QHBoxLayout()
        self.right_layout = QVBoxLayout()
        self.book_table = QTableWidget()
        self.book_table.setColumnCount(len(SEARCH_RESULT_TABLE_COLUMN))
        self.book_table.verticalHeader().setVisible(False)
        # 设置列表头
        self.book_table.setHorizontalHeaderLabels(SEARCH_RESULT_TABLE_COLUMN)
        # 设置是否显示网格
        self.book_table.setShowGrid(False)
        # 设置列宽自适应和其他列的宽度
        self.book_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.book_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.book_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.book_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Fixed)
        self.book_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Fixed)
        self.book_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.Fixed)
        self.book_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置整行
        self.book_table.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.book_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.book_table.customContextMenuRequested[QtCore.QPoint].connect(self.right_click_menu)

        self.right_layout.addWidget(self.book_table)
        right_side = QWidget()
        right_side.setLayout(self.right_layout)
        self.global_layout.addWidget(right_side)
        self.setLayout(self.global_layout)

    def setup_book_detail(self):
        search_db = BookSqlHandler("search_book")
        count = search_db.search_count()
        if len(self.book_list) != count:
            book_list = search_db.search_book()
            self.book_list = book_list
            self.book_table.setRowCount(len(book_list))
            for row_index, row in enumerate(self.book_list):
                # index
                index_cell_item = QTableWidgetItem(str(row[0]))
                index_cell_item.setTextAlignment(Qt.AlignCenter)
                self.book_table.setItem(row_index, 0, index_cell_item)
                # title
                title_cell_item = QTableWidgetItem(str(row[1]))
                title_cell_item.setTextAlignment(Qt.AlignCenter)
                self.book_table.setItem(row_index, 1, title_cell_item)
                # author
                author_cell_item = QTableWidgetItem(str(row[2]))
                author_cell_item.setTextAlignment(Qt.AlignCenter)
                self.book_table.setItem(row_index, 2, author_cell_item)
                # 最新章节
                update_chapter_cell_item = QTableWidgetItem(str(row[3]))
                update_chapter_cell_item.setTextAlignment(Qt.AlignCenter)
                self.book_table.setItem(row_index, 3, update_chapter_cell_item)
                # 来源
                from_cell_item = QTableWidgetItem(str(row[4]))
                from_cell_item.setTextAlignment(Qt.AlignCenter)
                self.book_table.setItem(row_index, 4, from_cell_item)
                # 状态
                status_cell_item = QTableWidgetItem(str(row[5]))
                status_cell_item.setTextAlignment(Qt.AlignCenter)
                self.book_table.setItem(row_index, 5, status_cell_item)
                # 按钮
                add_book_btn = QPushButton("开始阅读")
                add_book_btn.clicked.connect(self.read_book)
                # 绑按钮事件
                self.book_table.setCellWidget(row_index, 6, add_book_btn)

    def read_book(self):
        click_btn = self.sender()
        if click_btn:
            row_index = self.book_table.indexAt(click_btn.pos()).row()
            col_index = self.book_table.indexAt(click_btn.pos()).column()
            if col_index == 6:
                add_book_info(self.book_list[row_index][0])
                # 发送信号，切换tab
                self.switch_tab_pyqtSignal_trigger.emit(self.book_list[row_index])

    def right_click_menu(self, pos):
        pop_menu = QMenu()
        delete_item = pop_menu.addAction("删除")
        action = pop_menu.exec_(self.book_table.mapToGlobal(pos))
        if action == delete_item:
            row_index = self.book_table.currentRow()
            print('rowindex', row_index)
            search_db = BookSqlHandler("search_book")
            ret = search_db.delete_book(self.book_list[row_index][0])
            if ret:
                self.book_table.removeRow(row_index)
                delete_book_info(self.book_list[row_index][0])
                NotificationWindow.success(self, "成功", f"删除【{self.book_list[row_index][1]}】成功")
                self.book_list.pop(row_index)
            else:
                NotificationWindow.error(self, "删除", f"删除【{self.book_list[row_index][1]}】失败")

