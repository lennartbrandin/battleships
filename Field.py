import sys
from PyQt6.QtWidgets import *
from game import player as class_player
from PyQt6.QtCore import *
from websocketClient import websocketClient


class boardWidget(QWidget):
    def __init__(self, player):
        """Create a QGridLayout with buttons connected to a board"""
        super(QWidget, self).__init__()
        self.player = player
        self.grid = QGridLayout()
        self.initGrid()
        self.updateGrid()
        self.resize(400, 400)
        self.show()

    def initGrid(self):
        """Create a QGridLayout of size with empty buttons"""
        self.setLayout(self.grid)
        self.grid.setSpacing(0)

        for y in range(self.player.board.size):
            for x in range(self.player.board.size):
                # Create button and its policy
                button = QPushButton()
                button.setMinimumSize(20, 20)
                button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                self.grid.addWidget(button, y, x)
                button.clicked.connect(self.on_click(y, x))
    
    def updateGrid(self):
        """Update the grid with the current state of the board"""
        for y in range(self.player.board.size):
            for x in range(self.player.board.size):
                button = self.grid.itemAtPosition(y, x).widget()
                button.setText(str(self.player.board.getState(x, y)))

    def on_click(self, y, x):
        return lambda: self.player.interact(x, y)

class mainWindow(QMainWindow, QThread):
    def __init__(self):
        super().__init__()
        self.threadPool = QThreadPool()
        # Customize the window
        self.setWindowTitle("Battleships")
        self.resize(400, 400)

        selectGameType= QComboBox()
        selectGameType.addItems(["online", "offline"])
        # Make class attribute because we need to change its text according to the game type
        self.startGameButton = QPushButton(f"Start online game") # Online is default
        # On selector change, update the button text and the detail prompts
        selectGameType.currentTextChanged.connect(lambda: self.updateDetails(selectGameType.currentText()))

        # Connect the button to window creation
        self.startGameButton.clicked.connect(lambda: self.newGrid(selectGameType.currentText()))

        # Create a vertical layout with the gameDetails and the gameType specific details
        self.layout = QVBoxLayout()

        # Create a vertical layout with the selector and self.startGameButton
        game = QHBoxLayout()
        game.addWidget(selectGameType)
        game.addWidget(self.startGameButton)
        game.setSpacing(0)
        
        self.layout.addLayout(game); self.layout.addLayout(self.onlineDetails())
        self.layout.setSpacing(0)

        # Create a widget from the layout
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def updateDetails(self, gameType):
        """Replace onlineDetails with offlineDetails if offline is selected and vice versa"""
        self.startGameButton.setText(f"Start {gameType} game")
        item = self.layout.itemAt(1)
        if gameType == "offline":
            self.deleteItemsOfLayout(item.layout())
            self.layout.removeItem(item)
            self.layout.addLayout(self.offlineDetails())
        elif gameType == "online":
            self.deleteItemsOfLayout(item.layout())
            self.layout.removeItem(item)
            self.layout.addLayout(self.onlineDetails())

    def updateConnectionDetails(self, ip, port, room, playerName):
        """Update the connection details"""
        return f"wss://{ip.text()}:{port.text()}/?{room.text()}&{playerName.text()}"

    def deleteItemsOfLayout(self, layout):
        """Delete all items of a layout"""
        # https://stackoverflow.com/questions/37564728/pyqt-how-to-remove-a-layout-from-a-layout
        # Iterate over all items of the layout and orphan them to be able to delete layout
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    # Orphaning sounds like a bad idea, but found no equal
                    widget.setParent(None)
                else:
                    self.deleteItemsOfLayout(item.layout())

    def onlineDetails(self):
        connectionDetails = QVBoxLayout()
        # Prompt for address, port
        serverDetails = QHBoxLayout()
        serverDetails.addWidget(QLabel("Server:")); ip = QLineEdit(); ip.setText("battleships.lennardwalter.com"); serverDetails.addWidget(ip)
        serverDetails.addWidget(QLabel(":")); port = QLineEdit(); port.setText("443"); serverDetails.addWidget(port)
        serverDetails.setSpacing(0)

        # Prompt for room, playerName
        roomDetails = QHBoxLayout()
        playerDetails = QHBoxLayout()
        roomDetails.addWidget(QLabel("Room:")); room = QLineEdit(); room.setText("Room"); roomDetails.addWidget(room)
        playerDetails.addWidget(QLabel("Player:")); playerName = QLineEdit(); playerName.setText("Player"); playerDetails.addWidget(playerName)

        # Assemble connectionString from input
        connectionDetailsString = QHBoxLayout()
        connectionLabel = QLabel("Connection: ")
        connectionString = QLineEdit()
        updateConnectionString = lambda: connectionString.setText(self.updateConnectionDetails(ip, port, room, playerName))
        updateConnectionString()
        connectionString.setReadOnly(True)
        connectionDetailsString.addWidget(connectionLabel)
        connectionDetailsString.addWidget(connectionString)
        # Update the game start button to pass the correct keyword arguments to the newGrid() method
        self.startGameButton.clicked.connect(lambda: self.newGrid("online", ip=connectionString.text(), room=room.text(), playerName=playerName.text()))

        # Update connectionString as info is edited
        for layout in [serverDetails, roomDetails, playerDetails]:
            for i in range(layout.count()):
                item = layout.itemAt(i).widget()
                if isinstance(item, QLineEdit):
                    # Update connectionString on textChanged by getting the updated text
                    item.textChanged.connect(updateConnectionString)

        for layout in [serverDetails, roomDetails, playerDetails, connectionDetailsString]:
            layout.setSpacing(0)
            connectionDetails.addLayout(layout)
        return connectionDetails

    def offlineDetails(self):
        localDetails = QVBoxLayout()
        # Prompt for infos and give default values
        sizeDetails = QHBoxLayout()
        sizeDetails.addWidget(QLabel("Size:")); self.size = QLineEdit(); self.size.setText("10"); sizeDetails.addWidget(self.size)
        sizeDetails.setSpacing(0)

        self.maxBoatsDetails = QHBoxLayout()
        self.maxBoatsDetails.addWidget(QLabel("Max boats:"))
        # TODO: Generate maxBoats depending on size
        maxBoats = [0, 0, 4, 3, 2, 1]
        for amount in maxBoats:
            boatAmount = QLineEdit(); boatAmount.setText(str(amount)); self.maxBoatsDetails.addWidget(boatAmount)

        # Allow selection if is player or AI
        self.playerDetails = QHBoxLayout()
        player1Type = QComboBox(); player1Type.addItems(["Player", "AI"]); self.playerDetails.addWidget(player1Type)
        player1Name = QLineEdit(); player1Name.setText("Player1"); self.playerDetails.addWidget(player1Name)
        player1Type.currentTextChanged.connect(lambda text: player1Name.setText(f"{text}1"))

        player2Type = QComboBox(); player2Type.addItems(["Player", "AI"]); self.playerDetails.addWidget(player2Type)
        player2Name = QLineEdit(); player2Name.setText("Player2"); self.playerDetails.addWidget(player2Name)
        player2Type.currentTextChanged.connect(lambda text: player2Name.setText(f"{text}2"))
        self.playerDetails.setSpacing(2)

        localDetails.addLayout(sizeDetails); localDetails.addLayout(self.maxBoatsDetails); localDetails.addLayout(self.playerDetails)
        localDetails.setSpacing(10)
        return localDetails

    def newGrid(self, gameType, **kw):
        """Create a new window with a grid, or two grids if offline"""
        kw.update((key, value.text()) for key, value in kw.items()) # Extract text from QLineEdit
        if gameType == "online":
            # We need to pass the values to the websocket and the widget, because the widget should even work without websocket
            player = class_player(kw["playerName"], maxBoats=[0, 0, 4, 3, 2, 1], size=10, filler='0')
            self.windowBoard = boardWidget(player)
            self.createWebsocketWorker(kw["ip"], kw["port"], kw["room"], player)

        elif gameType == "offline":
            # Retrieve all maxBoats from the layout's QLineEdits
            maxBoats = []
            for i in range(kw["maxBoatsDetails"].count()):
                item = kw["maxBoatsDetails"].itemAt(i).widget()
                if isinstance(item, QLineEdit):
                    maxBoats.append(int(item.text()))
            # Iterate by elements of all players
            playerDetails = {}
            for i in range(self.playerDetails.count()):
                player = self.playerDetails.itemAt(i).widget()
                for j in player:
                    item = player.itemAt(j).widget()
                    if isinstance(item, QComboBox):
                        pass
                    if isinstance(item, QLineEdit):
                        pass


    def createWebsocketWorker(self, *args):
        """Create the websocketWorker to communicate with the server"""
        self.websocketWorker = websocketClient(*args)
        self.websocketWorker.signals.websocketMessage.connect(lambda message: print(message))
        self.websocketWorker.signals.websocketOpened.connect(lambda: print("Websocket open"))
        self.websocketWorker.signals.GAME_PHASE_CHANGED.connect(lambda phase: print(phase))
        self.websocketWorker.signals.websocketError.connect(lambda error: print(error))
        self.threadPool.start(self.websocketWorker)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = mainWindow()
    main.show()
    sys.exit(app.exec())