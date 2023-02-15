from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton

class placeholder(QWidget):
    def __init__(self, player, message):
        super(QWidget, self).__init__()
        self.player = player
        self.server = player.server.socket
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.message = QLabel(message)
        self.layout.addWidget(self.message)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setWindowTitle("Waiting")
        self.resize(300, 100)
        self.show()

    def closeEvent(self, event):
        self.server.close() if self.player.phase != "SETUP" else None
        event.accept()

    def update(self, message):
        self.message.setText(message)