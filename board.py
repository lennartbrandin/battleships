from boat import boat as class_boat
from multipledispatch import dispatch
class board:
    """A board holding boats and shots"""
    def __init__(self, maxBoats, size, filler):
        self.maxBoats={int(k): int(v) for k, v in maxBoats.items()} # Boat limit per length {0: 0, 1: 0, 2: 4, 3: 3, 4: 2, 5: 1}
        self.boats=[[] for i in range(len(maxBoats))] # Keeps track of boats per length
        self.size=int(size)
        self.filler=filler
        self.board=[[filler for y in range(self.size)] for x in range(self.size)]

    def __str__(self):
        """Return board as formatted string"""
        return '\n'.join([' '.join(str(self.get(x, y)) for x in range(self.size)) for y in range(self.size)])


    @dispatch(class_boat)
    def placeBoat(self, boat):
        """Place a boat on the board"""
        if self.invalidBoatSize(boat):
            raise Exception(f"Invalid boat size: {boat.length}")
        if self.checkMaxBoats(boat):
            raise Exception(f"Max amount of {boat.length} boats reached")
        if self.checkOutOfBounds(boat):
            raise Exception("Boat is out of bounds")
        if self.checkBoatCollision(boat):
            raise Exception("Boat is colliding with another boat")

        self.boats[boat.length].append(boat)

        for x, y in boat.getIndexes():
            self.board[x][y] = boat

    @dispatch(int, int, int, bool, isDestroyed=bool)
    def placeBoat(self, x, y, length, isVertical, isDestroyed=False):
        """Create and place a boat on the board"""
        boat = class_boat(length, isVertical, x, y, isDestroyed)
        self.placeBoat(boat)

    def placeShot(self, x, y, override=False):
        """Shoot indexes at board, return if isHit"""
        if self.checkOutOfBounds(x, y):
            raise Exception("Shot is out of bounds")

        state = self.board[x][y]
        if isinstance(state, class_boat):
            if state.isHit(x, y):
                raise Exception("Boat is already hit")
            state.hit(x, y)
            return True
        else:
            if override != False:
                # If override is set, mark indexes as override
                # Used if websocket communicates a shot
                self.board[x][y] = override
                return True if override == 'HIT' else False
            else:
                self.board[x][y] = 'MISS'
                return False

    def invalidBoatSize(self, boat):
        """Check if boat size is invalid"""
        return boat.length not in self.maxBoats

    def checkMaxBoats(self, boat):
        """Check if max amount of boats with boat length is reached"""
        return len(self.boats[boat.length]) >= self.maxBoats[boat.length]

    @dispatch(class_boat)
    def checkOutOfBounds(self, boat):
        """Check if boat is out of bounds"""
        for x, y in boat.getIndexes():
            if self.checkOutOfBounds(x, y):
                return True
        return False

    @dispatch(int, int)
    def checkOutOfBounds(self, x, y):
        """Check if indexes are out of bounds"""
        return x < 0 or x >= self.size or y < 0 or y >= self.size

    def checkBoatCollision(self, boat):
        """Check if boat is colliding with another boat"""
        collisionArea = boat.getCollisionArea()
        for x, y in collisionArea:
            if self.checkOutOfBounds(x, y):
                continue
            if isinstance(self.board[x][y], class_boat):
                return True
        return False
                
    @dispatch(int, int)
    def get(self, x, y):
        """Get state of indexes"""
        return self.board[x][y] # This can be the boat_obj, filler or 'MISS'

def randomBoard():
    # Test code
    import random
    def place(b, length):
        attempt = 0
        while True:
            isVertical = random.choice([True, False])
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            try:
                b.placeBoat(x, y, length, isVertical)
                return b
            except Exception:
                attempt += 1
                if attempt > 10000:
                    placeAll()
                    break

    def placeAll():            
        b = board({'0': 0, '1': 0, '2': 4, '3': 3, '4': 2, '5': 1}, 10, 'W')
        for length, amount in b.maxBoats.items():
            for i in range(amount):
                t = place(b, length)
        return t

    b = None
    impossibleBoardCount = 0
    while b is None:
        impossibleBoardCount += 1
        b = placeAll()
    return b