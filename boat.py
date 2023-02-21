class boat:
    def __init__(self, length, isVertical, x, y, isDestroyed=False):
        self.length=length
        self.isVertical=isVertical
        self.x=x
        self.y=y
        self.hits=[False if not isDestroyed else True for i in range(length)]

    def __str__(self):
        return f"{self.length}"

    def getIndex(self):
        """Get indexes of boat"""
        return self.x, self.y
        
    def getIndexes(self):
        """Get indexes of the boat"""
        if self.isVertical:
            return [(self.x, y) for y in range(self.y, self.y+self.length)]
        else:
            return [(x, self.y) for x in range(self.x, self.x+self.length)]

    def getCollisionArea(self):
        """Get indexes of boat and surrounding indexes"""
        if self.isVertical:
            x1, x2 = self.x-1, self.x+1
            y1, y2 = self.y-1, self.y+self.length
        else:
            x1, x2 = self.x-1, self.x+self.length
            y1, y2 = self.y-1, self.y+1
        return [(x, y) for x in range(x1, x2+1) for y in range(y1, y2+1)]
    
    def hit(self, x, y):
        """Mark hits at index as hit"""
        boatX, boatY = self.getIndex()
        if self.isVertical:
            self.hits[y-boatY] = True
        else:
            self.hits[x-boatX] = True
        return self.isSunk()
    
    def isHit(self, x, y):
        """Check if hits is hit at index"""
        boatX, boatY = self.getIndex()
        if self.isVertical:
            return self.hits[y-boatY]
        else:
            return self.hits[x-boatX]

    def isSunk(self):
        """Check if boat is sunk"""
        return all(self.hits)