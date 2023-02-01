from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from player import enemy as class_enemy
from ui.mainWindow import deleteItems

class grid(QWidget):
    def __init__(self, player):
        super(QWidget, self).__init__()
        self.mainLayout = QHBoxLayout()
        self.player = self.playerLayout(player)
        self.mainLayout.addLayout(self.player)
        self.enemy = self.playerLayout(player.enemy)
        self.mainLayout.addLayout(self.enemy)
        self.setLayout(self.mainLayout)
        self.show()

    class playerLayout(QVBoxLayout):
        def __init__(self, player):
            super().__init__()
            self.addWidget(QLabel(player.name))
            if not isinstance(player, class_enemy):
                self.boatDetails = self.boatDetailsLayout()
                self.board = self.gridLayout(player, self.boatDetails.details)
                self.addLayout(self.board)
                self.addLayout(self.boatDetails)
            else:
                self.setEnabled(False)
                self.board = self.gridLayout(player)
                self.addLayout(self.board)
            self.setAlignment(Qt.AlignmentFlag.AlignTop)

        class gridLayout(QGridLayout):
            def __init__(self, player, boatDetails=None):
                super().__init__()
                self.setSpacing(0)
                self.player = player
                self.board = player.board
                self.boatDetails = boatDetails
                self.update()

            def update(self):
                deleteItems(self)
                for a in range(self.board.size):
                    for b in range(self.board.size):
                        button = QPushButton(str(self.board.get(b, a)))
                        self.addWidget(button, a, b)
                        button.clicked.connect(lambda c, x=b, y=a: self.player.game.server.sendPlaceBoat(x, y, int(self.boatDetails["length"]), self.boatDetails["direction"]))
        
        class boatDetailsLayout(QHBoxLayout):
            def __init__(self):
                super().__init__()
                self.details = {}
                self.defaultValues()
                # TODO: Automatically get max Boats
                # TODO: Display number of boats left
                self.selectorShipLength = QComboBox()
                self.selectorShipLength.addItems(["2", "3", "4", "5"])
                self.selectorShipLength.setCurrentText(self.details["length"])
                self.selectorShipLength.currentTextChanged.connect(lambda v: self.details.update({"length": v}))
                self.addWidget(self.selectorShipLength)

                self.selectorShipDirection = QComboBox()
                self.selectorShipDirection.addItems(["VERTICAL", "HORIZONTAL"])
                self.selectorShipDirection.setCurrentText(self.details["direction"])
                self.selectorShipDirection.currentTextChanged.connect(lambda v: self.details.update({"direction": v}))
                self.addWidget(self.selectorShipDirection)

            def defaultValues(self):
                self.details["length"] = "2"
                self.details["direction"] = "VERTICAL"