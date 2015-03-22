from Player import Player
from copy import deepcopy
import random
import time

class MCPlayer(Player):
	def __init__(self, board):
		Player.__init__(self, board)
	
	
	
	def play(self, timeLimit, numSamples, depth):
		''' override super '''
		originalPositions = deepcopy(self.board.robotPositions) # keep the original positions for resetting the board
		currentSequence = [] # keep track of the sequence of moves that brought us to current state
		bestSequence = None # this will be the best of all sequences found
		tStart = time.clock()
		
		while True:
			self.numMoves = 0
			while not self.board.endState():
				if bestSequence != None and len(currentSequence) >= len(bestSequence):
					# no need to keep looking on this path
					currentSequence = []
					self.board.resetRobots(originalPositions)
					continue
				
				newSequence = self.jumpAhead(numSamples, depth)
				currentSequence += newSequence

				if time.clock() - tStart >= timeLimit:
					
					self.board.resetRobots(originalPositions)
					if bestSequence == None:
						return [], 0
					else:
						return bestSequence, len(bestSequence)
			
			# at this point it is an endstate
			if bestSequence == None:
				#print("Updating best sequence with length of {0}".format(len(self.currentSequence)))
				bestSequence = currentSequence
			elif len(bestSequence) > len(currentSequence):
				#print("Updating best sequence with length of {0}".format(len(self.currentSequence)))
				bestSequence = currentSequence


			currentSequence = []
			self.board.resetRobots(originalPositions)
	
	
	

	def findFirstSolutionNoTimeLimit(self, numSamples, depth):

		originalPositions = deepcopy(self.board.robotPositions) # keep the original positions for resetting the board
		currentSequence = [] # keep track of the sequence of moves that brought us to current state
		
		self.numMoves = 0
		while not self.board.endState():
			newSequence = self.jumpAhead(numSamples, depth)
			currentSequence += newSequence


		self.board.resetRobots(originalPositions) # don't want to actually change the board
		return currentSequence, len(currentSequence)



	def jumpAhead(self, numSamples, depth):
		''' n the number of samples.
			d the depth of each sample
		'''
		startPositions = deepcopy(self.board.robotPositions)
		currentValue = 0
		for i in xrange(numSamples):
			sequence = self.sample(depth)
			value = self.evaluateState()
			if value > currentValue:
				bestSequence = deepcopy(sequence)
				currentValue = value
			self.board.resetRobots(startPositions)

		# now play the moves from the best found sequence
		for move in bestSequence:
			self.board.makeMoveByInt(move)

		return bestSequence
	


	def sample(self, depth):
		sequence = []
		for i in xrange(depth):
			moveToMake = random.randint(0,15)
			sequence.append(moveToMake)
			self.board.makeMoveByInt(moveToMake)
			self.numMoves += 1
		return sequence


	def evaluateState(self):
		totalReachableTiles = self.board.CalcReachability
		blueTile = self.board.getTileOfRobot(Board.Board.BLUE)
		currentReachability = blueTile.reachable
		lowerBound = blueTile.lowerBound
		
		return 10






