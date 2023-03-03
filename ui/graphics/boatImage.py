import os
import image_slicer
from boat import boat
from io import BytesIO
from PyQt6.QtGui import QIcon, QPixmap
from PIL import Image
from PyQt6.QtCore import QRunnable, pyqtSignal, pyqtSlot, QObject

class icons(QRunnable):
    def __init__(self, game):
        super().__init__()
        self.vIcons = {}
        self.hIcons = {}

        self.game = game
        self.signals = iconGeneratorSignals()

    @pyqtSlot()
    def run(self):
        self.loadBoatIcons()
        self.game.icons = self
        self.signals.finished.emit()

    def loadBoatIcons(self):
        """Generate all boat icons"""
        lengths = len(self.game.gameDetails["max boats"])
        # Generate all boat icons
        for length in range(2, lengths):
            for i in range(2):
                isVertical = i == 0
                dummy = boat(length, isVertical, 0, 0)
                icons = boatImage(dummy)
                list = self.vIcons if isVertical else self.hIcons
                list[length] = icons

    def get(self, boat, x, y):
        """Get the icon of a boat"""
        index = boat.getIndexes().index((x, y))
        icon = lambda l: self.vIcons[l] if boat.isVertical else self.hIcons[l]
        if boat.isHit(x, y):
            return icon(boat.length).getHitIcon(index)
        else:
            return icon(boat.length).getIcon(index)

class boatImage():
    def __init__(self, boat):
        self.boat = boat
        path = self.getPath(boat.length)

        # Rotate image
        col = 1
        row = self.boat.length
        self.tiles = image_slicer.slice(path, col=col, row=row, save=False) # Slice image into tiles
        
        if not self.boat.isVertical:
            for tile in self.tiles:
                tile.image = tile.image.rotate(90, expand=True)

        # Stretch image
        #col = 1 if self.boat.isVertical else self.boat.length
        #row = self.boat.length if self.boat.isVertical else 1

        self.icons = [self.convertToIcon(tile.image, i) for i, tile in enumerate(self.tiles)] # Convert tiles to icons
        self.hitIcons = [self.getTintedIcon(i) for i in range(len(self.tiles))] # Tint tiles and convert to icons
    
    def convertToIcon(self, image, index):
        """Convert the image to a QIcon"""
        # PIL.image.image -> BytesIO -> QPixmap -> QIcon
        byteIO = BytesIO() 
        #self.tiles[index].image.save(byteIO, format="PNG")
        image.save(byteIO, format="PNG")
        byteArr = byteIO.getvalue()
        pixmap = QPixmap()
        pixmap.loadFromData(byteArr)
        return QIcon(pixmap.scaled(100, 100))
    
    def getTintedIcon(self, index):
        """Tint the image and convert it to a QIcon"""
        original = self.tiles[index].image
        R, G, B = original.split() # Split image into RGB channels
        R = R.point(lambda i: i * 2) # Tint red channel
        tinted = Image.merge("RGB", (R, G, B)) # Merge RGB channels
        return self.convertToIcon(tinted, index)
    
    def getIcon(self, index):
        """Get icon at index"""
        return self.icons[index]
    
    def getHitIcon(self, index):
        """Get hit icon at index"""
        return self.hitIcons[index]
    
    def getPath(self, length):
        """Get path of boat image"""
        path = os.path.join("ui", "graphics", f"boat{length}.png")
        if not os.path.exists(path):
            path = os.path.join("ui", "graphics", "default.gif")
        return path
    

class iconGeneratorSignals(QObject):
    """Send signals from worker thread"""
    finished = pyqtSignal()