import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class mainWindow(QMainWindow):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.setWindowTitle("Battleships")
        self.resize(800, 600)
        
        centralWidget = QWidget()
        centralWidget.setLayout(self.mainLayout())
        self.setCentralWidget(centralWidget)
        self.show()

    def mainLayout(self):
        """Return a layout which combines the game details and game online details layouts"""
        layout = QVBoxLayout()

        gameDetailsLayout = self.gameDetailsLayout()
        gameOnlineDetailsLayout = self.gameOnlineDetailsLayout()

        layout.addLayout(gameDetailsLayout); layout.addLayout(gameOnlineDetailsLayout)
        layout.setSpacing(0)
        return layout

    def gameDetailsLayout(self):
        """Return a layout which holds start game button and game type selector"""
        gameDetailsLayout = QHBoxLayout()
        buttonStartGame = QPushButton("Start online game")
        buttonStartGame.clicked.connect(lambda: self.game.startGame(self.gameDetails))

        selectorGameType = QComboBox()
        selectorGameType.addItems(["online", "offline"])

        def updateGameDetailsLayout(gameType):
            """Update the game details layout based on the game type"""
            buttonStartGame.setText(f"Start {gameType} game")
            # Remove all items from layout and delete layout
            self.deleteItems(self.centralWidget().layout().itemAt(1).layout())
            self.centralWidget().layout().itemAt(1).layout().deleteLater()
            if gameType == "online":
                self.centralWidget().layout().addLayout(self.gameOnlineDetailsLayout())
            elif gameType == "offline":
                self.centralWidget().layout().addLayout(self.gameOfflineDetailsLayout())

        selectorGameType.currentTextChanged.connect(lambda gameType: updateGameDetailsLayout(gameType))
        gameDetailsLayout.addWidget(selectorGameType); gameDetailsLayout.addWidget(buttonStartGame); gameDetailsLayout.setSpacing(0)
        return gameDetailsLayout

    def gameOnlineDetailsLayout(self):
        """Return a layout which holds the connection details"""
        connectionDetailsLayout = QVBoxLayout()
        add = lambda layout, *widgets: list(map(layout.addWidget, widgets))

        serverDetailsLayout = QHBoxLayout()
        inputServer = QLineEdit("localhost"); 
        inputPort = QLineEdit("8080");
        serverDetailsLayout.setSpacing(0)
        add(serverDetailsLayout, QLabel("Server: "), inputServer, QLabel("Port: "), inputPort)
        connectionDetailsLayout.addLayout(serverDetailsLayout)

        roomDetailsLayout = QHBoxLayout()
        inputRoom = QLineEdit("1")
        add(roomDetailsLayout, QLabel("Room: "), inputRoom)
        roomDetailsLayout.setSpacing(0)
        connectionDetailsLayout.addLayout(roomDetailsLayout)

        playerDetailsLayout = QHBoxLayout()
        inputPlayer = QLineEdit("Player1")
        add(playerDetailsLayout, QLabel("Player: "), inputPlayer)
        playerDetailsLayout.setSpacing(0)
        connectionDetailsLayout.addLayout(playerDetailsLayout)

        connectionString = QHBoxLayout()
        inputConnectionString = QLineEdit(f"ws://{inputServer.text()}:{inputPort.text()}/?room={inputRoom.text()}&player={inputPlayer.text()}")
        add(connectionString, QLabel("Connection: "), inputConnectionString)
        connectionString.setSpacing(0)
        connectionDetailsLayout.addLayout(connectionString)

        def updateConnectionString():
            inputConnectionString.setText(f"ws://{inputServer.text()}:{inputPort.text()}/?room={inputRoom.text()}&player={inputPlayer.text()}") 

        def updateGameDetails():
            self.gameDetails = {
                "gameType": "online",
                "server": inputServer.text(),
                "port": inputPort.text(),
                "room": inputRoom.text(),
                "player": inputPlayer.text()
            }
        updateGameDetails()

        # Connect all inputs to updating the ui and gameDetails
        onTextChanged = lambda func, *QLineEdits: list(map(lambda x: x.textChanged.connect(func), QLineEdits))
        onTextChanged(updateConnectionString, inputServer, inputPort, inputRoom, inputPlayer)
        onTextChanged(updateGameDetails, inputServer, inputPort, inputRoom, inputPlayer)

        connectionDetailsLayout.setSpacing(0)
        return connectionDetailsLayout

    def gameOfflineDetailsLayout(self):
        """Return a layout which holds the offline game details"""
        localDetailsLayout = QVBoxLayout()
        add = lambda layout, *widgets: list(map(layout.addWidget, widgets))

        sizeDetailsLayout = QHBoxLayout()
        inputSize = QLineEdit("10")
        validateInputSize = QIntValidator(5, 100)
        inputSize.setValidator(validateInputSize)
        add(sizeDetailsLayout, QLabel("Size: "), inputSize)
        sizeDetailsLayout.setSpacing(0)
        localDetailsLayout.addLayout(sizeDetailsLayout)

        playerAmountDetailsLayout = QHBoxLayout()
        inputPlayerAmount = QLineEdit("2")
        validateInputPlayerAmount = QIntValidator(2, 10)
        inputPlayerAmount.setValidator(validateInputPlayerAmount)
        add(playerAmountDetailsLayout, QLabel("Players: "), inputPlayerAmount)
        playerAmountDetailsLayout.setSpacing(0)
        localDetailsLayout.addLayout(playerAmountDetailsLayout)

        maxBoatsDetailsLayout = QHBoxLayout()
        def updateMaxBoats(size):
            """Update the maxBoatsDetailsLayout based on the size"""
            size = int(size) if size != "" else 0 # If size is empty, set it to 0
            # Remove the old boatAmount
            self.deleteItems(maxBoatsDetailsLayout)

            # Add new items
            maxBoatsDetailsLayout.addWidget(QLabel("Boats: "))
            maxBoats = [0, 0, 4, 3, 2, 1]
            maxBoats = [int(maxBoats[i]*(size/10)) for i in range(len(maxBoats))]
            for length, amount in enumerate(maxBoats):
                inputBoatAmount = QLineEdit(f"{amount}")
                validateInputBoatAmount = QIntValidator(0, amount)
                inputBoatAmount.setValidator(validateInputBoatAmount)
                maxBoatsDetailsLayout.addWidget(inputBoatAmount)
        
        inputSize.textChanged.connect(lambda text: updateMaxBoats(text)) # Update maxBoats when size changes
        updateMaxBoats(int(inputSize.text()))
        maxBoatsDetailsLayout.setSpacing(0)
        localDetailsLayout.addLayout(maxBoatsDetailsLayout)

        playerDetailsLayout = QVBoxLayout()
        def updatePlayerAmount(playerCount):
            """Update the player details layout based on the player amount"""
            playerCount = int(playerCount) if playerCount != "" else 0 # If playerCount is empty, set it to 0
            # Clear layout
            for i in reversed(range(playerDetailsLayout.count())):
                item = playerDetailsLayout.itemAt(i)
                self.deleteItems(item.layout())
                playerDetailsLayout.removeItem(item)

            # Add new items
            for i in range(playerCount):
                player = QHBoxLayout()
                selectorPlayerType = QComboBox(); selectorPlayerType.addItems(["Player", "AI"])
                inputPlayerName = QLineEdit(f"Player{i}")
                selectorPlayerType.currentTextChanged.connect(lambda text: inputPlayerName.setText(f"{text}{i}"))
                add(player, selectorPlayerType, inputPlayerName)
                playerDetailsLayout.addLayout(player)

        inputPlayerAmount.textChanged.connect(lambda text: updatePlayerAmount(text)) # Update playerDetailsLayout when playerAmount changes
        updatePlayerAmount(int(inputPlayerAmount.text()))
        playerDetailsLayout.setSpacing(0)
        localDetailsLayout.addLayout(playerDetailsLayout)

        def updateGameDetails():
            players = []
            for i in range(playerDetailsLayout.count()):
                player = playerDetailsLayout.itemAt(i).layout()
                players[i] = {"type":player.itemAt(0).widget().text(), "name":player.itemAt(1).widget().text()}

            self.gameDetails = {
                "type": "offline",
                "size": inputSize.text(),
                "players": players
            }
        updateGameDetails()

        onTextChanged = lambda func, *QLineEdits: list(map(lambda x: x.textChanged.connect(func), QLineEdits))
        onTextChanged(updateGameDetails, inputSize, inputPlayerAmount)

        localDetailsLayout.setSpacing(0)
        return localDetailsLayout

    def deleteItems(self, layout):
        """Delete all items in a layout so it can be removed"""
        # https://stackoverflow.com/questions/37564728/pyqt-how-to-remove-a-layout-from-a-layout
        # Iterate over all children of the layout and orphan them to be able to delete layout
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                widget = child.widget()
                if widget is not None:
                    #widget.deleteLater()
                    widget.setParent(None)
                else:
                    self.deleteItems(child.layout())