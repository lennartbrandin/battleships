from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import time

class timer(QWidget):
    def __init__(self ):
        super(QWidget, self).__init__()
        self.runtime = 0
        self.label = QLabel()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.show()

    def update(self):
        self.runtime += 1
        self.label.setText(time.strftime("%H:%M:%S", time.gmtime(self.runtime)))

    def start(self):
        self.timer.start(1000)

    def stop(self):
        self.timer.stop()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = timer()
    window.start()
    sys.exit(app.exec())