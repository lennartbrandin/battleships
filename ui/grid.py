from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from ui.mainMenu import deleteItems
from ui.dialogs import gameOverDialog, timer
from multipledispatch import dispatch

class grid(QWidget):
    def __init__(self, player):
        super(QWidget, self).__init__()
        # self.player = player
        self.server = player.server.socket
        self.mainLayout = QVBoxLayout()

        self.gameInfo = self.gameInfoLayout(player.roomName, "SETUP")
        self.mainLayout.addLayout(self.gameInfo)

        self.setWindowTitle("Battleships")
        # Apply style only on this dialog
        self.setObjectName("grid")
        self.setStyleSheet("QWidget#grid {border: 1px solid #DDDDDD;}")
        self.setLayout(self.mainLayout)

        self.show()

    def start(self, player):
        self.boatDetails = self.boatDetailsLayout(player)
        self.playerLayouts = QHBoxLayout()
        self.player = self.playerLayout(player, self.boatDetails.details)
        self.enemy = self.playerLayout(player.enemy)

        self.playerLayouts.addLayout(self.player)
        self.playerLayouts.addLayout(self.enemy)
        self.mainLayout.addLayout(self.playerLayouts)
        self.mainLayout.addLayout(self.boatDetails)

    def gameOver(self, player, reason):
        self.gameInfo.timer.timer.stop()
        self.gameInfo.timer.button.setText("Game ended")
        self.gameOver = gameOverDialog(self, player, reason)

    def closeEvent(self, event):
        self.server.close()
        event.accept()

    class gameInfoLayout(QHBoxLayout):
        def __init__(self, roomName, gamePhase):
            super().__init__()
            self.roomName = self.roomNameLayout(roomName)
            self.gamePhase = self.gamePhaseLayout(gamePhase)
            self.timer = timer()
            self.addLayout(self.roomName)
            self.addLayout(self.gamePhase)
            self.addWidget(self.timer)

        class roomNameLayout(QHBoxLayout):
            def __init__(self, name):
                super().__init__()
                self.label = QLabel("Room name: ")
                self.name = QLabel(name)
                self.addWidget(self.label)
                self.addWidget(self.name)
                self.setAlignment(Qt.AlignmentFlag.AlignLeft)
                self.setSpacing(0)

        class gamePhaseLayout(QHBoxLayout):
            def __init__(self, phase):
                super().__init__()
                self.label = QLabel("Game phase: ")
                self.phase = QLabel(phase)
                self.addWidget(self.label)
                self.addWidget(self.phase)
                self.setAlignment(Qt.AlignmentFlag.AlignLeft)
                self.setSpacing(0)

            def update(self, phase):
                self.phase.setText(phase)

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
                self.game = player.game
                self.board = player.board
                self.boatDetails = boatDetails
                self.update()

            @dispatch()
            def update(self):
                deleteItems(self)
                for a in range(self.board.size):
                    for b in range(self.board.size):
                        self.update(a, b)

            @dispatch(int, int)
            def update(self, x, y):
                if self.itemAtPosition(y, x):
                    self.itemAtPosition(y, x).widget().deleteLater()
                state = self.board.get(x, y)
                button = QPushButton()
                button.setFixedSize(40, 40)
                colors = {"HIT": "red", "MISS": "grey", "SUNK": "black", self.player.board.filler: "white"}
                if state in colors:
                    color = colors[state]
                    button.setStyleSheet(f"background-color: {color}; border-radius: 0px; border: 0.5px solid #DDDDDD;")
                else:
                    # State is a boat
                    while not hasattr(self.game, "icons"):
                        print("Waiting for icons")
                        __import__("time").sleep(2)
                    button.setIcon(self.game.icons.get(state, x, y))
                    button.setIconSize(QSize(40, 40))

                if self.player.isEnemy:
                    # If self is enemy, use the socket of self.enemy (the player)
                    button.clicked.connect(lambda c, x=x, y=y: self.player.enemy.server.sendFireShot(x, y))
                else:
                    button.clicked.connect(lambda c, x=x, y=y: self.player.server.sendPlaceBoat(x, y, int(self.boatDetails["length"]), self.boatDetails["direction"]))

                self.addWidget(button, y, x)

        
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
                newBoard = self.player.board.autoPlace()
                for boatLength in newBoard.boats:
                    for boat in boatLength:
                        self.player.server.sendPlaceBoat(boat)

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