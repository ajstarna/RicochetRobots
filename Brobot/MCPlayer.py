from Player import Player


class MCPlayer(Player):
	def __init__(self, board):
		Player.__init__(self, board)

	def findFirstSolutionNoTimeLimit(self):

		originalPositions = self.board.robotPositions # keep the original positions for resetting the board
		currentSequence = [] # keep track of the sequence of moves that brought us to current state

		while not self.board.endState():
			moveToMake = self.moves.getRandomMove()
			currentSequence.append(moveToMake)
			self.board.makeMove(moveToMake)
		
		self.board.resetRobots(originalPositions) # don't want to actually change the board
		return currentSequence, len(currentSequence)



	def sample(self, n):
		return