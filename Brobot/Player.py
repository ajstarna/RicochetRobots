import Board
import Move
import time

class Player:
	''' this player abstract class contains a Board and has methods for playing the game.
		it is the subclasses' job to implement how the game is played '''



	def __init__(self, board):
		''' initialize a Player by passing in a Board '''
		self.board = board
		self.moves = Move.AllMoves()


	def showBoard(self):
		''' displays the board using the board's printBoard method '''
		self.board.printBoard()


	def play(self, timeLimit):
		''' the play method given with a timeLimit.
			The current best solution must be returned in this timeLimit, and if none have been found, return None 
			Make sure that a current target has been set before this is called (use setTarget)'''
		raise NotImplementedError("Please implement this method")


	def setTarget(self):
		''' sets the target for the current game randomly from the list of targets '''
		self.board.currentTarget = self.board.targetPositions.pop()
		




########################## RandomPlayer subclass #############################

class RandomPlayer(Player):
	''' the simpliest type of player. It will just randomly make moves until it has arrived at the target. '''

	def __init__(self, board):
		Player.__init__(self, board) # call super init


	def play(self, timeLimit):
		''' override super '''
		self.originalPositions = self.board.robotPositions # keep the original positions for resetting the board
		self.currentSequence = [] # keep track of the sequence of moves that brought us to current state

		tStart = time.clock()
		
		while True:
			while not self.board.endState():
				moveToMake = self.moves.getRandomMove()
				self.currentSequence.append(moveToMake)
				self.board.makeMove(moveToMake)

		
		return self.currentSequence, len(self.currentSequence)
		


	def findFirstSolutionNoTimeLimit(self):
		''' this method will randomly make moves until a single solution is found.
			It has no time limit, and will only return the first solution it finds (could last a while) 
			Make sure that a current target has been set before this is called (use setTarget)'''

		originalPositions = self.board.robotPositions # keep the original positions for resetting the board
		currentSequence = [] # keep track of the sequence of moves that brought us to current state

		while not self.board.endState():
			moveToMake = self.moves.getRandomMove()
			currentSequence.append(moveToMake)
			self.board.makeMove(moveToMake)
		
		self.board.resetRobots(originalPositions) # don't want to actually change the board
		return currentSequence, len(currentSequence)
		