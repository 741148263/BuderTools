from PyQt5.QtCore import Qt, QDateTime, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTabWidget, QMainWindow, QStatusBar, QLabel


from components.image import ImagePage
from components.music import MusicPage
from components.network_disk import NetWorkDiskPage
from components.novel import NovelPage
from constants.window_constant import *
from window_func.db_handler import BookSqlHandler


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.db = None
        self.setup_window_base()
        self.setup_ui()
        self.setup_db()
        self.setup_status_bar()
        self.setup_timer()

    def setup_window_base(self):
        self.setWindowTitle(SOFTWARE_TITLE + " " + SOFTWARE_VERSION)
        self.resize(SOFTWARE_WIDTH, int(0.618 * SOFTWARE_WIDTH))

    def setup_db(self):
        db = BookSqlHandler("main_thread")
        db.close()
        del db

    def setup_ui(self):
        self.tab_widget = QTabWidget()
        self.tab_widget.setWindowFlags(Qt.FramelessWindowHint)
        # 设置页面显示方向
        self.tab_widget.setTabPosition(QTabWidget.West)
        # tab控件详情页面
        self.novel_page = NovelPage()
        self.music_page = MusicPage()
        # self.image_page = ImagePage()
        self.network_disk_page = NetWorkDiskPage()
        # self.book_page = BookPage()
        self.tab_widget.addTab(self.novel_page, QIcon("static/icon/book.png"), "小说")
        self.tab_widget.addTab(self.music_page, QIcon("static/icon/music.png"), "音乐")
        # self.tab_widget.addTab(self.image_page, QIcon("static/icon/image.png"), "图片")
        self.tab_widget.addTab(self.network_disk_page, QIcon("static/icon/networkdisk.png"), "云盘")
        # self.tab_widget.addTab(self.book_page, QIcon("static/icon_svg/book_lib.png"), "图书")
        # 设置界面的中心控件
        self.setCentralWidget(self.tab_widget)

    def setup_status_bar(self):
        self.status_bar = QStatusBar(self)
        self.temp1_label = QLabel()
        self.temp2_label = QLabel()
        self.temp3_label = QLabel()
        self.temp4_label = QLabel()
        self.temp5_label = QLabel()
        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.status_bar.addWidget(self.temp1_label, 1)
        self.status_bar.addWidget(self.temp2_label, 1)
        self.status_bar.addWidget(self.temp3_label, 1)
        self.status_bar.addWidget(self.temp4_label, 1)
        self.status_bar.addWidget(self.temp5_label, 1)
        self.status_bar.addPermanentWidget(self.time_label, 1)
        self.setStatusBar(self.status_bar)

    def setup_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        time = QDateTime.currentDateTime()
        time_display = time.toString("yyyy-MM-dd hh:mm:ss dddd")
        self.time_label.setText(time_display)
