

class Move:
	''' the move data structure. field for colour of robot and direction of move. '''

	def __init__(self, colour, direction):
		self.colour = colour # this int corresponds to the colour ints shown in the Board class
		self.direction = direction # this string is NORTH, SOUTH, EAST, or WEST



class AllMoves:
	''' this class holds all possibe moves that can be made in Ricochet Robots '''

	def __init__(self):
		self.moveSet = self.createMoveSet()


	def createMoveSet(self):
		''' creates the move set with all possible colours and directions '''
		moveSet = set()
		for colour in xrange(4):
			for direction in ["NORTH", "SOUTH", "EAST", "WEST"]:
				moveSet.add(Move(colour,direction))
		return moveSet


	#def getRandomMove(self):
