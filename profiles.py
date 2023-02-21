import json
import os

class profilesManager():
    def __init__(self):
        self.profiles = self.loadProfiles()
        self.changeProfile("default")

    def save(self):
        for profile in self.profiles.values():
            profile.saveProfile()

    def saveProfile(self, profileName):
        """Save profile"""
        self.profiles[profileName].saveProfile()
            
    def createProfile(self, profileName):
        """Create profile"""
        self.profiles[profileName] = profile(profileName)

    def renameProfile(self, oldName, newName):
        """Rename profile"""
        profile = self.profiles[oldName].profile
        self.deleteProfile(oldName)
        self.createProfile(newName)
        self.profiles[newName].profile = profile
        self.profiles[newName].saveProfile()

    def loadProfiles(self):
        """Load profiles, if nonexistent return empty dict"""
        profiles = {}
        if os.path.exists("profiles"):
            for profileName in os.listdir("profiles"):
                name = profileName[:-5]
                profiles[name] = profile(name)
        return profiles
    
    def changeProfile(self, profileName):
        """Change profile"""
        self.profile = self.profiles[profileName]

    def deleteProfile(self, profileName):
        """Delete profile"""
        self.profiles[profileName].deleteProfile()
        del self.profiles[profileName]

class profile():
    def __init__(self, profileName):
        self.profileName = profileName
        self.profile = self.loadProfile()

    def __str__(self):
        return self.profileName

    def loadProfile(self):
        """Load profile, if nonexistent return empty dict"""
        if os.path.exists(f"profiles/{self.profileName}.json"):
            with open(f"profiles/{self.profileName}.json") as file:
                return json.load(file)
        else:
            return {}

    def saveProfile(self):
        """Save profile"""
        with open(f"profiles/{self.profileName}.json", 'w') as file:
            json.dump(self.profile, file, indent=4, separators=(',', ': '))

    def deleteProfile(self):
        """Delete profile"""
        os.remove(f"profiles/{self.profileName}.json")