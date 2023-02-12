from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class gameMenu(QMainWindow):
    """Game configuration menu"""
    def __init__(self, game):
        super().__init__()
        # Style
        self.setWindowTitle("Battleships")
        self.resize(800, 600)

        self.centralWidget = QWidget()
        self.main = self.mainLayout(game) # Pass game to start button function
        self.centralWidget.setLayout(self.main)
        self.setCentralWidget(self.centralWidget)
        self.show()

    class mainLayout(QVBoxLayout):
        """Combination of game type and game details"""
        def __init__(self, game):
            super().__init__()
            self.setSpacing(0)
            self.gameTypeDetails = self.gameTypeDetailsLayout(game)
            self.addLayout(self.gameTypeDetails)
            self.gameDetails = self.gameTypeDetails.gameDetails # Create a reference to the game details layout
            self.addLayout(self.gameDetails)

        class gameTypeDetailsLayout(QHBoxLayout):
            """Game start button and game type selector"""
            def __init__(self, game):
                super().__init__()
                self.game = game
                self.setSpacing(0)
                self.buttonStartGame = QPushButton("Start online game")
                self.selectorGameType = QComboBox()
                self.selectorGameType.addItems(["online", "offline"])
                self.addWidget(self.selectorGameType)
                self.addWidget(self.buttonStartGame)
                self.gameDetails = self.gameDetailsLayout()

                self.buttonStartGame.clicked.connect(lambda: self.game.startGame(self.gameDetails.details))
                # Update the game details layout when the game type is changed
                self.selectorGameType.currentTextChanged.connect(lambda gameType: self.updateGameDetailsLayout(gameType))

            def updateGameDetailsLayout(self, gameType):
                """Update the game details layout based on the game type"""
                self.buttonStartGame.setText(f"Start {gameType} game")
                self.gameDetails.update(gameType)

            class gameDetailsLayout(QVBoxLayout):
                """Store the game details and create a layout for them"""
                def __init__(self):
                    super().__init__()
                    self.setSpacing(0)
                    self.details = {}
                    self.defaultValues()
                    self.update(self.details["gameType"]) # Creation of layout using the default gameType

                def defaultValues(self):
                    """Set the default values for the game details"""
                    self.details["gameType"] = "online"

                    # Online game details
                    self.details["address"] = "localhost"
                    self.details["port"] = "8080"
                    self.details["room"] = "1"
                    self.details["name"] = "Player"

                    # Offline game details
                    self.details["board size"] = "10"
                    self.details["max boats"] = {k: str(v) for k, v in enumerate([0, 0, 4, 3, 2, 1])} # {"length": "amount"}
                    self.details["player amount"] = "2"

                def update(self, gameType):
                    """Update the game details layout based on the game type"""
                    self.details["gameType"] = gameType

                    # Delete all items in the layout
                    deleteItems(self)

                    # Add the correct items to the layout
                    def detailPrompt(label, dict=self.details):
                        """Create a label and input for a given game detail"""
                        layout = QHBoxLayout()
                        layout.addWidget(QLabel(f"{label}:"))
                        key = int(label) if label.isnumeric() else label.lower() 
                        input = QLineEdit(dict[key]) # Set the start value to the saved game detail (Except for maxBoats)
                        input.textChanged.connect(lambda text: dict.update({key: text})) # Update the game detail when the input is changed
                        layout.addWidget(input)
                        return layout

                    # Add the correct items to the layout
                    if gameType == "online":
                        [self.addLayout(detailPrompt(label)) for label in ["Address", "Port", "Room", "Name"]]
                    elif gameType == "offline":
                        [self.addLayout(detailPrompt(label)) for label in ["Board size", "Player amount"]]

                        maxBoats = QHBoxLayout()
                        maxBoats.addWidget(QLabel("Max boats:"))
                        [maxBoats.addLayout(detailPrompt(str(label), self.details["max boats"])) for label in self.details["max boats"]]
                        self.addLayout(maxBoats)

                    

def deleteItems(layout):
    """Delete all items in the layout"""
    if layout:
        while layout.count(): # Iterate as long as there are items in the layout
            child = layout.takeAt(0) # Remove the first item in the layout
            if child.widget():
                child.widget().deleteLater() # Delete the widget
                child.widget().setParent(None) # Remove the widget from the layout
            elif child.layout():
                deleteItems(child.layout()) # Delete items in the layout
            else:
                child.deleteLater()
                QObjectCleanupHandler().add(child)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    game = gameMenu()
    sys.exit(app.exec())