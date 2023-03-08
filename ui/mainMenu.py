from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from profiles import profilesManager
from ui.settings import selectorGameType, selectorProfile, profileEditor

class mainMenu(QMainWindow):
    """Main menu holding the start button, game type selector, profile management and profile layout"""
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.pM = profilesManager()

        # Style
        self.setWindowTitle("Battleships")
        self.resize(400, 300)

        self.layout = QVBoxLayout()
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)

        # Game start button & game type selector
        self.startLayout = QVBoxLayout()
        self.startLayout.setSpacing(0)
        self.buttonStartGame = QPushButton("Start game")
        self.buttonStartGame.clicked.connect(lambda: self.game.startGame(self.pM.profile.profile))

        self.selectorGameType = selectorGameType(self.pM.profile)
        self.selectorGameType.currentTextChanged.connect(lambda gameType: self.profileLayout.update(gameType))

        self.startLayout.addWidget(self.buttonStartGame)
        self.startLayout.addWidget(self.selectorGameType)

        # Profile layout
        self.profileLayout = profileLayout(self.pM)
        self.profileManagement = profileManagementLayout(self.pM, self.profileLayout)

        # Add layouts to main layout
        self.topLayout = QHBoxLayout()
        self.topLayout.addLayout(self.profileManagement)
        self.topLayout.addLayout(self.startLayout)

        self.layout.addLayout(self.topLayout)
        self.layout.addLayout(self.profileLayout)

        self.show()

class profileManagementLayout(QVBoxLayout):
    """Profile selector and profile editor"""
    def __init__(self, pM, profileLayout):
        super().__init__()
        self.pM = pM
        self.profileLayout = profileLayout # Allow calling update function

        # Style
        self.setSpacing(0)

        # Profile selector
        self.selectorProfile = selectorProfile(self.pM)
        # Update the input fields when the profile is changed
        self.selectorProfile.currentTextChanged.connect(lambda: self.profileLayout.update(self.pM.profile.profile["gameType"]))

        # Profile editor
        self.profileEditor = profileEditor(self.pM, self.selectorProfile)
        self.buttonEditProfile = QPushButton("Manage profiles")
        self.buttonEditProfile.clicked.connect(lambda: self.openProfileEditor())

        # Add widgets to layout
        self.addWidget(self.buttonEditProfile)
        self.addWidget(self.selectorProfile)

    def openProfileEditor(self):
        """Open the profile editor"""
        self.profileEditor.exec()


class profileLayout(QVBoxLayout):
    """Profile layout holding the detail prompts"""
    def __init__(self, pM):
        super().__init__()
        self.pM = pM

        # Style
        self.setSpacing(0)

        self.update(self.pM.profile.profile["gameType"]) # Creation of layout using the default gameType

    def update(self, gameType):
        """Update the game details layout based on the game type"""
        self.pM.profile.profile["gameType"] = gameType

        # Delete all items in the layout
        deleteItems(self)

        # Add the correct items to the layout
        def detailPrompt(label, dict=self.pM.profile.profile):
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
        # elif gameType == "offline":
        #     [self.addLayout(detailPrompt(label)) for label in ["Board size", "Player amount"]]

        #     maxBoats = QHBoxLayout()
        #     maxBoats.addWidget(QLabel("Max boats:"))
        #     [maxBoats.addLayout(detailPrompt(str(label), self.pM.profile.profile["max boats"])) for label in self.pM.profile.profile["max boats"]]
        #     self.addLayout(maxBoats)  

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