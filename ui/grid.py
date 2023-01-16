from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class grid(QWidget):
    def __init__(self, player):
        super(QWidget, self).__init__()
        self.player = player
        self.game = player.game
        self.setLayout(self.mainLayout())
        self.show()

    
    def mainLayout(self):
        """Return a layout which holds the player's board and enemy's board"""
        layout = QHBoxLayout()
        layout.addLayout(self.boardLayout(self.player.board, self.player.name))
        layout.addLayout(self.boardLayout(self.player.enemy.board, self.player.enemy.name))
        return layout

    def boardLayout(self, board, name):
        """Return a layout which holds the board and name"""
        layout = QVBoxLayout()
        layout.addWidget(QLabel(name))
        layout.addLayout(self.boardGridLayout(board))
        return layout

    def boardGridLayout(self, board):
        """Return a layout which holds the board"""
        layout = QGridLayout()
        for x in range(self.game.size):
            for y in range(self.game.size):
                button = QPushButton(board.get(x, y))
                button.clicked.connect(lambda: self.player.shoot(x, y))
                layout.addWidget(button, x, y)
        return layout