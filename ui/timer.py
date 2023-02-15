from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import time

class timer(QWidget):
    def __init__(self ):
        super(QWidget, self).__init__()
        self.runtime = 0
        self.label = QLabel("00:00:00")
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.button = QPushButton("Start")
        self.button.clicked.connect(self.toggle)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.label)

        self.layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.start()

    def update(self):
        self.runtime += 1 if self.runtime < 24*60*60 else 0
        self.label.setText(time.strftime("%H:%M:%S", time.gmtime(self.runtime)))

    def toggle(self):
        if self.timer.isActive():
            self.pause()
        else:
            self.start()

    def start(self):
        self.timer.start(1000)
        self.button.setText("Pause")

    def pause(self):
        self.timer.stop()
        self.button.setText("Paused")
        self.pauseDialog(self)

    class pauseDialog(QDialog):
        def __init__(self, parent):
            super(QDialog, self).__init__()
            self.parentLayout = parent
            layout = QVBoxLayout()
            layout.addWidget(QLabel("Game is paused"))
            
            layout.addWidget(QPushButton("Resume", clicked=self.resume))
            self.setLayout(layout)
            self.exec()

        def closeEvent(self, event):
            self.parentLayout.start()
            event.accept()

        def resume(self):
            self.close()
            self.parentLayout.start()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = timer()
    window.start()
    sys.exit(app.exec())