#!/usr/bin/python

''' this file contains functions for experimenting with the different players and for running many trials and averaging results '''

from Player import RandomPlayer
from MCPlayer import MCPlayer, PNGSPlayer
import Board
import sys, traceback
from Solver import Solver



def runMCPlayerPlay(fileName, size, numSamples, depth,timeLimit):

	try:
		rr = Board.StandardBoard(size, size, fileName)
		mcPlayer = MCPlayer(rr)
		mcPlayer.setTarget()
		
		moveSequence, numMoves = mcPlayer.play(numSamples, depth)
		
		if rr.validateMoveSequence(moveSequence):
			# if the move sequence
			#print("valid sequence with {} moves!".format(numMoves))
			return numMoves
		else:
			print("Invalid sequence with {} moves!".format(numMoves))
			return None

	except:
		print("exception in runMCPlayerPlay")
		traceback.print_exc(file=sys.stdout)
		return None

def runPNGSPlayerPlay(fileName, size, numSamples, depth):

	try:
		rr = Board.StandardBoard(size, size, fileName)
		pngsPlayer = PNGSPlayer(rr)
		pngsPlayer.setTarget()
		
		moveSequence, numMoves = pngsPlayer.play(numSamples, depth)
		
		if rr.validateMoveSequence(moveSequence):
			# if the move sequence
			#print("valid sequence with {} moves!".format(numMoves))
			return numMoves
		else:
			print("Invalid sequence with {} moves!".format(numMoves))
			return None

	except:
		print("exception in runMCPlayerPlay")
		traceback.print_exc(file=sys.stdout)
		return None


def runPNGSPlayerPlay(fileName, size, numSamples, depth):

	try:
		rr = Board.StandardBoard(size, size, fileName)
		pngsPlayer = PNGSPlayer(rr)
		pngsPlayer.setTarget()
		
		moveSequence, numMoves = pngsPlayer.play(numSamples, depth)
		
		if rr.validateMoveSequence(moveSequence):
			# if the move sequence
			#print("valid sequence with {} moves!".format(numMoves))
			return numMoves
		else:
			print("Invalid sequence with {} moves!".format(numMoves))
			return None

	except:
		print("exception in runMCPlayerPlay")
		traceback.print_exc(file=sys.stdout)
		return None


def runSolverPlay(fileName, size, numSamples, depth, timeLimit):
	# numSamples and depth are useless here, just makes it more convenient to call an arbitrary function
	try:
		rr = Board.StandardBoard(size, size, fileName)
		sPlayer = Solver(rr)
		sPlayer.setTarget()
		moveSequence, numMoves = rPlayer.play()
		
		if rr.validateMoveSequence(moveSequence):
			# if the move sequence
			#print("valid sequence with {0} moves!".format(numMoves))
			return numMoves
		else:
			print("Invalid sequence with {0} moves!".format(numMoves))
			return None

	except:
		print("exception in runRandomPlayerPlay")
		traceback.print_exc(file=sys.stdout)
		return None


def playMultipleGames(function, numGames, fileName, size, numSamples, depth, timeLimit):
	totalMoves = 0
	movesDict = {}
	for i in xrange(numGames):
		currentMoves = function(fileName, size, numSamples, depth)
		if currentMoves == None:
			print("Problem in function {0}".format(function))
			sys.exit(-1)
		else:
			movesDict[currentMoves] = 1 if not currentMoves in movesDict else movesDict[currentMoves]+1
			totalMoves += currentMoves
	return totalMoves/float(numGames), movesDict


if __name__ == "__main__":
	numGames = 20

	numSamples = 10
	depth = 4
	
	for depth in [1, 2,3]: #,4,5,6,7,8]:
		for numSamples in [4,6]: #8,10,12,14,16]:
			print("Running MC with numGames = {2}, depth = {0} and numSamples = {1}".format(depth, numSamples, numGames))
			MCAverage, MCDict = playMultipleGames(runMCPlayerPlay, numGames, "builtin1.txt", 16, numSamples, depth)
			#print(MCDict)
			print("Average Number of Moves Per Game = {0}".format(MCAverage))

			print("Running PNGS with numGames = {2}, depth = {0} and numSamples = {1}".format(depth, numSamples, numGames))
			PNGSAverage, PNGSDict = playMultipleGames(runPNGSPlayerPlay, numGames, "builtin1.txt", 16, numSamples, depth)
			#print(PNGSDict)
			print("Average Number of Moves Per Game = {0}\n".format(PNGSAverage))


	print("Running Rand with numGames = {0}".format(numGames))
	RandAverage, RandDict = playMultipleGames(runRandomPlayerPlay, numGames, "builtin1.txt", 16, numSamples, depth)
	#print(RandDict)
	print("Average Number of Moves Per Game = {0}".format(RandAverage))




















