from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTabWidget, QMainWindow

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
        self.image_page = ImagePage()
        self.network_disk_page = NetWorkDiskPage()
        self.tab_widget.addTab(self.novel_page, QIcon("static/icon/book.png"), "小说")
        self.tab_widget.addTab(self.music_page, QIcon("static/icon/music.png"), "音乐")
        self.tab_widget.addTab(self.image_page, QIcon("static/icon/image.png"), "图片")
        self.tab_widget.addTab(self.network_disk_page, QIcon("static/icon/networkdisk.png"), "阿里云盘搜索")
        # 设置界面的中心控件
        self.setCentralWidget(self.tab_widget)


class GetSourceThread(QThread):
    def __init__(self):
        super(GetSourceThread, self).__init__()

    def run(self) -> None:
        pass
