class boat:
    def __init__(self, length, isVertical, x, y, isDestroyed=False):
        """Create a boat object and place it on the board"""
        self.length = length
        self.ID = length # Numeric representation in the board array
        self.isVertical = isVertical # True: array from top to bottom, False: array from left to right.
        self.isHit = [True if isDestroyed else False for i in range(length)] # Integrity of boat, mark as destroyed if isDestroyed is True
        self.x= x # Starting x position
        self.y= y # Starting y position

    def __str__(self):
        """return ID of boat"""
        return "S" if self.isSunk() else str(self.ID)


    def hit(self, x, y):
        """Hit a boat at given index"""
        # Set isHit array at given index to True
        if self.isVertical:
            self.isHit[y - self.y] = True
        else:
            self.isHit[x - self.x] = True
        # Returns true is boat is sunk
        return self.isSunk()

    def isSunk(self):
        """Check if the boat is sunk"""
        # Return True if all components are hit
        return all(self.isHit)
 
    def getID(self):
        """Return the ID of the boat, it also represents the length of the boat"""
        return self.ID

    def getSize(self):
        """Return the length of the boat"""
        return self.length

    def getIntegrity(self):
        """Return the integrity of the boat"""
        return self.isHit

    def getIndexes(self):
        """Return the indexes of the boat"""
        return [self.x, self.y]