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
		
		moveSequence, numMoves = mcPlayer.play(timeLimit, numSamples, depth )
		
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

def runPNGSPlayerPlay(fileName, size, numSamples, depth, timeLimit):

	try:
		rr = Board.StandardBoard(size, size, fileName)
		pngsPlayer = PNGSPlayer(rr)
		pngsPlayer.setTarget()
		
		moveSequence, numMoves = pngsPlayer.play(timeLimit, numSamples, depth )
		
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

def runRandomPlayerPlay(fileName, size, numSamples, depth, timeLimit):
	# numSamples and depth are useless here, just makes it more convenient to call an arbitrary function
	try:
		rr = Board.StandardBoard(size, size, fileName)
		rPlayer = RandomPlayer(rr)
		rPlayer.setTarget()
		moveSequence, numMoves = rPlayer.play(timeLimit)
		
		if rr.validateMoveSequence(moveSequence):
			# if the move sequence
			#print("valid sequence with {0} moves!".format(numMoves))
			return numMoves
		else:
			#print("Invalid sequence with {0} moves!".format(numMoves))
			return None

	except:
		print("exception in runRandomPlayerPlay")
		traceback.print_exc(file=sys.stdout)
		return None


def runSolverPlay(fileName, size, numSamples, depth, timeLimit):
	# numSamples and depth are useless here, just makes it more convenient to call an arbitrary function
	try:
		rr = Board.StandardBoard(size, size, fileName)
		sPlayer = Solver(rr)
		sPlayer.setTarget()
		moveSequence, numMoves = rPlayer.play(timeLimit)
		
		if rr.validateMoveSequence(moveSequence):
			# if the move sequence
			#print("valid sequence with {0} moves!".format(numMoves))
			return numMoves
		else:
			#print("Invalid sequence with {0} moves!".format(numMoves))
			return None

	except:
		print("exception in runSolverPlay")
		traceback.print_exc(file=sys.stdout)
		return None


def playMultipleGames(function, numGames, fileName, size, numSamples, depth, timeLimit):
	totalMoves = 0
	movesDict = {}
	fails = 0
	for i in xrange(numGames):
		currentMoves = function(fileName, size, numSamples, depth, timeLimit)
		if currentMoves is None:
			# no solution found in timeLimit
			fails += 1
		else:
			movesDict[currentMoves] = 1 if not currentMoves in movesDict else movesDict[currentMoves]+1
			totalMoves += currentMoves
	return totalMoves/float(numGames), movesDict, fails


if __name__ == "__main__":
	numGames = 20

	numSamples = 0
	depth = 0
	
	for depth in [1, 2,3]: #,4,5,6,7,8]:
		for numSamples in [4,6]: #8,10,12,14,16]:
			for timeLimit in [1]:
				print("Running MC with numGames = {2}, depth = {0}, numSamples = {1}, and timeLimit = {3}".format(depth, numSamples, numGames, timeLimit))
				MCAverage, MCDict, fails = playMultipleGames(runMCPlayerPlay, numGames, "builtin1.txt", 16, numSamples, depth, timeLimit)
				print("Average Number of Moves Per Game = {0}".format(MCAverage))

				print("Running PNGS with numGames = {2}, depth = {0}, numSamples = {1}, and timeLimit = {3}".format(depth, numSamples, numGames, timeLimit))
				PNGSAverage, PNGSDict, fails = playMultipleGames(runPNGSPlayerPlay, numGames, "builtin1.txt", 16, numSamples, depth, timeLimit)
				print("Average Number of Moves Per Game = {0}\n".format(PNGSAverage))


	# now run the solver and the random player for different times (don't care about depth or numSamples for them)
	for timeLimit in [1]:
		print("Running Rand with numGames = {0} and timeLimit = {1}".format(numGames, timeLimit))
		RandAverage, RandDict = playMultipleGames(runRandomPlayerPlay, numGames, "builtin1.txt", 16, numSamples, depth, timeLimit)
		print("Average Number of Moves Per Game = {0}".format(RandAverage))

		#print("Running Solver with numGames = {0} and timeLimit = {1}".format(numGames, timeLimit))
		#RandAverage, RandDict = playMultipleGames(runSolverPlay, numGames, "builtin1.txt", 16, numSamples, depth)
		#print("Average Number of Moves Per Game = {0}".format(RandAverage))




















