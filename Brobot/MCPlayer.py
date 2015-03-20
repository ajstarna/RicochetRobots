from Player import Player
from copy import deepcopy

class MCPlayer(Player):
	def __init__(self, board):
		Player.__init__(self, board)

	def findFirstSolutionNoTimeLimit(self, numSamples, depth):

		originalPositions = deepcopy(self.board.robotPositions) # keep the original positions for resetting the board
		currentSequence = [] # keep track of the sequence of moves that brought us to current state
		
		#currentPositions = deepcopy(self.board.robotPositions)
		self.numMoves = 0
		while not self.board.endState():
			newSequence = self.jumpAhead(numSamples, depth)
			currentSequence += newSequence
			print("len(currentSequence) = {0}, numMoves = {1}".format(len(currentSequence), self.numMoves))

		print("robot positions at alleged endstate = {0}".format(self.board.robotPositions))

		self.board.resetRobots(originalPositions) # don't want to actually change the board
		return currentSequence, len(currentSequence)



	def jumpAhead(self, n, d):
		''' n the number of samples.
			d the depth of each sample
		'''
		startPositions = deepcopy(self.board.robotPositions)
		currentValue = 0
		#for i in xrange(n):
		sequence = self.sample(d)
		value = self.evaluateState()
		#	if value > currentValue:
		bestSequence = deepcopy(sequence)
		currentValue = value
		#	self.board.resetRobots(startPositions)

		# now play the moves from the best found sequence
		#for move in bestSequence:
		#	self.board.makeMove(move)

		return bestSequence
	


	def sample(self, d):
		sequence = []
		for i in xrange(d):
			moveToMake = self.moves.getRandomMove()
			sequence.append(moveToMake)
			self.board.makeMove(moveToMake)
			self.numMoves += 1
		return sequence


	def evaluateState(self):
		return 10