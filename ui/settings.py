from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class selectorGameType(QComboBox):
    """Game type selector"""
    def __init__(self, profile):
        super().__init__()
        self.profile = profile

        # Selector settings
        self.addItems(["online"]) #, "offline"])
        self.setCurrentText(self.profile.profile["gameType"])
        self.currentTextChanged.connect(lambda gameType: self.update(gameType))

    def update(self, gameType):
        """Update the game type"""
        self.profile.profile["gameType"] = gameType

class selectorProfile(QComboBox):
    """Profile selector"""
    def __init__(self, pM):
        super().__init__()
        self.pM = pM

        # Selector settings
        self.selectorUpdate()
        self.currentTextChanged.connect(lambda profile: self.update(profile))

    def selectorUpdate(self):
        """Update the selector"""
        self.clear()
        self.addItems(self.pM.profiles.keys())
        self.setCurrentText(self.pM.profile.profileName)

    def update(self, profile):
        """Update the current profile"""
        if profile:
            self.pM.changeProfile(profile)

class profileEditor(QDialog):
    """Profile editor"""
    def __init__(self, pM, selectorProfile):
        super().__init__()
        self.pM = pM
        self.selectorProfile = selectorProfile

        self.setWindowTitle("Profiles manager")
        self.setFixedSize(300, 200)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.listProfiles = QListWidget()
        self.updateList()
        self.layout.addWidget(self.listProfiles)

        self.layoutButtons = QVBoxLayout()
        self.layoutButtons.addWidget(QPushButton("Save", clicked=self.saveProfile))
        self.layoutButtons.addWidget(QPushButton("Create", clicked=self.createProfile))
        self.layoutButtons.addWidget(QPushButton("Delete", clicked=self.deleteProfile))
        self.layoutButtons.addWidget(QPushButton("Rename", clicked=self.renameProfile))

        self.layout.addLayout(self.layoutButtons)

    def closeEvent(self, event):
        event.accept()

    def updateList(self):
        self.listProfiles.clear()
        self.listProfiles.addItems(self.pM.profiles)

    def saveProfile(self):
        item = self.listProfiles.currentItem().text()
        self.pM.saveProfile(item)

    def createProfile(self):
        name, ok = QInputDialog.getText(self, "Create profile", "Profile name")
        if ok and name and name != "default": # Check if the user clicked OK and if the text is not empty
            self.pM.createProfile(name)
            #self.pM.profiles[name] = self.pM.profile
            self.update()

    def deleteProfile(self):
        item = self.listProfiles.currentItem().text()
        if item == "default":
            return
        self.pM.deleteProfile(item)
        self.update() 

    def renameProfile(self):
        item = self.listProfiles.currentItem().text()
        name, ok = QInputDialog.getText(self, "Rename profile", "Profile name")
        if ok and name and name != "default":
            self.pM.renameProfile(item, name)
            self.update()

    def update(self):
        self.selectorProfile.selectorUpdate()
        self.updateList()
