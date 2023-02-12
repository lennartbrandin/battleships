from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from ui.gameMenu import deleteItems

class grid(QDialog):
    def __init__(self, player):
        super(QDialog, self).__init__()
        self.server = player.server.socket
        self.mainLayout = QVBoxLayout()

        self.boatDetails = self.boatDetailsLayout(player)
        self.playerLayouts = QHBoxLayout()
        self.player = self.playerLayout(player, self.boatDetails.details)
        self.enemy = self.playerLayout(player.enemy)

        self.playerLayouts.addLayout(self.player)
        self.playerLayouts.addLayout(self.enemy)
        self.mainLayout.addLayout(self.playerLayouts)
        self.mainLayout.addLayout(self.boatDetails)

        self.setWindowModality(Qt.WindowModality.WindowModal)
        # Apply style only on this dialog
        self.setObjectName("grid")
        self.setStyleSheet("QDialog#grid {border: 1px solid #DDDDDD;}")
        self.setLayout(self.mainLayout)

    def closeEvent(self, event):
        self.server.close() # This will trigger the game cleanup
        event.accept()

    class playerLayout(QVBoxLayout):
        def __init__(self, player, boatDetails=None):
            super().__init__()
            self.boatDetails = boatDetails
            self.addWidget(QLabel(player.name))
            self.board = self.gridLayout(player, self.boatDetails)
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
                        state = self.board.get(b, a)
                        button = QPushButton(str(state))
                        colors = {"HIT": "red", "MISS": "blue", "SUNK": "red", "EMPTY": "white"}
                        color = colors[state] if state in colors else colors["EMPTY"]
                        button.setStyleSheet(f"background-color: {color}; border-radius: 0px; border: 0.5px solid #DDDDDD;")
                        button.setFixedSize(35, 35)
                        self.addWidget(button, a, b)
                        if not self.player.isEnemy:
                            button.clicked.connect(lambda c, x=b, y=a: self.player.server.sendPlaceBoat(x, y, int(self.boatDetails["length"]), self.boatDetails["direction"]))
                        else:
                            button.clicked.connect(lambda c, x=b, y=a: self.player.server.sendFireShot(x, y))
        
    class boatDetailsLayout(QHBoxLayout):
        def __init__(self, player):
            super().__init__()
            self.player = player
            self.board = player.board
            self.details = {}
            self.defaultValues()
            # TODO: Automatically get max Boats
            # TODO: Display number of boats left
            self.selectorShipLength = QComboBox()
            self.selectorShipLength.addItems([str(k) for k, v in self.board.maxBoats.items()])
            self.selectorShipLength.setCurrentText(self.details["length"])
            self.selectorShipLength.currentTextChanged.connect(lambda v: self.details.update({"length": v}))
            self.addWidget(self.selectorShipLength)

            self.selectorShipDirection = QComboBox()
            self.selectorShipDirection.addItems(["VERTICAL", "HORIZONTAL"])
            self.selectorShipDirection.setCurrentText(self.details["direction"])
            self.selectorShipDirection.currentTextChanged.connect(lambda v: self.details.update({"direction": v}))
            self.addWidget(self.selectorShipDirection)

            def autoPlace():
                for l in range(len(self.board.maxBoats)):
                    for a in range(self.board.size):
                        for b in range(self.board.size):
                            self.player.server.sendPlaceBoat(b, a, l, self.details["direction"])
            self.placeAllBoats = QPushButton("AutoPlace")
            self.placeAllBoats.clicked.connect(lambda: autoPlace())
            self.addWidget(self.placeAllBoats)

            def autoShoot():
                for a in range(self.board.size):
                    for b in range(self.board.size):
                        self.player.server.sendFireShot(a, b)
            self.shootAll = QPushButton("AutoShoot")
            self.shootAll.clicked.connect(lambda: autoShoot())
            self.addWidget(self.shootAll)

        def defaultValues(self):
            self.details["length"] = "2"
            self.details["direction"] = "VERTICAL"