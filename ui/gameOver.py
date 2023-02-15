from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class gameOverDialog(QDialog):
    def __init__(self, grid, winner, reason):
        super(QDialog, self).__init__()
        self.grid = grid
        self.winner = winner
        self.reason = reason
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(QLabel("Game over"))
        self.layout.addWidget(QLabel("Winner: " + self.winner.name))
        self.layout.addWidget(QLabel("Reason: " + self.reason))
        self.layout.addWidget(QPushButton("Close", clicked=self.close))
        self.exec()

    def closeEvent(self, event):
        self.grid.close()
        event.accept()