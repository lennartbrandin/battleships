import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QObject, QThread
from game import player as class_player
from server import server as class_server
from PyQt6.QtCore import QThreadPool


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
        self.thread_manager = QThreadPool()
        # Customize the window
        self.setWindowTitle("Battleships")
        self.resize(400, 400)

        # Create a selector for the game type
        self.selectGameType= QComboBox()
        self.selectGameType.addItems(["online", "offline"])
        # Create a button which will create a new window
        self.startGameButton = QPushButton(f"Start online game") # Online is default
        # On selector change, update the button text and the detail prompts
        self.selectGameType.currentTextChanged.connect(lambda: self.updateDetails(self.selectGameType.currentText()))

        # Connect the button to window creation
        self.startGameButton.clicked.connect(lambda: self.newGrid(self.selectGameType.currentText()))

        # Create a vertical layout with the gameDetails and the gameType specific details
        self.layout = QVBoxLayout()

        # Create a vertical layout with the selector and startGameButton
        game = QHBoxLayout()
        game.addWidget(self.selectGameType)
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
        # self.layout.removeItem(self.onlineDetails() if gameType == "offline" else self.offlineDetails())
        item = self.layout.itemAt(1)
        if gameType == "offline":
            self.deleteItemsOfLayout(item.layout())
            self.layout.removeItem(item)
            self.layout.addLayout(self.offlineDetails())
        elif gameType == "online":
            self.deleteItemsOfLayout(item.layout())
            self.layout.removeItem(item)
            self.layout.addLayout(self.onlineDetails())

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
        # Prompt for infos and give default values
        serverDetails = QHBoxLayout()
        serverDetails.addWidget(QLabel("Server:")); self.ip = QLineEdit(); self.ip.setText("ws://localhost"); serverDetails.addWidget(self.ip)
        serverDetails.addWidget(QLabel(":")); self.port = QLineEdit(); self.port.setText("8080"); serverDetails.addWidget(self.port)
        serverDetails.setSpacing(0)

        roomDetails = QHBoxLayout()
        playerDetails = QHBoxLayout()
        roomDetails.addWidget(QLabel("Room:")); self.room = QLineEdit(); self.room.setText("Room"); roomDetails.addWidget(self.room)
        playerDetails.addWidget(QLabel("Player:")); self.playerName = QLineEdit(); self.playerName.setText("Player"); playerDetails.addWidget(self.playerName)

        # Create a connection string from the input
        connectionDetailsString = QHBoxLayout()
        connectionLabel = QLabel("Connection: ")
        connectionString = QLineEdit()
        updateConnectionString = lambda: connectionString.setText(f"{self.ip.text()}:{self.port.text()}/?{self.room.text()}&{self.playerName.text()}")
        updateConnectionString()
        connectionString.setReadOnly(True)
        connectionDetailsString.addWidget(connectionLabel)
        connectionDetailsString.addWidget(connectionString)

        # QLINEEDIT update connectionString on textChanged as eye candy 
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

        maxBoatsDetails = QHBoxLayout()
        maxBoatsDetails.addWidget(QLabel("Max boats:"))
        # TODO: Generate maxBoats depending on size
        maxBoats = [0, 0, 4, 3, 2, 1]
        for amount in maxBoats:
            boatAmount = QLineEdit(); boatAmount.setText(str(amount)); maxBoatsDetails.addWidget(boatAmount)

        # Allow selection if is player or AI
        playerDetails = QHBoxLayout()
        self.player1Type = QComboBox(); self.player1Type.addItems(["Player", "AI"]); playerDetails.addWidget(self.player1Type)
        self.player1Name = QLineEdit(); self.player1Name.setText("Player1"); playerDetails.addWidget(self.player1Name)
        self.player1Type.currentTextChanged.connect(lambda text: self.player1Name.setText(f"{text}1"))

        self.player2Type = QComboBox(); self.player2Type.addItems(["Player", "AI"]); playerDetails.addWidget(self.player2Type)
        self.player2Name = QLineEdit(); self.player2Name.setText("Player2"); playerDetails.addWidget(self.player2Name)
        self.player2Type.currentTextChanged.connect(lambda text: self.player2Name.setText(f"{text}2"))
        playerDetails.setSpacing(2)

        localDetails.addLayout(sizeDetails); localDetails.addLayout(maxBoatsDetails); localDetails.addLayout(playerDetails)
        localDetails.setSpacing(10)
        return localDetails

    def newGrid(self, gameType):
        """Create a new window with a grid, or two grids if offline"""
        v = lambda var: var.text() # Shortcut for getting the text of a QLineEdit
        if gameType == "online":
            # Use predefined values for the server
            self.windowBoard = boardWidget(
                player=class_player(v(self.playerName), 
                    maxBoats=[0, 0, 4, 3, 2, 1],
                    size=10,
                    filler="0"
                )
            )
            # self.server = class_server(
            #     address=v(self.ip),
            #     port=v(self.port),
            #     room=v(self.room),
            #     player=self.windowBoard.player
            # )

        elif gameType == "offline":
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = mainWindow()
    main.show()
    sys.exit(app.exec())