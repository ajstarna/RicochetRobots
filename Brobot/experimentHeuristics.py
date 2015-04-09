#!/usr/bin/python

''' this file contains functions for experimenting with the different players and for running many trials and averaging results '''

from Player import RandomPlayer
from MCPlayer import MCPlayer, PNGSPlayer
import Board
import sys, traceback
import time


def runMCPlayerFirstSol(fileName, size, numSamples, depth, reachableWeight, lowerBoundWeight, totalReachableWeight):

	try:
		rr = Board.StandardBoard(size, size, fileName)
		mcPlayer = MCPlayer(rr, reachableWeight, lowerBoundWeight, totalReachableWeight )
		mcPlayer.setTarget()
		
		moveSequence, numMoves = mcPlayer.findFirstSolutionNoTimeLimit(numSamples, depth)
		
		if rr.validateMoveSequence(moveSequence):
			# if the move sequence
			#print("valid sequence with {} moves!".format(numMoves))
			return numMoves
		else:
			print("Invalid sequence with {} moves!".format(numMoves))
			return None

	except:
		print("exception in runMCPlayerFirstSolution")
		traceback.print_exc(file=sys.stdout)
		return None


def playMultipleGames(function, numGames, fileName, size, numSamples, depth, reachableWeight, lowerBoundWeight, totalReachableWeight):
	totalMoves = 0
	movesDict = {}
	for i in xrange(numGames):
		currentMoves = function(fileName, size, numSamples, depth, reachableWeight, lowerBoundWeight, totalReachableWeight)
		if currentMoves == None:
			print("Problem in function {0}".format(function))
			sys.exit(-1)
		else:
			movesDict[currentMoves] = 1 if not currentMoves in movesDict else movesDict[currentMoves]+1
			totalMoves += currentMoves
	return totalMoves/float(numGames), movesDict


if __name__ == "__main__":
	numGames = 20
	depth = 1
	numSamples = 5
	fileName = "builtin1.txt"
	print("Using file = {0}".format(fileName))
	for reachableWeight in [x for x in range(1, 5)]:
		for lowerBoundWeight in [x for x in range(1, 5)]:
			for totalReachableWeight in [x for x in range(1, 5)]:
				
				tstart = time.clock()
	
				if reachableWeight + lowerBoundWeight + totalReachableWeight == 0:
					continue # need some heuristic
				
				print("Running MC with numGames = {2}, depth = {0} and numSamples = {1}".format(depth, numSamples, numGames))
				print("reachableWeight = {0}, lowerBoundWeight = {1}, and totalReachableWeight = {2}".format(reachableWeight, lowerBoundWeight, totalReachableWeight))
				MCAverage, MCDict = playMultipleGames(runMCPlayerFirstSol, numGames, fileName, 16, numSamples, depth, reachableWeight, lowerBoundWeight, totalReachableWeight )
				print("Average Number of Moves Per Game = {0}".format(MCAverage))
				print("Average time per game = {0}\n".format((time.clock() - tstart)/ numGames))























