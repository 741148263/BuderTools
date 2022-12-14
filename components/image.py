from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout


class ImagePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.global_layout = QHBoxLayout()
        label = QLabel(self)
        label.setText("image")
        self.global_layout.addWidget(label)
        self.setLayout(self.global_layout)