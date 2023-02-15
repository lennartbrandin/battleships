from PyQt6.QtWidgets import *
from profiles import profilesManager

class profileLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.setSpacing(0)
        self.pM = profilesManager()
        self.selectorProfile = QComboBox()
        self.selectorProfile.addItems(self.pM.profiles)
        self.selectorProfile.currentIndexChanged.connect(self.changeProfile)
        self.addWidget(self.selectorProfile)

        self.addWidget(QPushButton("Manage profiles", clicked=lambda: self.openManager(self, self.pM)))

    def selectorUpdate(self):
        self.selectorProfile.clear()
        self.selectorProfile.addItems(self.pM.profiles)

    def changeProfile(self):
        if self.selectorProfile.currentText() != "":
            self.pM.changeProfile(self.selectorProfile.currentText())

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
        self.listProfiles.addItems(self.pM.profiles)
        self.layout.addWidget(self.listProfiles)

        self.layoutButtons = QVBoxLayout()
        self.layoutButtons.addWidget(QPushButton("Edit", clicked=self.editProfile))
        self.layoutButtons.addWidget(QPushButton("Create", clicked=self.createProfile))
        self.layoutButtons.addWidget(QPushButton("Delete", clicked=self.deleteProfile))
        self.layoutButtons.addWidget(QPushButton("Rename", clicked=self.renameProfile))

        self.layout.addLayout(self.layoutButtons)

        self.exec()

    def closeEvent(self, event):
        self.pM.save()
        event.accept()

    def updateList(self):
        self.listProfiles.clear()
        self.listProfiles.addItems(self.pM.profiles)

    def editProfile(self):
        pass

    def createProfile(self):
        name, ok = QInputDialog.getText(self, "Create profile", "Profile name")
        if ok:
            if name != "":
                self.pM.createProfile(name)
                self.pM.profiles[name] = self.pM.profile
                self.update()

    def deleteProfile(self):
        item = self.listProfiles.currentItem().text()
        del self.pM.profiles[item] 
        self.update() 

    def renameProfile(self):
        pass

    def update(self):
        self.profileLayout.selectorUpdate()
        self.updateList()
