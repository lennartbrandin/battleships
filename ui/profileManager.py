from PyQt6.QtWidgets import *

class profileLayout(QHBoxLayout):
    def __init__(self, pM, updateDetails):
        super().__init__()
        self.setSpacing(0)

        self.updateDetails = updateDetails # Update function of mainLayout
        self.pM = pM
        self.selectorProfile = QComboBox(currentIndexChanged=self.changeProfile)
        self.selectorProfile.addItems(self.pM.profiles)
        self.selectorProfile.setCurrentText("default")
        self.addWidget(self.selectorProfile)

        self.addWidget(QPushButton("Manage profiles", clicked=lambda: self.openManager(self, self.pM)))

    def selectorUpdate(self):
        self.selectorProfile.clear()
        self.selectorProfile.addItems(self.pM.profiles)

    def changeProfile(self):
        if self.selectorProfile.currentText():
            self.pM.changeProfile(self.selectorProfile.currentText())
            self.updateDetails()

    def openManager(self, profileLayout, pM):
        self.manager = profileManagerDialog(profileLayout, pM)

class profileManagerDialog(QDialog):
    def __init__(self, profileLayout, pM):
        super().__init__()
        self.setWindowTitle("Profiles manager")
        self.setFixedSize(300, 200)
        self.profileLayout = profileLayout
        self.pM = pM

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

        self.exec()

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
        if ok and name: # Check if the user clicked OK and if the text is not empty
            self.pM.createProfile(name)
            #self.pM.profiles[name] = self.pM.profile
            self.update()

    def deleteProfile(self):
        item = self.listProfiles.currentItem().text()
        self.pM.deleteProfile(item)
        self.update() 

    def renameProfile(self):
        item = self.listProfiles.currentItem().text()
        name, ok = QInputDialog.getText(self, "Rename profile", "Profile name")
        if ok and name: 
            self.pM.renameProfile(item, name)
            self.update()

    def update(self):
        self.profileLayout.selectorUpdate()
        self.updateList()
