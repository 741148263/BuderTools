import os
import sys
from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet

from window_func.config_reader import init_config
from window_ui.main_window import MainWindow


# 初始化qss样式
def get_style() -> str:
    if not os.path.exists("static/qss/window.css"):
        raise Exception("window.css文件不存在")
    else:
        try:
            with open("static/qss/window.css", "r") as fp:
                return fp.read()
        except Exception as e:
            raise Exception(e)


if __name__ == '__main__':
    init_config()
    app = QApplication(sys.argv)
    QApplication.setStyle("Fusion")
    window = MainWindow()
    apply_stylesheet(app, theme='light_teal.xml')
    window.setStyleSheet(get_style())
    window.show()
    sys.exit(app.exec_())
