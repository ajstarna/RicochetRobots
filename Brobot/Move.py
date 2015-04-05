import random
import numpy as np
from copy import deepcopy

class Move:
	''' the move data structure. field for colour of robot and direction of move. '''
	
	intToColourConversion = ["BLUE", "RED", "GREEN", "YELLOW"] # index with robot number to get colour as string

	def __init__(self, colour, direction):
		self.colour = colour # this int corresponds to the colour ints shown in the Board class
		self.direction = direction # this string is NORTH, SOUTH, EAST, or WEST


	def __str__(self):
		return "Colour = {0} and direction = {1}".format(self.intToColourConversion[self.colour], self.direction)


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
		return deepcopy(random.sample(self.moveSet, 1)[0])

	def getMoveAtIndex(self, index):
		''' return the move at this index '''
		return self.moveSet[index]

	def printMoveSequence(self, sequence):
		''' given a sequence of moves (as ints) prints them out in human-readable format '''
		count = 1
		for moveInt in sequence:
			print("Move {0}: {1}".format(count, self.getMoveAtIndex(moveInt)))
			count += 1


