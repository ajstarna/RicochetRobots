#!/usr/bin/python

''' this file contains functions for experimenting with the timing of methods '''

from Player import RandomPlayer
from MCPlayer import MCPlayer, PNGSPlayer
import Board
import sys, traceback
import time
from Solver import Solver



def timeMCPlayer(fileName, size, numSamples, depth):

	try:
		rr = Board.StandardBoard(size, size, fileName)
		mcPlayer = MCPlayer(rr)
		mcPlayer.setTarget()
		
		moveSequence, numMoves = mcPlayer.findFirstSolutionNoTimeLimit(numSamples, depth)
		
		if rr.validateMoveSequence(moveSequence):
			return numMoves
		else:
			print("Invalid sequence with {} moves!".format(numMoves))
			return None

	except:
		print("exception in timeMCPlayer")
		traceback.print_exc(file=sys.stdout)
		return None


def timePNGSPlayer(fileName, size, numSamples, depth):

	try:
		rr = Board.StandardBoard(size, size, fileName)
		pngsPlayer = PNGSPlayer(rr)
		pngsPlayer.setTarget()
		
		moveSequence, numMoves = pngsPlayer.findFirstSolutionNoTimeLimit(numSamples, depth)
		
		if rr.validateMoveSequence(moveSequence):
			return numMoves
		else:
			print("Invalid sequence with {} moves!".format(numMoves))
			return None

	except:
		print("exception in timeMCPlayer")
		traceback.print_exc(file=sys.stdout)
		return None



def timeSolver(fileName, size, numSamples, depth):
	# numSamples and depth are useless here, just makes it more convenient to call an arbitrary function
	try:
		rr = Board.StandardBoard(size, size, fileName)
		sPlayer = Solver(rr)
		sPlayer.setTarget()
		bestDepth, best = sPlayer.play(1000)
		
		if best == -1:
			# no solution found
			print("best == -1")
			return None
		
		moveSequence = sPlayer.getSolution(best)
		
		
		if rr.validateMoveSequence(moveSequence):
			# if the move sequence
			#print("valid sequence with {0} moves!".format(numMoves))
			return len(moveSequence)
		else:
			print("Invalid sequence with {0} moves!".format(len(moveSequence)))
			rr.allMoves.printMoveSequence(moveSequence)
			print(moveSequence)
			
			return None

	except:
		print("exception in timeSolver")
		traceback.print_exc(file=sys.stdout)
		return None



def playMultipleGames(function, numGames, fileName, size, numSamples, depth):
	totalMoves = 0
	movesDict = {}
	totalTime = 0
	for i in xrange(numGames):
		tstart = time.clock()
		currentMoves = function(fileName, size, numSamples, depth)
		if currentMoves == None:
			print("Problem in function {0}".format(function))
			sys.exit(-1)
		else:
			movesDict[currentMoves] = 1 if not currentMoves in movesDict else movesDict[currentMoves]+1
			totalMoves += currentMoves
			totalTime += time.clock() - tstart
	return totalMoves/float(numGames), movesDict, totalTime/float(numGames)


if __name__ == "__main__":
	numGames = 20

	numSamples = 10
	depth = 4
	'''
	print("Running Solve with numGames = {0}".format(numGames))
	solveAverage, solveDict, solveTime = playMultipleGames(timeSolver, numGames, "builtin1.txt", 16, numSamples, depth)
	print("Average Number of Moves Per Game = {0}".format(solveAverage))
	print("Average Time Per Game = {0}".format(solveTime))
	'''
	for depth in [1, 2,3]: #,4,5,6,7,8]:
		for numSamples in [4,6]: #8,10,12,14,16]:
			print("Running MC with numGames = {2}, depth = {0} and numSamples = {1}".format(depth, numSamples, numGames))
			MCAverage, MCDict, MCtime = playMultipleGames(timeMCPlayer, numGames, "builtin1.txt", 16, numSamples, depth)
			print("Average Number of Moves Per Game = {0}".format(MCAverage))
			print("Average Time Per Game = {0}".format(MCtime))

			print("Running PNGS with numGames = {2}, depth = {0} and numSamples = {1}".format(depth, numSamples, numGames))
			PNGSAverage, PNGSDict, PNGStime = playMultipleGames(timePNGSPlayer, numGames, "builtin1.txt", 16, numSamples, depth)
			print("Average Number of Moves Per Game = {0}".format(PNGSAverage))
			print("Average Time Per Game = {0}\n".format(PNGStime))



















