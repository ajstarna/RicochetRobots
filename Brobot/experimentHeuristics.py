#!/usr/bin/python

''' this file contains functions for experimenting with the different players and for running many trials and averaging results '''

from Player import RandomPlayer
from MCPlayer import MCPlayer, PNGSPlayer
import Board
import sys, traceback


def runPNGSPlayerFirstSol(fileName, size, numSamples, depth, reachableWeight, lowerBoundWeight, totalReachableWeight):

	try:
		rr = Board.StandardBoard(size, size, fileName)
		pngsPlayer = PNGSPlayer(rr, reachableWeight, lowerBoundWeight, totalReachableWeight )
		pngsPlayer.setTarget()
		
		moveSequence, numMoves = pngsPlayer.findFirstSolutionNoTimeLimit(numSamples, depth)
		
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
	numGames = 10
	depth = 1
	numSamples = 5
	fileName = "builtin1.txt"
	print("Using file = {0}".format(fileName))
	for reachableWeight in [x * 0.1 for x in range(1, 11)]:
		for lowerBoundWeight in [x * 0.1 for x in range(1, 11)]:
			for totalReachableWeight in [x * 0.1 for x in range(1, 11)]:
	
				print("Running PNGS with numGames = {2}, depth = {0} and numSamples = {1}".format(depth, numSamples, numGames))
				print("reachableWeight = {0}, lowerBoundWeight = {1}, and totalReachableWeight = {2}".format(reachableWeight, lowerBoundWeight, totalReachableWeight))
				PNGSAverage, PNGSDict = playMultipleGames(runPNGSPlayerFirstSol, numGames, fileName, 16, numSamples, depth, reachableWeight, lowerBoundWeight, totalReachableWeight )
				print("Average Number of Moves Per Game = {0}\n".format(PNGSAverage))






















