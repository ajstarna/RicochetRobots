import Board
import Move
import time
import numpy as np
from copy import deepcopy
import random

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


	def findFirstSolutionNoTimeLimit(self):
		''' this method will search until a single solution is found.
			It has no time limit, and will only return the first solution it finds (could last a while) 
			Make sure that a current target has been set before this is called (use setTarget)'''
		raise NotImplementedError("Please implement this method")


	def setTarget(self):
		''' sets the target for the current game randomly from the list of targets '''
		self.board.setTarget()
		self.board.lowerBoundPreProc() # set up the lower bound in each tile
		
		
	def printMoveSequence(self, sequence):
		''' this method takes a sequence of moves (as ints) and prints them in human-readable format '''
		self.moves.printMoveSequence(sequence)
			



########################## RandomPlayer subclass #############################

class RandomPlayer(Player):
	''' the simpliest type of player. It will just randomly make moves until it has arrived at the target. '''

	def __init__(self, board):
		Player.__init__(self, board) # call super init


	def play(self, timeLimit):
		''' override super '''
		originalPositions = deepcopy(self.board.robotPositions) # keep the original positions for resetting the board
		currentSequence = [] # keep track of the sequence of moves that brought us to current state
		bestSequence = None # this will be the best of all sequences found
		tStart = time.clock()
		
		while True:
	
			while not self.board.endState():
				if bestSequence != None and len(currentSequence) >= len(bestSequence):
					# no need to keep looking on this path
					currentSequence = []
					self.board.resetRobots(originalPositions)
					continue
				
				
				moveToMake = random.randint(0,15)
				currentSequence.append(moveToMake)
				self.board.makeMoveByInt(moveToMake)

				if time.clock() - tStart >= timeLimit:
					
					self.board.resetRobots(originalPositions)
					if bestSequence == None:
						return [], float("inf")
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

		
		
		


	def findFirstSolutionNoTimeLimit(self):
		''' this method will randomly make moves until a single solution is found.
			It has no time limit, and will only return the first solution it finds (could last a while) 
			Make sure that a current target has been set before this is called (use setTarget)'''

		if (not self.board.correctRobotTiles()):
			print("Incorrect robot posititions at start of findFirstSol")

		originalPositions = deepcopy(self.board.robotPositions) # keep the original positions for resetting the board
		currentSequence = [] # keep track of the sequence of moves that brought us to current state

		while not self.board.endState():
			moveToMake = random.randint(0,15) # 16 possible moves; this is the index
			currentSequence.append(moveToMake)
			self.board.makeMoveByInt(moveToMake)

		
		self.board.resetRobots(originalPositions) # don't want to actually change the board
		if (not self.board.correctRobotTiles()):
			print("Incorrect robot posititions at END of findFirstSol")		
		
		return currentSequence, len(currentSequence)



	'''
	def dictFromSequence(self, originalPositions, currentSequence):
		rr = deepcopy(self.board)
		rr.resetRobots(originalPositions)
		
		for move in currentSequence:
			rr.makeMoveByInt(move)

		return rr.robotPositions
	'''


















