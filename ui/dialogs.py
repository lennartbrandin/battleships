from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import time

class gameOverDialog(QDialog):
    def __init__(self, grid, winner, reason):
        super(QDialog, self).__init__()
        self.grid = grid
        self.winner = winner
        self.reason = reason
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(QLabel("Game over"))
        self.layout.addWidget(QLabel("Winner: " + self.winner))
        self.layout.addWidget(QLabel("Reason: " + self.reason))
        self.layout.addWidget(QPushButton("Close", clicked=self.close))
        self.exec()

    def closeEvent(self, event):
        # self.grid.closeGameOver()
        self.grid.close()
        event.accept()

class placeholderDialog(QWidget):
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
        try:
            self.server.close() if self.player.phase != "SETUP" else None
        except AttributeError:
            pass
        event.accept()

    def update(self, message):
        self.message.setText(message)

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
            self.setWindowTitle("Paused")
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

class error(QDialog):
    def __init__(self, message):
        super(QDialog, self).__init__()
        self.setWindowTitle("Error")
        layout = QVBoxLayout()
        layout.addWidget(QLabel(message))
        layout.addWidget(QPushButton("Close", clicked=self.close))
        self.setLayout(layout)
        self.exec()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = timer()
    window.start()
    sys.exit(app.exec())