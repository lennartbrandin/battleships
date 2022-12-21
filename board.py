from multipledispatch import dispatch # For overloading functions
from boat import boat as class_boat

class board:
    def __init__(self, maxBoats, size):
        self.size = size
        self.maxBoats = maxBoats # List of maximum amount of boats with the index as the length of the boat
        self._board = [[0 for a in range(size)] for b in range(size)] # 2D array to represent the board, fill with 0s
        self.boats = [[] for i in range(len(self.maxBoats))] # Empty list of boats on the board
        

    def __str__(self):
        """Return a formatted string of the board"""
        formattedString = ""
        for y in range(self.size):
            for x in range(self.size):
                formattedString += str(self.getState(x,y)) + " "
            formattedString += "\n"
        return formattedString

    def shoot(self, x, y):
        """Shoot a coordinate on the board"""
        if self.checkOutOfBounds(x, y):
            raise ValueError("Coordinates are out of bounds")
        # TODO: Check if server allows shooting at this coordinate (In file: server.py)
        x, y = board.toIndex(x, y)

        
        if self._board[y][x] == 0:
            self._board[y][x] = 'M'
            return False
        elif isinstance(self._board[y][x], class_boat):
            self._board[y][x].hit(x, y)
            return True

    def placeBoat(self, boat):
        """Place a boat on the board"""
        # Get boat indexes from coordinates
        x, y = boat.getCoordinates()

        # Check if the maximum amount of boats are on the board
        if self.checkMaxAmount(boat):
            raise ValueError("Maximum amount of boats with the length of " + str(boat.getSize()) + " are on the board")

        # Check if initial coordinates or maximum coordinates are out of bounds, differ between vertical and horizontal
        if self.checkOutOfBounds(x, y) or self.checkOutOfBounds(x, y + boat.getSize()) if boat.isVertical else self.checkOutOfBounds(x + boat.getSize(), y):
            raise ValueError("Coordinates are out of bounds")

        # Check if surrounding coordinates are not boat
        if self.checkCollision(boat):
            raise ValueError("Coordinates are occupied")
        
        x, y = board.toIndex(x, y)

        self.boats[boat.getSize()].append(boat) # Add boat to list of same length boats in list of boats

        if boat.isVertical:
            # Fill array with boat ID horizontally or vertically
            for i in range(boat.getSize()):
                self._board[y+i][x] = boat
        else:
            for i in range(boat.getSize()):
                self._board[y][x+i] = boat

    def checkOutOfBounds(self, x, y):
        """Check if coordinates are out of bounds"""
        if x <= 0 or y <= 0 or x > self.size or y > self.size:
            # Return True if coordinates are out of bounds
            return True
        return False

    def checkCollision(self, boat):
        """Check if coordinates and the x or y coordinates that the boat will take up are empty.
        Check if the space around the boat is empty"""
        # Convert coordinates to array indexes
        x, y = board.toIndex(*boat.getCoordinates())

        checkRange = []
        # Get the range of coordinates around the boat to check
        if boat.isVertical:
            x1 = x - 1
            x2 = x + 1
            y1 = y - 1
            y2 = y + boat.getSize()
            checkRange = self.getState(x1, x2, y1, y2)
        else:
            x1 = x - 1
            x2 = x + boat.getSize()
            y1 = y - 1
            y2 = y + 1
            checkRange = self.getState(x1, x2, y1, y2)

        # Iterate through the yRange
        isFree = []
        for yRange in checkRange:
            # Iterate through x in yRange, check if its not a boat
            # Append to isFree if is not a boat
            for x in yRange:
                isFree.append(not(isinstance(x, class_boat))) # If x is not a boat, append True to isFree

        # Check if all values in isFree are True
        if all(isFree):
            return False
        return True

    def checkMaxAmount(self, boat):
        """Check if the maximum amount of boats are on the board"""
        # Raise exception if the boat length is greater than the maxBoats list
        if boat.getSize() > len(self.maxBoats):
            raise ValueError("Boat length is greater than the amount of declared boat lengths")
        if len(self.boats[boat.getSize()]) >= self.maxBoats[boat.getSize()]:
            return True
        return False

    # def occupation(self):
    #     """Return the board occupation"""
    #     isOccupied = self.getBoard() # Copy the board
    #     for y in range(isOccupied.size):
    #         for x in range(isOccupied.size):
    #             state = self.getBoard().getState(x, y)
    #             if state == isinstance(state, class_boat):
    #                 x1, y1 = x-1, y-1
    #                 if state.isVertical:
    #                     x2, y2 = x+1, y+state.length
    #                 else:
    #                     x2, y2 = x+state.length, y+1
    #                 # Set range around boat to true
    #                 isOccupied.setState(x1, x2, y1, y2, True)
    #     return isOccupied

    @dispatch(int, int)
    def getState(self, x, y):
        """Return the state of coordinates in the board"""
        state = self._board[y][x]
        if isinstance(state, class_boat) and not state.isSunk:
            boat = state # Better naming
            # If an boat and isHit at pos, return 'X'
            boatX, boatY = board.toIndex(boat.getCoordinates())
            if boat.isVertical:
                if boat.isHit[y-boatY]:
                    return 'X'
            else:
                if boat.isHit[x-boatX]:
                    return 'X'
        # Else return state (0 / M / boat.ID)
        return state

    @dispatch(int, int, int, int)
    def getState(self, x1, x2, y1, y2):
        """Return the state of coordinates in the board, given in a range"""
        # Adjust coordinates if out of bounds
        x1, x2, y1, y2 = self.adjustIndex(x1, x2, y1, y2)

        # Adjust upper indexes to be inclusive when extracting the range
        x2 += 1
        y2 += 1
        # Extract the range of indexes from the board
        return [row[x1:x2] for row in self._board[y1:y2]]

    # @dispatch(int, int)
    # def setState(self, x, y, state):
    #     """Set the state of coordinates in the board"""
    #     self._board[y][x] = state

    # @dispatch(int, int, int, int)
    # def setState(self, x1, x2, y1, y2, state):
    #     """Set state of coordinate range in the board"""
    #     # Adjust coordinates if out of bounds
    #     x1, x2, y1, y2 = self.adjustIndex(x1, x2, y1, y2)

    #     # Set the range of indexes from the board
    #     for y in range(y1, y2):
    #         for x in range(x1, x2):
    #             self._board[y][x] = state

    def adjustIndex(self, *coordinates):
        """Adjust coordinates if out of bounds"""
        adjustedCoordinates = []
        for coordinate in coordinates:
            # If coordinate is less than 0, set it to 0 else check if it is greater than the max width, if so set to index of max width
            adjustedCoordinates.append(0 if coordinate < 0 else coordinate if coordinate < self.size else self.size-1)
        return adjustedCoordinates

    @staticmethod 
    @dispatch(int, int)
    def toIndex(x, y):
        """Convert coordinates to array indexes"""
        return x - 1, y - 1

    @staticmethod
    @dispatch(list)
    def toIndex(coordinates):
        """Convert coordinates to array indexes"""
        return [x - 1 for x in coordinates]
    
    @staticmethod
    @dispatch(int, int)
    def toCoordinates(x, y):
        """Convert array indexes to coordinates"""
        return x + 1, y + 1

    @staticmethod
    @dispatch(list)
    def toCoordinates(indexes):
        """Convert array indexes to coordinates"""
        return [x + 1 for x in indexes]