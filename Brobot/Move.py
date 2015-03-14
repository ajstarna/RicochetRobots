import random
import numpy as np

class Move:
	''' the move data structure. field for colour of robot and direction of move. '''

	def __init__(self, colour, direction):
		self.colour = colour # this int corresponds to the colour ints shown in the Board class
		self.direction = direction # this string is NORTH, SOUTH, EAST, or WEST



class AllMoves:
	''' this class holds all possibe moves that can be made in Ricochet Robots '''

	def __init__(self):
		self.moveSet = self.createMoveSet() # a np array


	def createMoveSet(self):
		''' creates the move set with all possible colours and directions '''
		moveSet = []
		for colour in xrange(4):
			for direction in ["NORTH", "SOUTH", "EAST", "WEST"]:
				moveSet.append(Move(colour,direction))
		return np.array(moveSet)


	def getRandomMove(self):
		''' return a random move from the moveSet '''
		return random.sample(self.moveSet, 1)[0]